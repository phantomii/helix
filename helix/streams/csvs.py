# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2016-2017 Eugene Frolov <eugene@frolov.net.ru>
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

import csv
from datetime import datetime
import time

from helix.dm import models


class TickInfo(object):

    def __init__(self, timestamp, ask, bid, ask_volume, bid_volume):
        super(TickInfo, self).__init__()
        self._timestamp = timestamp
        self._ask = float(ask)
        self._bid = float(bid)
        self._ask_volume = float(ask_volume)
        self._bid_volume = float(bid_volume)

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def ask(self):
        return self._ask

    @property
    def bid(self):
        return self._bid

    @property
    def ask_volume(self):
        return self._ask_volume

    @property
    def bid_volume(self):
        return self._bid_volume


class TickStreamReader(object):

    def __init__(self, file_path):
        super(TickStreamReader, self).__init__()
        self._file_path = file_path
        self._fp = open(file_path, 'r')
        self._reader = csv.DictReader(self._fp)

    def stream(self):
        for record in self._reader:
            dt = datetime.strptime(record['time'] + " UTC",
                                   '%d.%m.%Y %H:%M:%S.%f %Z')
            timestamp = round(
                time.mktime(dt.timetuple()) + dt.microsecond / 1e6,
                3)
            yield TickInfo(timestamp=timestamp, ask=record['ask'],
                           bid=record['bid'], ask_volume=record['ask_volume'],
                           bid_volume=record['bid_volume'])

    def close(self):
        self._fp.close()
