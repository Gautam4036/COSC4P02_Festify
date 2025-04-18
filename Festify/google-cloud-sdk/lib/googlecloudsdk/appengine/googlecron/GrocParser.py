# Copyright 2016 Google LLC. All Rights Reserved.
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

import sys
from antlr3 import *
from antlr3.compat import set, frozenset

# Copyright 2005-2009 Google, Inc.  All rights reserved.
# @author arb@google.com (Anthony Baxter)
# Based on original C++ version by
# @author estlin@google.com (Brian Estlin)

# Groc (Googley runner of commands) is a microlanguage that provides an
# alternative to traditional cron syntax/semantics for specifying
# recurrent events.  Syntactically, it is designed to be more readable
# (more easily 'grokked') than crontab language.  Groc forfeits certain
# semantics found in crontab, in favor of readability; however,
# certain timespecs which are awkward in crontab are much easier
# to express in Groc (for example, the 3rd tuesday of the month).
# It is these constructs to which Groc is best suited.
#
# Examples of valid Groc include:
# '1st,3rd monday of month 15:30'
# 'every wed,fri of jan,jun 13:15'
# 'first sunday of quarter 00:00'
# 'every 2 hours'
#
# FEATURES NOT YET IMPLEMENTED (in approx. order of priority):
# - some way to specify multiple values for minutes/hours (definitely)
# - 'am/pm' (probably)
# - other range/interval functionality (maybe)
__author__ = 'arb@google.com (Anthony Baxter)'

# WARNING: This file is externally viewable by our users.  All comments from
# this file will be stripped.  The docstrings will NOT.  Do not put sensitive
# information in docstrings.  If you must communicate internal information in
# this source file, please place them in comments only.


allOrdinals = set([1, 2, 3, 4, 5])
numOrdinals = len(allOrdinals)




# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
MONTH=27
THURSDAY=23
FOURTH_OR_FIFTH=16
THIRD=13
DECEMBER=39
FROM=41
EVERY=6
WEDNESDAY=22
QUARTER=40
SATURDAY=25
SYNCHRONIZED=9
JANUARY=28
SUNDAY=26
TUESDAY=21
SEPTEMBER=36
UNKNOWN_TOKEN=45
AUGUST=35
JULY=34
MAY=32
FRIDAY=24
DIGITS=8
FEBRUARY=29
TWO_DIGIT_HOUR_TIME=43
OF=4
WS=44
EOF=-1
APRIL=31
COMMA=10
JUNE=33
OCTOBER=37
TIME=5
FIFTH=15
NOVEMBER=38
FIRST=11
DIGIT=7
FOURTH=14
MONDAY=20
HOURS=17
MARCH=30
SECOND=12
MINUTES=18
TO=42
DAY=19

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "OF", "TIME", "EVERY", "DIGIT", "DIGITS", "SYNCHRONIZED", "COMMA", "FIRST",
    "SECOND", "THIRD", "FOURTH", "FIFTH", "FOURTH_OR_FIFTH", "HOURS", "MINUTES",
    "DAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY",
    "SUNDAY", "MONTH", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
    "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "QUARTER",
    "FROM", "TO", "TWO_DIGIT_HOUR_TIME", "WS", "UNKNOWN_TOKEN"
]




