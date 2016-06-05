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

import six


@six.add_metaclass(abc.ABCMeta)
class GObject(object):

    @abc.abstractmethod
    def draw(self, context):
        raise NotImplementedError()


class Line(GObject):

    def __init__(self, x0, y0, x1, y1):
        super(Line, self).__init__()
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1

    def draw(self, context):
        cr = context.get_cairo_context()
        cr.move_to(self._x0, self._y0)
        cr.line_to(self._x1, self._y1)
        cr.stroke()


class Label(GObject):

    VALIGN_TOP = 1
    VALIGN_CENTER = 2
    VALIGN_BOTTOM = 3

    HALIGN_LEFT = 4
    HALIGN_CENTER = 5
    HALIGN_RIGHT = 6

    # Magic align
    HALIGN_MAGIC_CENTER = 7

    def __init__(self, x, y, text, width=0, height=0,
                 align=HALIGN_LEFT, valign=VALIGN_BOTTOM, canvas_x1=0):
        super(Label, self).__init__()
        self._x = x
        self._y = y
        self._text = text
        self._width = width
        self._height = height
        self._valign = valign
        self._halign = align
        if align == self.HALIGN_MAGIC_CENTER and canvas_x1 < 1:
            raise ValueError("'canvas_x1' parameter should not be < 1")
        self._canvas_x1 = canvas_x1

    def _calculate_y(self, text_height):
        if self._valign == self.VALIGN_TOP:
            return self._y + text_height
        elif self._valign == self.VALIGN_CENTER:
            return self._y + (self._height / 2.0) + (text_height / 2.0)
        elif self._valign == self.VALIGN_BOTTOM:
            return self._y + self._height
        else:
            raise ValueError("Incorrect value (%s) for vertical align")

    def _calculate_x(self, text_width):
        if self._halign == self.HALIGN_LEFT:
            return self._x
        elif self._halign == self.HALIGN_CENTER:
            return self._x + (self._width / 2.0) - (text_width / 2.0)
        elif self._halign == self.HALIGN_RIGHT:
            return self._x + self._width - text_width
        elif self._halign == self.HALIGN_MAGIC_CENTER:
            real_width = self._width
            real_x = self._x
            if self._x < 0:
                real_width += self._x
                real_x = 0
            if self._canvas_x1 < self._x + self._width:
                real_width -= (self._x + self._width - self._canvas_x1)
            if text_width < real_width:
                return real_x + (real_width / 2.0) - (text_width / 2.0)
            elif self._x < 0:
                return self._x + self._width - text_width
            else:
                return self._x
        else:
            raise ValueError("Incorrect value (%s) for vertical align")

    def draw(self, context):
        cr = context.get_cairo_context()
        width, height = cr.text_extents(self._text)[2:4]
        cr.move_to(self._calculate_x(width), self._calculate_y(height))
        cr.show_text(self._text)
