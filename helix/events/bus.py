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

import logging
import Queue
import threading


LOG = logging.getLogger(__name__)


class Eventbus(object):

    def __init__(self):
        super(Eventbus, self).__init__()
        self._event_queue = Queue.Queue()
        self._subscribers = {}
        self._subscribers_lock = threading.RLock()

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

    def fire(self, event):
        if event:
            self._event_queue.put(event)

    def is_empty(self):
        return self._event_queue.empty()

    def process_events(self):
        # process events
        while True:
            try:
                event = self._event_queue.get_nowait()
                for callback in self._subscribers.get(type(event), []):
                    callback(event=event)
            except Queue.Empty:
                break
            except Exception:
                LOG.exception("Opsss!!! Can't process event %s", event)
