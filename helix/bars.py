# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2015 Eugene Frolov <eugene@frolov.net.ru>
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


class Tick(object):

    def __init__(self, datetime, instrument, ask, bid, ask_volume,
                 bid_volume):
        self.instrument = instrument
        self.ask = float(ask)
        self.bid = float(bid)
        self.ask_volume = float(ask_volume)
        self.bid_volume = float(bid_volume)
        self.datetime = datetime

    def __str__(self):
        return "Tick dt: %s. %s: ask: %f, bid: %f, av: %f, bv: %f" % (
            self.datetime, self.instrument, self.ask, self.bid,
            self.ask_volume, self.bid_volume)
