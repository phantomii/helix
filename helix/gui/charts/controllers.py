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

import logging

from helix.gui.charts import contexts
from helix.gui.charts import tools
from helix.gui.gtk import gdk


LOG = logging.getLogger(__name__)


class ChartController(object):

    def __init__(self, chart_widget, start_time, end_time, start_price,
                 end_price):
        self._chart_widget = chart_widget

        chart_area = self._chart_widget.get_chart_area()
        self._price_axis = tools.PriceAxis(
            real_x0=0,
            real_x1=chart_area.get_allocated_height(),
            virtual_x0=start_price,
            virtual_x1=end_price)
        self._time_axis = tools.TimeAxis(
            real_x0=0,
            real_x1=chart_area.get_allocated_width(),
            virtual_x0=start_time,
            virtual_x1=end_time)

        # Get areas
        timeline_area = chart_widget.get_timeline_area()
        priceline_area = chart_widget.get_priceline_area()
        chart_area = chart_widget.get_chart_area()

        # Subscribe to signals
        timeline_area.connect("draw", self.on_draw_timeline)
        timeline_area.connect("button_press_event", self.on_press_timeline)
        timeline_area.connect("button-release-event", self.on_release_timeline)
        timeline_area.connect("motion-notify-event", self.on_motion_timeline)
        timeline_area.add_events(gdk.EventMask.BUTTON_PRESS_MASK |
                                 gdk.EventMask.BUTTON_RELEASE_MASK |
                                 gdk.EventMask.BUTTON1_MOTION_MASK)
        priceline_area.connect("draw", self.on_draw_priceline)
        priceline_area.connect("button_press_event", self.on_press_priceline)
        priceline_area.connect("button-release-event",
                               self.on_release_priceline)
        priceline_area.connect("motion-notify-event", self.on_motion_priceline)
        priceline_area.add_events(gdk.EventMask.BUTTON_PRESS_MASK |
                                  gdk.EventMask.BUTTON_RELEASE_MASK |
                                  gdk.EventMask.BUTTON1_MOTION_MASK)
        chart_area.connect("draw", self.on_draw_chart)
        chart_area.connect("size-allocate", self.on_chart_size_allocate)
        chart_area.connect("button_press_event", self.on_press_chart)
        chart_area.connect("button-release-event", self.on_release_chart)
        chart_area.connect("motion-notify-event", self.on_motion_chart)
        chart_area.add_events(gdk.EventMask.BUTTON_PRESS_MASK |
                              gdk.EventMask.BUTTON_RELEASE_MASK |
                              gdk.EventMask.BUTTON1_MOTION_MASK)
        chart_area.connect("draw", self.on_draw_chart)

    def on_press_chart(self, widget, event):
        self._move_chart = True
        self._time_previous_x = event.x
        self._price_previous_y = event.y

    def on_release_chart(self, widget, event):
        self._move_chart = False

    def on_motion_chart(self, widget, event):
        if self._move_chart:
            self._time_axis.move(event.x - self._time_previous_x)
            self._price_axis.move(event.y - self._price_previous_y)

            self._time_previous_x = event.x
            self._price_previous_y = event.y

            self._chart_widget.get_priceline_area().queue_draw()
            self._chart_widget.get_timeline_area().queue_draw()
            self._chart_widget.get_chart_area().queue_draw()

    def on_press_timeline(self, widget, event):
        self._time_previous_x = event.x

    def on_release_timeline(self, widget, event):
        pass

    def on_motion_timeline(self, widget, event):
        self._time_axis.scale(event.x - self._time_previous_x)

        self._time_previous_x = event.x

        self._chart_widget.get_timeline_area().queue_draw()
        self._chart_widget.get_chart_area().queue_draw()

    def on_press_priceline(self, widget, event):
        self._price_previous_y = event.y

    def on_release_priceline(self, widget, event):
        pass

    def on_motion_priceline(self, widget, event):
        self._price_axis.scale(event.y - self._price_previous_y)
        self._price_previous_y = event.y

        self._chart_widget.get_priceline_area().queue_draw()
        self._chart_widget.get_chart_area().queue_draw()

    def on_draw_timeline(self, widget, cr):
        ctx = contexts.GContext(cairo_contex=cr)

        for obj in self._time_axis.objects:
            obj.draw(ctx)

        # WIDTH = self._time_axis.real_x1
        # HC = self._chart_widget.TIMELINE_HEIGHT // 2
        # HWC = self._chart_widget.TIMELINE_HEIGHT
        # HC_DELTA = 3

        # # Drawing ...
        # cr.select_font_face("Ubuntu Mono", cairo.FONT_SLANT_NORMAL,
        #     cairo.FONT_WEIGHT_NORMAL)
        # cr.set_font_size(20)
        # cr.set_source_rgb(1, 1, 1)
        # cr.set_line_width(2)

        # # Draw deliver
        # cr.move_to(0, HC)
        # cr.line_to(WIDTH, HC)

        # for real_x, label in self._time_axis.values():
        #     cr.move_to(real_x, 0)
        #     cr.line_to(real_x, HC)
        #     cr.move_to(real_x + HC_DELTA, HC - HC_DELTA)
        #     cr.show_text(label)

        # for real_x, label in self._hr_time_axis.values():
        #     cr.move_to(real_x, HC),
        #     cr.line_to(real_x, HWC)
        #     cr.move_to(real_x + HC_DELTA, HWC - HC_DELTA)
        #     cr.show_text(label)

        # cr.stroke()

    def on_draw_priceline(self, widget, cr):
        ctx = contexts.GContext(cairo_contex=cr)

        for obj in self._price_axis.objects:
            obj.draw(context=ctx)

    def on_draw_chart(self, widget, cr):

        HEIGHT = self._price_axis.real_x1
        WIDTH = self._time_axis.real_x1

        cr.set_source_rgb(0.3, 0.3, 0.3)
        cr.set_dash([10.0, 5.0])

        # Draw price seporators
        for real_x, label in self._price_axis.values():
            cr.move_to(0, real_x)
            cr.line_to(WIDTH, real_x)

        # Draw time seporators
        for real_x, label in self._time_axis.values():
            cr.move_to(real_x, 0)
            cr.line_to(real_x, HEIGHT)

        cr.stroke()

    def on_chart_size_allocate(self, widget, allocation):
        self._price_axis.set_real_axis(0, allocation.height)
        self._time_axis.set_real_axis(0, allocation.width)