class GrocParser(Parser):
    grammarFileName = "borg/borgcron/py/Groc.g"
    antlr_version = version_str_to_tuple("3.1.1")
    antlr_version_str = "3.1.1"
    tokenNames = tokenNames

    def __init__(self, input, state=None):
        if state is None:
            state = RecognizerSharedState()

        Parser.__init__(self, input, state)


        self.dfa4 = self.DFA4(
            self, 4,
            eot = self.DFA4_eot,
            eof = self.DFA4_eof,
            min = self.DFA4_min,
            max = self.DFA4_max,
            accept = self.DFA4_accept,
            special = self.DFA4_special,
            transition = self.DFA4_transition
            )




        self.ordinal_set = set()
        self.weekday_set = set()
        self.month_set = set()
        self.monthday_set = set()
        self.time_string = ''
        self.interval_mins = 0
        self.period_string = ''
        self.synchronized = False
        self.start_time_string = ''
        self.end_time_string = ''










    valuesDict = {
        SUNDAY: 0,
        FIRST: 1,
        MONDAY: 1,
        JANUARY: 1,
        TUESDAY: 2,
        SECOND: 2,
        FEBRUARY: 2,
        WEDNESDAY: 3,
        THIRD: 3,
        MARCH: 3,
        THURSDAY: 4,
        FOURTH: 4,
        APRIL: 4,
        FRIDAY: 5,
        FIFTH: 5,
        MAY: 5,
        SATURDAY: 6,
        JUNE: 6,
        JULY: 7,
        AUGUST: 8,
        SEPTEMBER: 9,
        OCTOBER: 10,
        NOVEMBER: 11,
        DECEMBER: 12,
      }

    # Convert date tokens to int representations of properties.
    def ValueOf(self, token_type):
      return self.valuesDict.get(token_type, -1)




    # $ANTLR start "timespec"
    # borg/borgcron/py/Groc.g:92:1: timespec : ( specifictime | interval ) EOF ;
    def timespec(self, ):

        try:
            try:
                # borg/borgcron/py/Groc.g:93:3: ( ( specifictime | interval ) EOF )
                # borg/borgcron/py/Groc.g:93:5: ( specifictime | interval ) EOF
                pass
                # borg/borgcron/py/Groc.g:93:5: ( specifictime | interval )
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if (LA1_0 == EVERY) :
                    LA1_1 = self.input.LA(2)

                    if ((DIGIT <= LA1_1 <= DIGITS)) :
                        alt1 = 2
                    elif ((DAY <= LA1_1 <= SUNDAY)) :
                        alt1 = 1
                    else:
                        nvae = NoViableAltException("", 1, 1, self.input)

                        raise nvae

                elif ((DIGIT <= LA1_0 <= DIGITS) or (FIRST <= LA1_0 <= FOURTH_OR_FIFTH)) :
                    alt1 = 1
                else:
                    nvae = NoViableAltException("", 1, 0, self.input)

                    raise nvae

                if alt1 == 1:
                    # borg/borgcron/py/Groc.g:93:7: specifictime
                    pass
                    self._state.following.append(self.FOLLOW_specifictime_in_timespec44)
                    self.specifictime()

                    self._state.following.pop()


                elif alt1 == 2:
                    # borg/borgcron/py/Groc.g:93:22: interval
                    pass
                    self._state.following.append(self.FOLLOW_interval_in_timespec48)
                    self.interval()

                    self._state.following.pop()



                self.match(self.input, EOF, self.FOLLOW_EOF_in_timespec52)




            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "timespec"


    # $ANTLR start "specifictime"
    # borg/borgcron/py/Groc.g:96:1: specifictime : ( ( ( ( ( ordinals weekdays ) | monthdays ) OF ( monthspec | quarterspec ) ) | ( ordinals weekdays ) ) TIME ) ;
    def specifictime(self, ):

        TIME1 = None

        try:
            try:
                # borg/borgcron/py/Groc.g:97:3: ( ( ( ( ( ( ordinals weekdays ) | monthdays ) OF ( monthspec | quarterspec ) ) | ( ordinals weekdays ) ) TIME ) )
                # borg/borgcron/py/Groc.g:97:5: ( ( ( ( ( ordinals weekdays ) | monthdays ) OF ( monthspec | quarterspec ) ) | ( ordinals weekdays ) ) TIME )
                pass
                # borg/borgcron/py/Groc.g:97:5: ( ( ( ( ( ordinals weekdays ) | monthdays ) OF ( monthspec | quarterspec ) ) | ( ordinals weekdays ) ) TIME )
                # borg/borgcron/py/Groc.g:97:7: ( ( ( ( ordinals weekdays ) | monthdays ) OF ( monthspec | quarterspec ) ) | ( ordinals weekdays ) ) TIME
                pass
                # borg/borgcron/py/Groc.g:97:7: ( ( ( ( ordinals weekdays ) | monthdays ) OF ( monthspec | quarterspec ) ) | ( ordinals weekdays ) )
                alt4 = 2
                alt4 = self.dfa4.predict(self.input)
                if alt4 == 1:
                    # borg/borgcron/py/Groc.g:97:8: ( ( ( ordinals weekdays ) | monthdays ) OF ( monthspec | quarterspec ) )
                    pass
                    # borg/borgcron/py/Groc.g:97:8: ( ( ( ordinals weekdays ) | monthdays ) OF ( monthspec | quarterspec ) )
                    # borg/borgcron/py/Groc.g:97:10: ( ( ordinals weekdays ) | monthdays ) OF ( monthspec | quarterspec )
                    pass
                    # borg/borgcron/py/Groc.g:97:10: ( ( ordinals weekdays ) | monthdays )
                    alt2 = 2
                    LA2_0 = self.input.LA(1)

                    if (LA2_0 == EVERY or (FIRST <= LA2_0 <= FOURTH_OR_FIFTH)) :
                        alt2 = 1
                    elif ((DIGIT <= LA2_0 <= DIGITS)) :
                        alt2 = 2
                    else:
                        nvae = NoViableAltException("", 2, 0, self.input)

                        raise nvae

                    if alt2 == 1:
                        # borg/borgcron/py/Groc.g:97:11: ( ordinals weekdays )
                        pass
                        # borg/borgcron/py/Groc.g:97:11: ( ordinals weekdays )
                        # borg/borgcron/py/Groc.g:97:12: ordinals weekdays
                        pass
                        self._state.following.append(self.FOLLOW_ordinals_in_specifictime72)
                        self.ordinals()

                        self._state.following.pop()
                        self._state.following.append(self.FOLLOW_weekdays_in_specifictime74)
                        self.weekdays()

                        self._state.following.pop()





                    elif alt2 == 2:
                        # borg/borgcron/py/Groc.g:97:31: monthdays
                        pass
                        self._state.following.append(self.FOLLOW_monthdays_in_specifictime77)
                        self.monthdays()

                        self._state.following.pop()



                    self.match(self.input, OF, self.FOLLOW_OF_in_specifictime80)
                    # borg/borgcron/py/Groc.g:97:45: ( monthspec | quarterspec )
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if ((MONTH <= LA3_0 <= DECEMBER)) :
                        alt3 = 1
                    elif ((FIRST <= LA3_0 <= THIRD) or LA3_0 == QUARTER) :
                        alt3 = 2
                    else:
                        nvae = NoViableAltException("", 3, 0, self.input)

                        raise nvae

                    if alt3 == 1:
                        # borg/borgcron/py/Groc.g:97:46: monthspec
                        pass
                        self._state.following.append(self.FOLLOW_monthspec_in_specifictime83)
                        self.monthspec()

                        self._state.following.pop()


                    elif alt3 == 2:
                        # borg/borgcron/py/Groc.g:97:56: quarterspec
                        pass
                        self._state.following.append(self.FOLLOW_quarterspec_in_specifictime85)
                        self.quarterspec()

                        self._state.following.pop()








                elif alt4 == 2:
                    # borg/borgcron/py/Groc.g:98:11: ( ordinals weekdays )
                    pass
                    # borg/borgcron/py/Groc.g:98:11: ( ordinals weekdays )
                    # borg/borgcron/py/Groc.g:98:12: ordinals weekdays
                    pass
                    self._state.following.append(self.FOLLOW_ordinals_in_specifictime101)
                    self.ordinals()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_weekdays_in_specifictime103)
                    self.weekdays()

                    self._state.following.pop()
                    #action start
                    self.month_set = set(range(1,13))
                    #action end






                TIME1=self.match(self.input, TIME, self.FOLLOW_TIME_in_specifictime117)
                #action start
                self.time_string = TIME1.text
                #action end







            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "specifictime"


    # $ANTLR start "interval"
    # borg/borgcron/py/Groc.g:102:1: interval : ( EVERY intervalnum= ( DIGIT | DIGITS ) period ( time_range | ( SYNCHRONIZED ) )? ) ;
    def interval(self, ):

        intervalnum = None
        period2 = None


        try:
            try:
                # borg/borgcron/py/Groc.g:103:3: ( ( EVERY intervalnum= ( DIGIT | DIGITS ) period ( time_range | ( SYNCHRONIZED ) )? ) )
                # borg/borgcron/py/Groc.g:103:5: ( EVERY intervalnum= ( DIGIT | DIGITS ) period ( time_range | ( SYNCHRONIZED ) )? )
                pass
                # borg/borgcron/py/Groc.g:103:5: ( EVERY intervalnum= ( DIGIT | DIGITS ) period ( time_range | ( SYNCHRONIZED ) )? )
                # borg/borgcron/py/Groc.g:103:7: EVERY intervalnum= ( DIGIT | DIGITS ) period ( time_range | ( SYNCHRONIZED ) )?
                pass
                self.match(self.input, EVERY, self.FOLLOW_EVERY_in_interval136)
                intervalnum = self.input.LT(1)
                if (DIGIT <= self.input.LA(1) <= DIGITS):
                    self.input.consume()
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                #action start

                self.interval_mins = int(intervalnum.text)

                #action end
                self._state.following.append(self.FOLLOW_period_in_interval164)
                period2 = self.period()

                self._state.following.pop()
                #action start

                if ((period2 is not None) and [self.input.toString(period2.start,period2.stop)] or [None])[0] == "hours":
                  self.period_string = "hours"
                else:
                  self.period_string = "minutes"

                #action end
                # borg/borgcron/py/Groc.g:113:7: ( time_range | ( SYNCHRONIZED ) )?
                alt5 = 3
                LA5_0 = self.input.LA(1)

                if (LA5_0 == FROM) :
                    alt5 = 1
                elif (LA5_0 == SYNCHRONIZED) :
                    alt5 = 2
                if alt5 == 1:
                    # borg/borgcron/py/Groc.g:113:9: time_range
                    pass
                    self._state.following.append(self.FOLLOW_time_range_in_interval176)
                    self.time_range()

                    self._state.following.pop()


                elif alt5 == 2:
                    # borg/borgcron/py/Groc.g:114:9: ( SYNCHRONIZED )
                    pass
                    # borg/borgcron/py/Groc.g:114:9: ( SYNCHRONIZED )
                    # borg/borgcron/py/Groc.g:114:10: SYNCHRONIZED
                    pass
                    self.match(self.input, SYNCHRONIZED, self.FOLLOW_SYNCHRONIZED_in_interval189)
                    #action start
                    self.synchronized = True
                    #action end













            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "interval"


    # $ANTLR start "ordinals"
    # borg/borgcron/py/Groc.g:118:1: ordinals : ( EVERY | ( ordinal ( COMMA ordinal )* ) ) ;
    def ordinals(self, ):

        try:
            try:
                # borg/borgcron/py/Groc.g:119:3: ( ( EVERY | ( ordinal ( COMMA ordinal )* ) ) )
                # borg/borgcron/py/Groc.g:119:5: ( EVERY | ( ordinal ( COMMA ordinal )* ) )
                pass
                # borg/borgcron/py/Groc.g:119:5: ( EVERY | ( ordinal ( COMMA ordinal )* ) )
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if (LA7_0 == EVERY) :
                    alt7 = 1
                elif ((FIRST <= LA7_0 <= FOURTH_OR_FIFTH)) :
                    alt7 = 2
                else:
                    nvae = NoViableAltException("", 7, 0, self.input)

                    raise nvae

                if alt7 == 1:
                    # borg/borgcron/py/Groc.g:119:7: EVERY
                    pass
                    self.match(self.input, EVERY, self.FOLLOW_EVERY_in_ordinals218)


                elif alt7 == 2:
                    # borg/borgcron/py/Groc.g:120:5: ( ordinal ( COMMA ordinal )* )
                    pass
                    # borg/borgcron/py/Groc.g:120:5: ( ordinal ( COMMA ordinal )* )
                    # borg/borgcron/py/Groc.g:120:7: ordinal ( COMMA ordinal )*
                    pass
                    self._state.following.append(self.FOLLOW_ordinal_in_ordinals226)
                    self.ordinal()

                    self._state.following.pop()
                    # borg/borgcron/py/Groc.g:120:15: ( COMMA ordinal )*
                    while True: #loop6
                        alt6 = 2
                        LA6_0 = self.input.LA(1)

                        if (LA6_0 == COMMA) :
                            alt6 = 1


                        if alt6 == 1:
                            # borg/borgcron/py/Groc.g:120:16: COMMA ordinal
                            pass
                            self.match(self.input, COMMA, self.FOLLOW_COMMA_in_ordinals229)
                            self._state.following.append(self.FOLLOW_ordinal_in_ordinals231)
                            self.ordinal()

                            self._state.following.pop()


                        else:
                            break #loop6












            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "ordinals"


    # $ANTLR start "ordinal"
    # borg/borgcron/py/Groc.g:123:1: ordinal : ord= ( FIRST | SECOND | THIRD | FOURTH | FIFTH | FOURTH_OR_FIFTH ) ;
    def ordinal(self, ):

        ord = None

        try:
            try:
                # borg/borgcron/py/Groc.g:124:3: (ord= ( FIRST | SECOND | THIRD | FOURTH | FIFTH | FOURTH_OR_FIFTH ) )
                # borg/borgcron/py/Groc.g:124:5: ord= ( FIRST | SECOND | THIRD | FOURTH | FIFTH | FOURTH_OR_FIFTH )
                pass
                ord = self.input.LT(1)
                if (FIRST <= self.input.LA(1) <= FOURTH_OR_FIFTH):
                    self.input.consume()
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                #action start

                self.ordinal_set.add(self.ValueOf(ord.type));

                #action end




            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "ordinal"

    class period_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)





    # $ANTLR start "period"
    # borg/borgcron/py/Groc.g:129:1: period : ( HOURS | MINUTES ) ;
    def period(self, ):

        retval = self.period_return()
        retval.start = self.input.LT(1)

        try:
            try:
                # borg/borgcron/py/Groc.g:130:3: ( ( HOURS | MINUTES ) )
                # borg/borgcron/py/Groc.g:130:5: ( HOURS | MINUTES )
                pass
                if (HOURS <= self.input.LA(1) <= MINUTES):
                    self.input.consume()
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end "period"


    # $ANTLR start "monthdays"
    # borg/borgcron/py/Groc.g:133:1: monthdays : ( monthday ( COMMA monthday )* ) ;
    def monthdays(self, ):

        try:
            try:
                # borg/borgcron/py/Groc.g:134:3: ( ( monthday ( COMMA monthday )* ) )
                # borg/borgcron/py/Groc.g:134:5: ( monthday ( COMMA monthday )* )
                pass
                # borg/borgcron/py/Groc.g:134:5: ( monthday ( COMMA monthday )* )
                # borg/borgcron/py/Groc.g:134:7: monthday ( COMMA monthday )*
                pass
                self._state.following.append(self.FOLLOW_monthday_in_monthdays314)
                self.monthday()

                self._state.following.pop()
                # borg/borgcron/py/Groc.g:134:16: ( COMMA monthday )*
                while True: #loop8
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == COMMA) :
                        alt8 = 1


                    if alt8 == 1:
                        # borg/borgcron/py/Groc.g:134:18: COMMA monthday
                        pass
                        self.match(self.input, COMMA, self.FOLLOW_COMMA_in_monthdays318)
                        self._state.following.append(self.FOLLOW_monthday_in_monthdays320)
                        self.monthday()

                        self._state.following.pop()


                    else:
                        break #loop8









            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "monthdays"


    # $ANTLR start "monthday"
    # borg/borgcron/py/Groc.g:137:1: monthday : day= ( DIGIT | DIGITS ) ;
    def monthday(self, ):

        day = None

        try:
            try:
                # borg/borgcron/py/Groc.g:138:3: (day= ( DIGIT | DIGITS ) )
                # borg/borgcron/py/Groc.g:138:5: day= ( DIGIT | DIGITS )
                pass
                day = self.input.LT(1)
                if (DIGIT <= self.input.LA(1) <= DIGITS):
                    self.input.consume()
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                #action start

                self.monthday_set.add(int(day.text));
                #action end




            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "monthday"


    # $ANTLR start "weekdays"
    # borg/borgcron/py/Groc.g:142:1: weekdays : ( DAY | ( weekday ( COMMA weekday )* ) ) ;
    def weekdays(self, ):

        try:
            try:
                # borg/borgcron/py/Groc.g:143:3: ( ( DAY | ( weekday ( COMMA weekday )* ) ) )
                # borg/borgcron/py/Groc.g:143:5: ( DAY | ( weekday ( COMMA weekday )* ) )
                pass
                # borg/borgcron/py/Groc.g:143:5: ( DAY | ( weekday ( COMMA weekday )* ) )
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == DAY) :
                    alt10 = 1
                elif ((MONDAY <= LA10_0 <= SUNDAY)) :
                    alt10 = 2
                else:
                    nvae = NoViableAltException("", 10, 0, self.input)

                    raise nvae

                if alt10 == 1:
                    # borg/borgcron/py/Groc.g:143:7: DAY
                    pass
                    self.match(self.input, DAY, self.FOLLOW_DAY_in_weekdays365)
                    #action start

                    if self.ordinal_set:
                      # <ordinal> day means <ordinal> day of the month,
                      # not every day of the <ordinal> week.
                      self.monthday_set = self.ordinal_set
                      self.ordinal_set = set()
                    else:
                      self.ordinal_set = self.ordinal_set.union(allOrdinals)
                      self.weekday_set = set([self.ValueOf(SUNDAY), self.ValueOf(MONDAY),
                              self.ValueOf(TUESDAY), self.ValueOf(WEDNESDAY),
                              self.ValueOf(THURSDAY), self.ValueOf(FRIDAY),
                              self.ValueOf(SATURDAY), self.ValueOf(SUNDAY)])

                    #action end


                elif alt10 == 2:
                    # borg/borgcron/py/Groc.g:155:11: ( weekday ( COMMA weekday )* )
                    pass
                    # borg/borgcron/py/Groc.g:155:11: ( weekday ( COMMA weekday )* )
                    # borg/borgcron/py/Groc.g:155:13: weekday ( COMMA weekday )*
                    pass
                    self._state.following.append(self.FOLLOW_weekday_in_weekdays373)
                    self.weekday()

                    self._state.following.pop()
                    # borg/borgcron/py/Groc.g:155:21: ( COMMA weekday )*
                    while True: #loop9
                        alt9 = 2
                        LA9_0 = self.input.LA(1)

                        if (LA9_0 == COMMA) :
                            alt9 = 1


                        if alt9 == 1:
                            # borg/borgcron/py/Groc.g:155:22: COMMA weekday
                            pass
                            self.match(self.input, COMMA, self.FOLLOW_COMMA_in_weekdays376)
                            self._state.following.append(self.FOLLOW_weekday_in_weekdays378)
                            self.weekday()

                            self._state.following.pop()


                        else:
                            break #loop9


                    #action start

                    if not self.ordinal_set:
                      self.ordinal_set = self.ordinal_set.union(allOrdinals)

                    #action end










            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "weekdays"


    # $ANTLR start "weekday"
    # borg/borgcron/py/Groc.g:161:1: weekday : dayname= ( MONDAY | TUESDAY | WEDNESDAY | THURSDAY | FRIDAY | SATURDAY | SUNDAY ) ;
    def weekday(self, ):

        dayname = None

        try:
            try:
                # borg/borgcron/py/Groc.g:162:3: (dayname= ( MONDAY | TUESDAY | WEDNESDAY | THURSDAY | FRIDAY | SATURDAY | SUNDAY ) )
                # borg/borgcron/py/Groc.g:162:5: dayname= ( MONDAY | TUESDAY | WEDNESDAY | THURSDAY | FRIDAY | SATURDAY | SUNDAY )
                pass
                dayname = self.input.LT(1)
                if (MONDAY <= self.input.LA(1) <= SUNDAY):
                    self.input.consume()
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                #action start

                self.weekday_set.add(self.ValueOf(dayname.type))

                #action end




            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "weekday"


    # $ANTLR start "monthspec"
    # borg/borgcron/py/Groc.g:168:1: monthspec : ( MONTH | months ) ;
    def monthspec(self, ):

        try:
            try:
                # borg/borgcron/py/Groc.g:169:3: ( ( MONTH | months ) )
                # borg/borgcron/py/Groc.g:169:5: ( MONTH | months )
                pass
                # borg/borgcron/py/Groc.g:169:5: ( MONTH | months )
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == MONTH) :
                    alt11 = 1
                elif ((JANUARY <= LA11_0 <= DECEMBER)) :
                    alt11 = 2
                else:
                    nvae = NoViableAltException("", 11, 0, self.input)

                    raise nvae

                if alt11 == 1:
                    # borg/borgcron/py/Groc.g:169:7: MONTH
                    pass
                    self.match(self.input, MONTH, self.FOLLOW_MONTH_in_monthspec459)
                    #action start

                    self.month_set = self.month_set.union(set([
                        self.ValueOf(JANUARY), self.ValueOf(FEBRUARY), self.ValueOf(MARCH),
                        self.ValueOf(APRIL), self.ValueOf(MAY), self.ValueOf(JUNE),
                        self.ValueOf(JULY), self.ValueOf(AUGUST), self.ValueOf(SEPTEMBER),
                        self.ValueOf(OCTOBER), self.ValueOf(NOVEMBER),
                        self.ValueOf(DECEMBER)]))

                    #action end


                elif alt11 == 2:
                    # borg/borgcron/py/Groc.g:177:7: months
                    pass
                    self._state.following.append(self.FOLLOW_months_in_monthspec469)
                    self.months()

                    self._state.following.pop()







            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "monthspec"


    # $ANTLR start "months"
    # borg/borgcron/py/Groc.g:180:1: months : ( month ( COMMA month )* ) ;
    def months(self, ):

        try:
            try:
                # borg/borgcron/py/Groc.g:181:3: ( ( month ( COMMA month )* ) )
                # borg/borgcron/py/Groc.g:181:5: ( month ( COMMA month )* )
                pass
                # borg/borgcron/py/Groc.g:181:5: ( month ( COMMA month )* )
                # borg/borgcron/py/Groc.g:181:7: month ( COMMA month )*
                pass
                self._state.following.append(self.FOLLOW_month_in_months486)
                self.month()

                self._state.following.pop()
                # borg/borgcron/py/Groc.g:181:13: ( COMMA month )*
                while True: #loop12
                    alt12 = 2
                    LA12_0 = self.input.LA(1)

                    if (LA12_0 == COMMA) :
                        alt12 = 1


                    if alt12 == 1:
                        # borg/borgcron/py/Groc.g:181:14: COMMA month
                        pass
                        self.match(self.input, COMMA, self.FOLLOW_COMMA_in_months489)
                        self._state.following.append(self.FOLLOW_month_in_months491)
                        self.month()

                        self._state.following.pop()


                    else:
                        break #loop12









            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "months"


    # $ANTLR start "month"
    # borg/borgcron/py/Groc.g:184:1: month : monthname= ( JANUARY | FEBRUARY | MARCH | APRIL | MAY | JUNE | JULY | AUGUST | SEPTEMBER | OCTOBER | NOVEMBER | DECEMBER ) ;
    def month(self, ):

        monthname = None

        try:
            try:
                # borg/borgcron/py/Groc.g:185:3: (monthname= ( JANUARY | FEBRUARY | MARCH | APRIL | MAY | JUNE | JULY | AUGUST | SEPTEMBER | OCTOBER | NOVEMBER | DECEMBER ) )
                # borg/borgcron/py/Groc.g:185:5: monthname= ( JANUARY | FEBRUARY | MARCH | APRIL | MAY | JUNE | JULY | AUGUST | SEPTEMBER | OCTOBER | NOVEMBER | DECEMBER )
                pass
                monthname = self.input.LT(1)
                if (JANUARY <= self.input.LA(1) <= DECEMBER):
                    self.input.consume()
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                #action start
                self.month_set.add(self.ValueOf(monthname.type));
                #action end




            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "month"


    # $ANTLR start "quarterspec"
    # borg/borgcron/py/Groc.g:190:1: quarterspec : ( QUARTER | ( quarter_ordinals MONTH OF QUARTER ) ) ;
    def quarterspec(self, ):

        try:
            try:
                # borg/borgcron/py/Groc.g:191:3: ( ( QUARTER | ( quarter_ordinals MONTH OF QUARTER ) ) )
                # borg/borgcron/py/Groc.g:191:5: ( QUARTER | ( quarter_ordinals MONTH OF QUARTER ) )
                pass
                # borg/borgcron/py/Groc.g:191:5: ( QUARTER | ( quarter_ordinals MONTH OF QUARTER ) )
                alt13 = 2
                LA13_0 = self.input.LA(1)

                if (LA13_0 == QUARTER) :
                    alt13 = 1
                elif ((FIRST <= LA13_0 <= THIRD)) :
                    alt13 = 2
                else:
                    nvae = NoViableAltException("", 13, 0, self.input)

                    raise nvae

                if alt13 == 1:
                    # borg/borgcron/py/Groc.g:191:7: QUARTER
                    pass
                    self.match(self.input, QUARTER, self.FOLLOW_QUARTER_in_quarterspec583)
                    #action start

                    self.month_set = self.month_set.union(set([
                        self.ValueOf(JANUARY), self.ValueOf(APRIL), self.ValueOf(JULY),
                        self.ValueOf(OCTOBER)]))
                    #action end


                elif alt13 == 2:
                    # borg/borgcron/py/Groc.g:195:7: ( quarter_ordinals MONTH OF QUARTER )
                    pass
                    # borg/borgcron/py/Groc.g:195:7: ( quarter_ordinals MONTH OF QUARTER )
                    # borg/borgcron/py/Groc.g:195:9: quarter_ordinals MONTH OF QUARTER
                    pass
                    self._state.following.append(self.FOLLOW_quarter_ordinals_in_quarterspec595)
                    self.quarter_ordinals()

                    self._state.following.pop()
                    self.match(self.input, MONTH, self.FOLLOW_MONTH_in_quarterspec597)
                    self.match(self.input, OF, self.FOLLOW_OF_in_quarterspec599)
                    self.match(self.input, QUARTER, self.FOLLOW_QUARTER_in_quarterspec601)










            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "quarterspec"


    # $ANTLR start "quarter_ordinals"
    # borg/borgcron/py/Groc.g:198:1: quarter_ordinals : ( month_of_quarter_ordinal ( COMMA month_of_quarter_ordinal )* ) ;
    def quarter_ordinals(self, ):

        try:
            try:
                # borg/borgcron/py/Groc.g:199:3: ( ( month_of_quarter_ordinal ( COMMA month_of_quarter_ordinal )* ) )
                # borg/borgcron/py/Groc.g:199:5: ( month_of_quarter_ordinal ( COMMA month_of_quarter_ordinal )* )
                pass
                # borg/borgcron/py/Groc.g:199:5: ( month_of_quarter_ordinal ( COMMA month_of_quarter_ordinal )* )
                # borg/borgcron/py/Groc.g:199:7: month_of_quarter_ordinal ( COMMA month_of_quarter_ordinal )*
                pass
                self._state.following.append(self.FOLLOW_month_of_quarter_ordinal_in_quarter_ordinals620)
                self.month_of_quarter_ordinal()

                self._state.following.pop()
                # borg/borgcron/py/Groc.g:199:32: ( COMMA month_of_quarter_ordinal )*
                while True: #loop14
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == COMMA) :
                        alt14 = 1


                    if alt14 == 1:
                        # borg/borgcron/py/Groc.g:199:33: COMMA month_of_quarter_ordinal
                        pass
                        self.match(self.input, COMMA, self.FOLLOW_COMMA_in_quarter_ordinals623)
                        self._state.following.append(self.FOLLOW_month_of_quarter_ordinal_in_quarter_ordinals625)
                        self.month_of_quarter_ordinal()

                        self._state.following.pop()


                    else:
                        break #loop14









            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "quarter_ordinals"


    # $ANTLR start "month_of_quarter_ordinal"
    # borg/borgcron/py/Groc.g:202:1: month_of_quarter_ordinal : offset= ( FIRST | SECOND | THIRD ) ;
    def month_of_quarter_ordinal(self, ):

        offset = None

        try:
            try:
                # borg/borgcron/py/Groc.g:203:3: (offset= ( FIRST | SECOND | THIRD ) )
                # borg/borgcron/py/Groc.g:203:5: offset= ( FIRST | SECOND | THIRD )
                pass
                offset = self.input.LT(1)
                if (FIRST <= self.input.LA(1) <= THIRD):
                    self.input.consume()
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                #action start

                jOffset = self.ValueOf(offset.type) - 1
                self.month_set = self.month_set.union(set([
                    jOffset + self.ValueOf(JANUARY), jOffset + self.ValueOf(APRIL),
                    jOffset + self.ValueOf(JULY), jOffset + self.ValueOf(OCTOBER)]))
                #action end




            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "month_of_quarter_ordinal"


    # $ANTLR start "time_range"
    # borg/borgcron/py/Groc.g:210:1: time_range : ( FROM (start_time= TIME ) TO (end_time= TIME ) ) ;
    def time_range(self, ):

        start_time = None
        end_time = None

        try:
            try:
                # borg/borgcron/py/Groc.g:211:3: ( ( FROM (start_time= TIME ) TO (end_time= TIME ) ) )
                # borg/borgcron/py/Groc.g:211:5: ( FROM (start_time= TIME ) TO (end_time= TIME ) )
                pass
                # borg/borgcron/py/Groc.g:211:5: ( FROM (start_time= TIME ) TO (end_time= TIME ) )
                # borg/borgcron/py/Groc.g:211:7: FROM (start_time= TIME ) TO (end_time= TIME )
                pass
                self.match(self.input, FROM, self.FOLLOW_FROM_in_time_range673)
                # borg/borgcron/py/Groc.g:211:12: (start_time= TIME )
                # borg/borgcron/py/Groc.g:211:13: start_time= TIME
                pass
                start_time=self.match(self.input, TIME, self.FOLLOW_TIME_in_time_range680)
                #action start
                self.start_time_string = start_time.text
                #action end



                self.match(self.input, TO, self.FOLLOW_TO_in_time_range691)
                # borg/borgcron/py/Groc.g:212:10: (end_time= TIME )
                # borg/borgcron/py/Groc.g:212:11: end_time= TIME
                pass
                end_time=self.match(self.input, TIME, self.FOLLOW_TIME_in_time_range698)
                #action start
                self.end_time_string = end_time.text
                #action end










            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "time_range"


    # Delegated rules


    # lookup tables for DFA #4

    DFA4_eot = DFA.unpack(
        u"\13\uffff"
        )

    DFA4_eof = DFA.unpack(
        u"\13\uffff"
        )

    DFA4_min = DFA.unpack(
        u"\1\6\1\23\1\12\1\uffff\2\4\1\13\1\uffff\1\24\1\12\1\4"
        )

    DFA4_max = DFA.unpack(
        u"\1\20\2\32\1\uffff\1\5\1\12\1\20\1\uffff\2\32\1\12"
        )

    DFA4_accept = DFA.unpack(
        u"\3\uffff\1\1\3\uffff\1\2\3\uffff"
        )

    DFA4_special = DFA.unpack(
        u"\13\uffff"
        )


    DFA4_transition = [
        DFA.unpack(u"\1\1\2\3\2\uffff\6\2"),
        DFA.unpack(u"\1\4\7\5"),
        DFA.unpack(u"\1\6\10\uffff\1\4\7\5"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\3\1\7"),
        DFA.unpack(u"\1\3\1\7\4\uffff\1\10"),
        DFA.unpack(u"\6\11"),
        DFA.unpack(u""),
        DFA.unpack(u"\7\12"),
        DFA.unpack(u"\1\6\10\uffff\1\4\7\5"),
        DFA.unpack(u"\1\3\1\7\4\uffff\1\10")
    ]

    # class definition for DFA #4

    DFA4 = DFA


    FOLLOW_specifictime_in_timespec44 = frozenset([])
    FOLLOW_interval_in_timespec48 = frozenset([])
    FOLLOW_EOF_in_timespec52 = frozenset([1])
    FOLLOW_ordinals_in_specifictime72 = frozenset([19, 20, 21, 22, 23, 24, 25, 26])
    FOLLOW_weekdays_in_specifictime74 = frozenset([4])
    FOLLOW_monthdays_in_specifictime77 = frozenset([4])
    FOLLOW_OF_in_specifictime80 = frozenset([11, 12, 13, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
    FOLLOW_monthspec_in_specifictime83 = frozenset([5])
    FOLLOW_quarterspec_in_specifictime85 = frozenset([5])
    FOLLOW_ordinals_in_specifictime101 = frozenset([19, 20, 21, 22, 23, 24, 25, 26])
    FOLLOW_weekdays_in_specifictime103 = frozenset([5])
    FOLLOW_TIME_in_specifictime117 = frozenset([1])
    FOLLOW_EVERY_in_interval136 = frozenset([7, 8])
    FOLLOW_set_in_interval146 = frozenset([17, 18])
    FOLLOW_period_in_interval164 = frozenset([1, 9, 41])
    FOLLOW_time_range_in_interval176 = frozenset([1])
    FOLLOW_SYNCHRONIZED_in_interval189 = frozenset([1])
    FOLLOW_EVERY_in_ordinals218 = frozenset([1])
    FOLLOW_ordinal_in_ordinals226 = frozenset([1, 10])
    FOLLOW_COMMA_in_ordinals229 = frozenset([11, 12, 13, 14, 15, 16])
    FOLLOW_ordinal_in_ordinals231 = frozenset([1, 10])
    FOLLOW_set_in_ordinal252 = frozenset([1])
    FOLLOW_set_in_period291 = frozenset([1])
    FOLLOW_monthday_in_monthdays314 = frozenset([1, 10])
    FOLLOW_COMMA_in_monthdays318 = frozenset([7, 8])
    FOLLOW_monthday_in_monthdays320 = frozenset([1, 10])
    FOLLOW_set_in_monthday340 = frozenset([1])
    FOLLOW_DAY_in_weekdays365 = frozenset([1])
    FOLLOW_weekday_in_weekdays373 = frozenset([1, 10])
    FOLLOW_COMMA_in_weekdays376 = frozenset([19, 20, 21, 22, 23, 24, 25, 26])
    FOLLOW_weekday_in_weekdays378 = frozenset([1, 10])
    FOLLOW_set_in_weekday400 = frozenset([1])
    FOLLOW_MONTH_in_monthspec459 = frozenset([1])
    FOLLOW_months_in_monthspec469 = frozenset([1])
    FOLLOW_month_in_months486 = frozenset([1, 10])
    FOLLOW_COMMA_in_months489 = frozenset([27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39])
    FOLLOW_month_in_months491 = frozenset([1, 10])
    FOLLOW_set_in_month510 = frozenset([1])
    FOLLOW_QUARTER_in_quarterspec583 = frozenset([1])
    FOLLOW_quarter_ordinals_in_quarterspec595 = frozenset([27])
    FOLLOW_MONTH_in_quarterspec597 = frozenset([4])
    FOLLOW_OF_in_quarterspec599 = frozenset([40])
    FOLLOW_QUARTER_in_quarterspec601 = frozenset([1])
    FOLLOW_month_of_quarter_ordinal_in_quarter_ordinals620 = frozenset([1, 10])
    FOLLOW_COMMA_in_quarter_ordinals623 = frozenset([11, 12, 13, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
    FOLLOW_month_of_quarter_ordinal_in_quarter_ordinals625 = frozenset([1, 10])
    FOLLOW_set_in_month_of_quarter_ordinal644 = frozenset([1])
    FOLLOW_FROM_in_time_range673 = frozenset([5])
    FOLLOW_TIME_in_time_range680 = frozenset([42])
    FOLLOW_TO_in_time_range691 = frozenset([5])
    FOLLOW_TIME_in_time_range698 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("GrocLexer", GrocParser)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)
