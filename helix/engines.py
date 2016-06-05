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

from datetime import datetime
import logging
import threading

from helix import bars


LOG = logging.getLogger(__name__)


class TickFileStream(object):

    def __init__(self, file_path, instrument):
        self._file_path = file_path
        self._instrument = instrument
        self._fp = open(file_path, 'r')
        header = self._fp.readline()
        if header.strip() != "Time,Ask,Bid,AskVolume,BidVolume":
            raise TypeError("Incorrect DukasCopy Tick file. Header is '%s'"
                            % header.strip())

    def read(self):
        args = self._fp.readline().strip().split(',')
        if args:
            return bars.Tick(
                datetime=datetime.strptime(args[0], '%Y-%m-%d %H:%M:%S.%f'),
                instrument=self._instrument,
                ask=float(args[1]),
                bid=float(args[2]),
                ask_volume=float(args[3]),
                bid_volume=float(args[4]))
        return None


class Engine(threading.Thread):

    def __init__(self, strategy, tick_stream):
        super(Engine, self).__init__()
        self._strategy = strategy
        self._tick_stream = tick_stream
        self._stop = False

    def _read_next_tick(self):
        return self._tick_stream.read()

    def run(self):
        LOG.info("Starting strategy...")
        self._strategy.on_start(self)
        try:
            while not self._stop:
                tick = self._read_next_tick()
                if tick is None:
                    self.stop()
                    continue
                self._strategy.on_tick(tick)
        finally:
            LOG.info("Stopping strategy...")
            self._strategy.on_stop()

    def stop(self):
        LOG.info("Stopping engine...")
        self._stop = True
