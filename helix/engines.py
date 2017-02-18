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

import abc
import logging
import Queue
import threading
import time

import six


from helix.dm import events
from helix.events import base


class OnStartEngine(base.Event):
    pass


class OnStopEngine(base.Event):
    pass


LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class AbstractGroupOfInstruments(object):

    def __init__(self, instruments):
        super(AbstractGroupOfInstruments, self).__init__()
        self._instruments = instruments

    def get_current_timestamp(self):
        return time.time()

    @abc.abstractmethod
    def on_loop(self, engine):
        raise NotImplementedError()

    def __iter__(self):
        return iter(self._instruments)


class GroupOfHistoricalInstruments(AbstractGroupOfInstruments):

    def _select_instrument(self):
        target_instrument = None
        next_tick_time = float("inf")
        for instrument in self._instruments:
            if instrument.get_next_tick_info().timestamp < next_tick_time:
                target_instrument = instrument
        return target_instrument

    def get_current_timestamp(self):
        target_instrument = self._select_instrument()
        return target_instrument.get_next_tick_info().timestamp

    def on_loop(self, engine):
        target_instrument = self._select_instrument()
        target_instrument.on_loop(engine)


class EventEngine(threading.Thread):
    """Event engine

        parameters:

        :param instruments: - Instance of AbstractGroupOfInstruments child
        """

    def __init__(self, instruments):
        super(EventEngine, self).__init__()
        self._event_queue = Queue.Queue()
        self._market_timestamp = 0
        self._instruments = instruments
        self._set_market_timestamp(instruments.get_current_timestamp())
        self._idle_timeout = 10
        self._subscribers = {}
        self._subscribers_lock = threading.RLock()
        self.subscribe(OnStopEngine, self._stop_event_handler)
        self.subscribe(events.OnTickEvent, self._set_market_timestamp_handler)
        self._stop = False

    def subscribe(self, event_type, callback):
        self._subscribers_lock.acquire()
        try:
            callback_list = self._subscribers.get(event_type, [])
            callback_list.append(callback)
            self._subscribers[event_type] = callback_list
        finally:
            self._subscribers_lock.release()

    def unsubscribe(self, event_type, callback):
        self._subscribers_lock.acquire()
        try:
            callback_list = self._subscribers.get(event_type, [])
            if callback in callback_list:
                callback_list.remove(callback)
            self._subscribers[event_type] = callback_list
            if len(callback_list) == 0:
                del self._subscribers[event_type]
        finally:
            self._subscribers_lock.release()

    def get_ide_timeout(self):
        return self._idle_timeout

    def set_idle_timeout(self, timeout):
        self._idle_timeout = timeout

    def get_market_timestamp(self):
        return self._market_timestamp

    def _set_market_timestamp(self, timestamp):
        if self._market_timestamp < timestamp:
            self._market_timestamp = timestamp

    def _set_market_timestamp_handler(self, engine, event):
        self._set_market_timestamp(event.get_tick().timestamp)

    def get_instruments(self):
        return self._instruments

    def get_instrument(self, name):
        for instrument in self._instruments:
            if instrument.name == name:
                return instrument
        raise ValueError("Instrument %s not found" % name)

    def fire(self, event):
        if event:
            self._event_queue.put(event)

    def run(self):
        self._event_queue.put(OnStartEngine())
        while not self._stop:
            # get new tick events
            self._instruments.on_loop(self)

            if self._event_queue.empty():
                time.sleep(self._idle_timeout)

            # process events
            while True:
                try:
                    event = self._event_queue.get_nowait()
                    for callback in self._subscribers.get(type(event), []):
                        callback(engine=self, event=event)
                except Queue.Empty:
                    break
                except Exception:
                    LOG.exception("Opsss!!! Can't process event %s", event)
        LOG.info("Engine stopped")

    def _stop_event_handler(self, engine, event):
        self._stop = True

    def stop(self):
        self.fire(OnStopEngine())
