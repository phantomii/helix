# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2017 Eugene Frolov <eugene@frolov.net.ru>
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

from helix.dm import events as dm_events
from helix.market import positions


class Account(object):

    def __init__(self, engine, deposit, leverage=1):
        super(Account, self).__init__()
        self._engine = engine
        self._event_bus = engine.get_event_bus()
        self._deposit = deposit
        self._leverage = leverage
        self._positions = positions.PositionManager(
            event_bus=self._event_bus,
            instruments=engine.get_instruments())
        self._event_bus.subscribe(dm_events.OnTickEvent, self._on_tick_handler)

    def get_engine(self):
        return self._engine

    def _on_tick_handler(self, event):
        # TODO(efrolov): Should check margin level here
        pass

    def submit_order_positions(self, instrument, positions):
        # TODO(efrolov): Should check margin level here
        instrument.submit_order_positions(positions=positions)
