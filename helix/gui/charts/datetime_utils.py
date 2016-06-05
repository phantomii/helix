# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2016 Eugene Frolov <eugene@frolov.net.ru>
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import calendar
import datetime
import math

import numpy


ONE_SEC = 1.0
FIVE_SECS = 5.0
FIFTEEN_SECS = 15.0
THIRTY_SECS = 30.0
ONE_MIN = 60.0
FIVE_MINS = 300.0
FIFTEEN_MINS = 900.0
THIRTY_MINS = 1800.0
ONE_HOUR = 3600.0
FOUR_HOURS = 14400.0
ONE_DAY = 86400.0
ONE_WEEK = 604800.0
ONE_MONTH = 2592000.0
ONE_YEAR = 30758400.0


ZERO = datetime.timedelta(0)


# A UTC class
class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()


def floor(timestamp, interval, tz=utc):
    dt = datetime.datetime.fromtimestamp(timestamp, tz=tz)
    if interval in [ONE_SEC, FIVE_SECS, FIFTEEN_SECS, THIRTY_SECS,
                    ONE_MIN, FIVE_MINS, FIFTEEN_MINS, THIRTY_MINS,
                    ONE_HOUR, FOUR_HOURS, ONE_DAY]:
        return math.floor(timestamp / interval) * interval
    elif interval == ONE_WEEK:
        near_day = dt - datetime.timedelta(days=dt.weekday(),
                                           hours=dt.hour,
                                           minutes=dt.minute,
                                           seconds=dt.second,
                                           milliseconds=dt.microsecond)
    elif interval == ONE_MONTH:
        near_day = datetime.datetime(year=dt.year,
                                     month=dt.month,
                                     day=1,
                                     tzinfo=tz)
    elif interval == ONE_YEAR:
        near_day = datetime.datetime(year=dt.year,
                                     month=1,
                                     day=1,
                                     tzinfo=tz)
    else:
        raise ValueError("Invalid interval value. Interval value is %s",
                         interval)
    return calendar.timegm(near_day.timetuple())


def inc_month(dt):
    if dt.month < 12:
        return dt.replace(month=dt.month + 1)
    return dt.replace(year=dt.year + 1, month=1)


def ceil(timestamp, interval, tz=utc):
    dt = datetime.datetime.fromtimestamp(timestamp, tz=tz)
    if interval in [ONE_SEC, FIVE_SECS, FIFTEEN_SECS, THIRTY_SECS,
                    ONE_MIN, FIVE_MINS, FIFTEEN_MINS, THIRTY_MINS,
                    ONE_HOUR, FOUR_HOURS, ONE_DAY]:
        return math.ceil(timestamp / interval) * interval
    elif interval == ONE_WEEK:
        near_day = (dt - datetime.timedelta(days=dt.weekday(),
                                            hours=dt.hour,
                                            minutes=dt.minute,
                                            seconds=dt.second,
                                            milliseconds=dt.microsecond) +
                    datetime.timedelta(days=7))
    elif interval == ONE_MONTH:
        near_day = inc_month(datetime.datetime(year=dt.year,
                                               month=dt.month,
                                               day=1,
                                               tzinfo=tz))
    elif interval == ONE_YEAR:
        near_day = datetime.datetime(year=dt.year + 1,
                                     month=1,
                                     day=1,
                                     tzinfo=tz)
    else:
        raise ValueError("Invalid interval value. Interval value is %s",
                         interval)
    return calendar.timegm(near_day.timetuple())


def drange(start_timestamp, end_timestamp, step, tz=utc):
    start = floor(start_timestamp, step)
    end = ceil(end_timestamp, step)

    start_dt = datetime.datetime.fromtimestamp(start, tz=tz)
    end_dt = datetime.datetime.fromtimestamp(end, tz=tz)

    if step in [ONE_SEC, FIVE_SECS, FIFTEEN_SECS, THIRTY_SECS,
                ONE_MIN, FIVE_MINS, FIFTEEN_MINS, THIRTY_MINS,
                ONE_HOUR, FOUR_HOURS, ONE_DAY, ONE_WEEK]:
        for value in numpy.arange(start, end, step):
            yield value
    elif step == ONE_MONTH:
        value = start_dt
        while (value < end_dt):
            yield calendar.timegm(value.timetuple())
            value = inc_month(value)
    elif step == ONE_YEAR:
        value = start_dt
        while (value < end_dt):
            yield calendar.timegm(value.timetuple())
            value = value.replace(year=value.year + 1)
    else:
        raise ValueError("Invalid interval value. Interval value is %s",
                         step)
