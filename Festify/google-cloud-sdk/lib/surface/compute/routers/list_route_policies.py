# -*- coding: utf-8 -*- #
# Copyright 2023 Google LLC. All Rights Reserved.
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

"""Command for listing route policies from a Compute Engine router."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from apitools.base.py import list_pager
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute import flags as compute_flags
from googlecloudsdk.command_lib.compute.routers import flags


@base.UniverseCompatible
class ListRoutePolicies(base.ListCommand):
  """List route policies from a Compute Engine router."""

  ROUTER_ARG = None

  @classmethod
  def Args(cls, parser):
    ListRoutePolicies.ROUTER_ARG = flags.RouterArgument()
    ListRoutePolicies.ROUTER_ARG.AddArgument(parser, operation_type='list')
    parser.display_info.AddCacheUpdater(flags.RoutersCompleter)
    parser.display_info.AddFormat('table(name, type)')

  def Run(self, args):
    """Issues a request necessary for listing route policies from a Router."""
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client

    router_ref = ListRoutePolicies.ROUTER_ARG.ResolveAsResource(
        args,
        holder.resources,
        scope_lister=compute_flags.GetDefaultScopeLister(client),
    )

    request = client.messages.ComputeRoutersListRoutePoliciesRequest(
        **router_ref.AsDict()
    )
    return list_pager.YieldFromList(
        client.apitools_client.routers,
        request,
        limit=args.limit,
        batch_size=args.page_size,
        method='ListRoutePolicies',
        field='result',
        current_token_attribute='pageToken',
        next_token_attribute='nextPageToken',
        batch_size_attribute='maxResults',
    )

ListRoutePolicies.detailed_help = {
    'DESCRIPTION': """\
*{command}* lists all route policies from a Compute Engine router.
        """,
    'EXAMPLES': """\
        To list route policies from a router `my-router` in region `us-central1`, run:

              $ {command} my-router --region=us-central1
        """,
}
