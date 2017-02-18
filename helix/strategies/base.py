# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2015-2017 Eugene Frolov <eugene@frolov.net.ru>
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

import abc
import logging

import six


from helix.dm import events
from helix import engines


@six.add_metaclass(abc.ABCMeta)
class Strategy(object):

    def __init__(self, account):
        super(Strategy, self).__init__()
        self._log = logging.getLogger(__name__)
        self._account = account
        self._engine = account.get_engine()
        self._event_bus = self._engine.get_event_bus()
        self._event_bus.subscribe(engines.OnStartEngine,
                                  self._on_start_handler)
        self._event_bus.subscribe(engines.OnStopEngine,
                                  self._on_stop_handler)
        self._event_bus.subscribe(events.OnTickEvent,
                                  self._on_tick_handler)

    def _on_start_handler(self, event):
        self.on_start()

    def _on_stop_handler(self, event):
        self.on_stop()

    def _on_tick_handler(self, event):
        self.on_tick(tick=event.get_tick())

    @abc.abstractmethod
    def on_start(self):
        pass

    @abc.abstractmethod
    def on_stop(self):
        pass

    @abc.abstractmethod
    def on_tick(self, tick):
        pass
