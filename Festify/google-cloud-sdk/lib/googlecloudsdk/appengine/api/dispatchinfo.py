# Copyright 2012 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Dispatch configuration tools.

Library for parsing dispatch.yaml files and working with these in memory.
"""

from __future__ import absolute_import
from __future__ import unicode_literals


# WARNING: This file is externally viewable by our users.  All comments from
# this file will be stripped.  The docstrings will NOT.  Do not put sensitive
# information in docstrings.  If you must communicate internal information in
# this source file, please place them in comments only.

import os
import re
from googlecloudsdk.appengine._internal import six_subset

# pylint: disable=g-import-not-at-top
if os.environ.get('APPENGINE_RUNTIME') == 'python27':
  from google.appengine.api import appinfo
  from google.appengine.api import validation
  from google.appengine.api import yaml_builder
  from google.appengine.api import yaml_listener
  from google.appengine.api import yaml_object
else:
  from googlecloudsdk.appengine.api import appinfo
  from googlecloudsdk.appengine.api import validation
  from googlecloudsdk.appengine.api import yaml_builder
  from googlecloudsdk.appengine.api import yaml_listener
  from googlecloudsdk.appengine.api import yaml_object
# pylint: enable=g-import-not-at-top

_URL_SPLITTER_RE = re.compile(r'^([^/]+)(/.*)$')

# Regular expression for a hostname based on
# http://tools.ietf.org/html/rfc1123.
#
# This pattern is more restrictive than the RFC because it only accepts
# lower case letters.
_URL_HOST_EXACT_PATTERN_RE = re.compile(r"""
# 0 or more . terminated hostname segments (may not start or end in -).
^([a-z0-9]([a-z0-9\-]*[a-z0-9])*\.)*
# followed by a host name segment.
([a-z0-9]([a-z0-9\-]*[a-z0-9])*)$""", re.VERBOSE)

_URL_IP_V4_ADDR_RE = re.compile(r"""
#4 1-3 digit numbers separated by .
^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$""", re.VERBOSE)

# Regualar expression for a prefix of a hostname based on
# http://tools.ietf.org/html/rfc1123. Restricted to lower case letters.
_URL_HOST_SUFFIX_PATTERN_RE = re.compile(r"""
# Single star or
^([*]|
# Host prefix with no .,  Ex '*-a' or
[*][a-z0-9\-]*[a-z0-9]|
# Host prefix with ., Ex '*-a.b-c.d'
[*](\.|[a-z0-9\-]*[a-z0-9]\.)([a-z0-9]([a-z0-9\-]*[a-z0-9])*\.)*
([a-z0-9]([a-z0-9\-]*[a-z0-9])*))$
""", re.VERBOSE)

APPLICATION = 'application'
DISPATCH = 'dispatch'
URL = 'url'
MODULE = 'module'
SERVICE = 'service'


class Error(Exception):
  """Base class for errors in this module."""


class MalformedDispatchConfigurationError(Error):
  """Configuration file for dispatch is malformed."""


class DispatchEntryURLValidator(validation.Validator):
  """Validater for URL patterns."""

  def Validate(self, value, unused_key=None):
    """Validates an URL pattern."""
    if value is None:
      raise validation.MissingAttribute('url must be specified')
    if not isinstance(value, six_subset.string_types):
      raise validation.ValidationError('url must be a string, not \'%r\'' %
                                       type(value))

    url_holder = ParsedURL(value)
    if url_holder.host_exact:
      _ValidateMatch(_URL_HOST_EXACT_PATTERN_RE, url_holder.host,
                     'invalid host_pattern \'%s\'' % url_holder.host)
      # Explicitly disallow IpV4 #.#.#.# addresses. These will match
      # _URL_HOST_EXACT_PATTERN_RE above.
      _ValidateNotIpV4Address(url_holder.host)
    else:
      _ValidateMatch(_URL_HOST_SUFFIX_PATTERN_RE, url_holder.host_pattern,
                     'invalid host_pattern \'%s\'' % url_holder.host_pattern)

    #TODO(user): validate path_pattern and lengths of both patterns.
    #                also validate hostname label lengths 63 charn max)
    return value


class ParsedURL(object):
  """Dispath Entry URL holder class.

  Attributes:
    host_pattern: The host pattern component of the URL pattern.
    host_exact: True if the host pattern does not start with a *.
    host: host_pattern  with any leading * removed.
    path_pattern: The path pattern component of the URL pattern.
    path_exact: True if the path_pattern does not end with a *.
    path: path_pattern with any trailing * removed.
  """

  def __init__(self, url_pattern):
    """Initializes this ParsedURL with an URL pattern value.

    Args:
      url_pattern: An URL pattern that conforms to the regular expression
          '^([^/]+)(/.*)$'.

    Raises:
      validation.ValidationError: When url_pattern does not match the required
          regular expression.
    """
    split_matcher = _ValidateMatch(_URL_SPLITTER_RE, url_pattern,
                                   'invalid url \'%s\'' % url_pattern)
    self.host_pattern, self.path_pattern = split_matcher.groups()
    if self.host_pattern.startswith('*'):
      self.host_exact = False
      self.host = self.host_pattern[1:]
    else:
      self.host_exact = True
      self.host = self.host_pattern

    if self.path_pattern.endswith('*'):
      self.path_exact = False
      self.path = self.path_pattern[:-1]
    else:
      self.path_exact = True
      self.path = self.path_pattern


def _ValidateMatch(regex, value, message):
  """Validate value matches regex."""
  matcher = regex.match(value)
  if not matcher:
    raise validation.ValidationError(message)
  return matcher


def _ValidateNotIpV4Address(host):
  """Validate host is not an IPV4 address."""
  matcher = _URL_IP_V4_ADDR_RE.match(host)
  if matcher and sum(1 for x in matcher.groups() if int(x) <= 255) == 4:
    raise validation.ValidationError('Host may not match an ipv4 address \'%s\''
                                     % host)
  return matcher


class DispatchEntry(validation.Validated):
  """A Dispatch entry describes a mapping from a URL pattern to a module."""
  ATTRIBUTES = {
      URL: DispatchEntryURLValidator(),
      SERVICE: validation.Preferred(MODULE, appinfo.MODULE_ID_RE_STRING),
      MODULE: validation.Deprecated(SERVICE, appinfo.MODULE_ID_RE_STRING),
  }


class DispatchInfoExternal(validation.Validated):
  """Describes the format of a dispatch.yaml file."""
  ATTRIBUTES = {
      APPLICATION: validation.Optional(appinfo.APPLICATION_RE_STRING),
      DISPATCH: validation.Optional(validation.Repeated(DispatchEntry)),
  }


def LoadSingleDispatch(dispatch_info, open_fn=None):
  """Load a dispatch.yaml file or string and return a DispatchInfoExternal.

  Args:
    dispatch_info: The contents of a dispatch.yaml file as a string, or an open
      file object.
    open_fn: Function for opening files. Unused here, needed to provide
      a polymorphic API used by appcfg.py yaml parsing.

  Returns:
    A DispatchInfoExternal instance which represents the contents of the parsed
      yaml file.

  Raises:
    MalformedDispatchConfigurationError: The yaml file contains multiple
      dispatch sections or is missing a required value.
    yaml_errors.EventError: An error occured while parsing the yaml file.
  """
  builder = yaml_object.ObjectBuilder(DispatchInfoExternal)
  handler = yaml_builder.BuilderHandler(builder)
  listener = yaml_listener.EventListener(handler)
  listener.Parse(dispatch_info)

  parsed_yaml = handler.GetResults()
  if not parsed_yaml:
    return DispatchInfoExternal()
  if len(parsed_yaml) > 1:
    raise MalformedDispatchConfigurationError('Multiple dispatch: sections '
                                              'in configuration.')

  # The validation framework doesn't allow validating multiple fields at once,
  # so we have to check here.
  dispatch_info_external = parsed_yaml[0]
  dispatch_info_external.CheckInitialized()
  return dispatch_info_external
