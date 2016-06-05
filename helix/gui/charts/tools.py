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

import abc
from datetime import datetime
import logging
import math

import numpy
import six

from helix.gui.charts import datetime_utils as dutils
from helix.gui.charts import gobjects


LOG = logging.getLogger(__name__)


class LabelFormat(object):

    def __init__(self, label_format):
        self._label_format = label_format

    def get_label(self, value):
        return self._label_format % value


class TimeLabelFormat(LabelFormat):

    def __init__(self, short_label_format, full_label_format):
        super(TimeLabelFormat, self).__init__(short_label_format)
        self._full_label_format = full_label_format

    def get_label(self, value):
        return datetime.utcfromtimestamp(value).strftime(self._label_format)

    def get_full_label(self, value):
        return datetime.utcfromtimestamp(value).strftime(
            self._full_label_format)


class FormatChoiser(object):

    def __init__(self, axis):
        self._axis = axis

    def get_label(self, value):
        formater = self._axis._get_resolution_label_format()[
            self._axis.get_resolution()]
        return formater.get_label(value)

    def get_full_label(self, value):
        formater = self._axis._get_resolution_label_format()[
            self._axis.get_ex_resolution()]
        return formater.get_full_label(value)


@six.add_metaclass(abc.ABCMeta)
class Axis(object):

    @abc.abstractproperty
    def _resolution_set():
        raise NotImplementedError()

    @abc.abstractproperty
    def _min_size(self):
        raise NotImplementedError()

    @abc.abstractproperty
    def objects(self):
        raise NotImplementedError()

    def __init__(self, real_x0, real_x1, virtual_x0, virtual_x1,
                 label_format):
        self._virtual_x1_norm = 0
        self._label_format = label_format
        self.set_real_axis(real_x0, real_x1)
        self.set_virtual_axis(virtual_x0, virtual_x1)

    def set_real_axis(self, real_x0, real_x1):
        self._real_x0 = float(real_x0)
        self._real_x1 = float(real_x1)
        self._real_x0_norm = 0.0
        self._real_x1_norm = self._real_x1 - self._real_x0
        self._deliver = self._virtual_x1_norm / self._real_x1_norm

    def set_virtual_axis(self, virtual_x0, virtual_x1):
        self._virtual_x0 = float(virtual_x0)
        self._virtual_x1 = float(virtual_x1)
        self._virtual_x0_norm = 0.0
        self._virtual_x1_norm = self._virtual_x1 - self._virtual_x0
        self._deliver = self._virtual_x1_norm / self._real_x1_norm

    def _get_virtual_x_delta(self, real_x_delta):
        return (self.from_real_to_virtual(2) -
                self.from_real_to_virtual(1)) * real_x_delta

    def scale(self, real_x_delta):
        virtual_x_delta = self._get_virtual_x_delta(real_x_delta)
        self.set_virtual_axis(self._virtual_x0 - virtual_x_delta,
                              self._virtual_x1 + virtual_x_delta)

    def move(self, real_x_delta):
        virtual_x_delta = self._get_virtual_x_delta(real_x_delta)
        self.set_virtual_axis(self._virtual_x0 - virtual_x_delta,
                              self._virtual_x1 - virtual_x_delta)

    def get_resolution(self):
        for rvalue in self._resolution_set:
            x0 = self.from_virtual_to_real(self._virtual_x0)
            x1 = self.from_virtual_to_real(self._virtual_x0 + rvalue)
            if math.fabs(x1 - x0) > self._min_size:
                return rvalue
        return self._resolution_set[-1]

    def from_real_to_virtual(self, real_x):
        return real_x * self._deliver + self._virtual_x0

    def from_virtual_to_real(self, virtual_x):
        return (virtual_x - self._virtual_x0) / self._deliver

    def values(self):
        min_x = min(self._virtual_x0, self._virtual_x1)
        max_x = max(self._virtual_x0, self._virtual_x1)

        rvalue = self.get_resolution()

        start_x = math.floor(min_x / rvalue) * rvalue
        end_x = math.ceil(max_x / rvalue) * rvalue

        for value in numpy.arange(start_x, end_x, rvalue):
            yield (self.from_virtual_to_real(value),
                   self._label_format.get_label(value))

    @property
    def virtual_x0(self):
        return self._virtual_x0

    @property
    def virtual_x1(self):
        return self._virtual_x1

    @property
    def real_x0(self):
        return self._real_x0

    @property
    def real_x1(self):
        return self._real_x1


class PriceAxis(Axis):

    LINE_WIDTH = 10
    TEXT_START = 13

    def __init__(self, real_x0, real_x1, virtual_x0, virtual_x1,
                 label_format=LabelFormat("%.5f")):
        super(PriceAxis, self).__init__(real_x0, real_x1, virtual_x0,
                                        virtual_x1, label_format)

    @property
    def _resolution_set(self):
        return [
            0.00001, 0.00002, 0.00005,
            0.00010, 0.00020, 0.00050,
            0.00100, 0.00200, 0.00500,
            0.01000, 0.02000, 0.05000,
            0.10000, 0.20000, 0.50000,
            1.00000, 2.00000, 5.00000,
            10.0000, 20.0000, 50.0000,
            100.000, 200.000, 500.000,
            1000.00, 2000.00, 5000.00
        ]

    @property
    def _min_size(self):
        return 40

    @property
    def objects(self):
        for real_x, label in self.values():
            yield gobjects.Line(0, real_x, self.LINE_WIDTH, real_x)
            yield gobjects.Label(
                x=self.TEXT_START, y=real_x - 20, text=label,
                height=40, valign=gobjects.Label.VALIGN_CENTER)


