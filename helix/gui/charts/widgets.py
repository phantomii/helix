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

from helix.gui.gtk import gtk


class ChartWidget(gtk.Alignment):

    TIMELINE_HEIGHT = 40
    PRICELINE_WIDHT = 100

    def __init__(self):
        super(ChartWidget, self).__init__()
        self.set_padding(padding_top=5, padding_bottom=5,
                         padding_left=10, padding_right=10)

        main_box = gtk.Box(orientation=gtk.Orientation.VERTICAL,
                           spacing=3)
        main_box.pack_start(self._build_chart(), True, True, 0)
        main_box.pack_end(self._build_timeline(), False, True, 0)

        self.add(main_box)

    def _build_chart(self):
        box = gtk.Box(orientation=gtk.Orientation.HORIZONTAL,
                      spacing=3)
        self._chart_area = gtk.DrawingArea()
        # self._chart_area.connect("draw", self.on_draw_chart)
        self._price_area = gtk.DrawingArea(width_request=self.PRICELINE_WIDHT)
        # self._price_area.connect("draw", self.on_draw_priceline)

        box.pack_start(self._chart_area, True, True, 0)
        box.pack_end(self._price_area, False, True, 0)

        return box

    def _build_timeline(self):
        box = gtk.Box(orientation=gtk.Orientation.HORIZONTAL,
                      spacing=3)
        self._time_area = gtk.DrawingArea(height_request=self.TIMELINE_HEIGHT)
        # self._time_area.connect("draw", self.on_draw_timeline)
        null_area = gtk.DrawingArea(height_request=self.TIMELINE_HEIGHT,
                                    width_request=self.PRICELINE_WIDHT)

        box.pack_start(self._time_area, True, True, 0)
        box.pack_end(null_area, False, True, 0)

        return box

    def get_timeline_area(self):
        return self._time_area

    def get_chart_area(self):
        return self._chart_area

    def get_priceline_area(self):
        return self._price_area

    def attach_controller(self, ctr_class, *args, **kwargs):
        self._ctrl = ctr_class(self, *args, **kwargs)