class TimeAxis(Axis):

    def __init__(self, real_x0, real_x1, virtual_x0, virtual_x1):
        super(TimeAxis, self).__init__(
            real_x0, real_x1, virtual_x0, virtual_x1, FormatChoiser(self))
        self._resolution_label_format = self._get_resolution_label_format()

    def _get_resolution_label_format(self):
        return {
            dutils.ONE_SEC: TimeLabelFormat("%Ss", "%Y %b %d %H:%M:%S"),
            dutils.FIVE_SECS: TimeLabelFormat("%Ss", "%Y %b %d %H:%M:%S"),
            dutils.FIFTEEN_SECS: TimeLabelFormat("%Ss", "%Y %b %d %H:%M:%S"),
            dutils.THIRTY_SECS: TimeLabelFormat("%Ss", "%Y %b %d %H:%M:%S"),
            dutils.ONE_MIN: TimeLabelFormat("%H:%M", "%Y %b %d %H:%M"),
            dutils.FIVE_MINS: TimeLabelFormat("%H:%M", "%Y %b %d %H:%M"),
            dutils.FIFTEEN_MINS: TimeLabelFormat("%H:%M", "%Y %b %d %H:%M"),
            dutils.THIRTY_MINS: TimeLabelFormat("%H:%M", "%Y %b %d %H:%M"),
            dutils.ONE_HOUR: TimeLabelFormat("%H:%M", "%Y %b %d %H:%M"),
            dutils.FOUR_HOURS: TimeLabelFormat("%H:%M", "%Y %b %d %H:%M"),
            dutils.ONE_DAY: TimeLabelFormat("%d %b", "%Y %b %d"),
            dutils.ONE_WEEK: TimeLabelFormat("%W", "%Y week %W"),
            dutils.ONE_MONTH: TimeLabelFormat("%b", "%Y %b"),
            dutils.ONE_YEAR: TimeLabelFormat("%Y", "%Y")

        }

    def get_ex_resolution(self):
        resolution_map = {
            dutils.ONE_SEC: dutils.ONE_MIN,
            dutils.FIVE_SECS: dutils.ONE_MIN,
            dutils.FIFTEEN_SECS: dutils.ONE_MIN,
            dutils.THIRTY_SECS: dutils.ONE_MIN,
            dutils.ONE_MIN: dutils.ONE_HOUR,
            dutils.FIVE_MINS: dutils.ONE_HOUR,
            dutils.FIFTEEN_MINS: dutils.ONE_HOUR,
            dutils.THIRTY_MINS: dutils.ONE_HOUR,
            dutils.ONE_HOUR: dutils.ONE_DAY,
            dutils.FOUR_HOURS: dutils.ONE_DAY,
            dutils.ONE_DAY: dutils.ONE_WEEK,
            dutils.ONE_WEEK: dutils.ONE_MONTH,
            dutils.ONE_MONTH: dutils.ONE_YEAR,
            dutils.ONE_YEAR: dutils.ONE_YEAR
        }
        return resolution_map[self.get_resolution()]

    @property
    def _resolution_set(self, shift=0):
        return sorted(self._get_resolution_label_format().keys())

    @property
    def _min_size(self):
        return 90

    def scale(self, real_x_delta):
        virtual_x_delta = self._get_virtual_x_delta(real_x_delta)
        self.set_virtual_axis(self._virtual_x0 - virtual_x_delta,
                              self._virtual_x1)

    @property
    def objects(self):
        min_x = min(self._virtual_x0, self._virtual_x1)
        max_x = max(self._virtual_x0, self._virtual_x1)

        yield gobjects.Line(self._real_x0, 20, self._real_x1, 20)

        # Getting up axis objects
        interval = self.get_resolution()

        start_x = dutils.floor(min_x, interval)
        end_x = dutils.ceil(max_x, interval)

        # Calculate width
        width = (self._real_x0 - self.from_virtual_to_real(start_x) +
                 self.from_virtual_to_real(start_x + interval))

        for virtual_x in dutils.drange(start_x, end_x, interval):
            real_x = self.from_virtual_to_real(virtual_x)
            yield gobjects.Line(real_x, 0, real_x, 20)
            yield gobjects.Label(
                x=real_x, y=0, text=self._label_format.get_label(virtual_x),
                height=20, valign=gobjects.Label.VALIGN_CENTER,
                width=width, align=gobjects.Label.HALIGN_CENTER)

        # Getting bottom axis objects
        interval = self.get_ex_resolution()

        start_x = dutils.floor(min_x, interval)
        end_x = dutils.ceil(max_x, interval)

        # Calculate width
        width = (self._real_x0 - self.from_virtual_to_real(start_x) +
                 self.from_virtual_to_real(start_x + interval))

        for virtual_x in dutils.drange(start_x, end_x, interval):
            real_x = self.from_virtual_to_real(virtual_x)
            yield gobjects.Line(real_x, 20, real_x, 40)
            yield gobjects.Label(
                x=real_x, y=20,
                text=self._label_format.get_full_label(virtual_x),
                height=20, valign=gobjects.Label.VALIGN_CENTER,
                width=width, align=gobjects.Label.HALIGN_MAGIC_CENTER,
                canvas_x1=self._real_x1)
