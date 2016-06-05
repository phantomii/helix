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

import cairo
import six


class GContext(object):

    def __init__(self, cairo_contex, font=None, color=None, line_style=None):
        self._cr = cairo_contex
        self.set_font(font or Font(font_name="Ubuntu Mono", size=20))
        self.set_source_color(color or RGBColor(red=1, green=1, blue=1))
        self.set_line_style(line_style or LineStyle(width=2))

    def get_cairo_context(self):
        return self._cr

    def set_font(self, font):
        font.apply(self.get_cairo_context())
        self._font = font

    def set_source_color(self, color):
        color.apply(self.get_cairo_context())
        self._source_color = color

    def set_line_style(self, line_style):
        line_style.apply(self.get_cairo_context())
        self._line_style = line_style


@six.add_metaclass(abc.ABCMeta)
class GParameters(object):

    @abc.abstractmethod
    def apply(self, cr):
        raise NotImplementedError()


class Font(GParameters):

    # Upright font style
    FONT_SLANT_NORMAL = cairo.FONT_SLANT_NORMAL
    # Italic font style
    FONT_SLANT_ITALIC = cairo.FONT_SLANT_ITALIC
    # Oblique font style
    FONT_SLANT_OBLIQUE = cairo.FONT_SLANT_OBLIQUE

    # Normal font weight
    FONT_WEIGHT_NORMAL = cairo.FONT_WEIGHT_NORMAL
    # Bold font weight
    FONT_WEIGHT_BOLD = cairo.FONT_WEIGHT_BOLD

    def __init__(self, font_name, size, slant=FONT_SLANT_NORMAL,
                 weight=FONT_WEIGHT_NORMAL):
        super(Font, self).__init__()
        self._font_name = font_name
        self._size = size
        self._slant = slant
        self._weight = weight

    def apply(self, cr):
        cr.select_font_face(self._font_name, self.FONT_SLANT_NORMAL,
                            self.FONT_WEIGHT_NORMAL)
        cr.set_font_size(self._size)


class RGBColor(GParameters):

    def __init__(self, red, green, blue):
        super(RGBColor, self).__init__()
        self._red = red
        self._green = green
        self._blue = blue

    def apply(self, cr):
        cr.set_source_rgb(self._red, self._green, self._blue)


class LineStyle(GParameters):

    LINE_CAP_BUTT = cairo.LINE_CAP_BUTT
    LINE_CAP_ROUND = cairo.LINE_CAP_ROUND
    LINE_CAP_SQUARE = cairo.LINE_CAP_SQUARE

    def __init__(self, width, dash=None, cap=LINE_CAP_BUTT):
        super(LineStyle, self).__init__()
        self._width = width
        self._dash = dash or []
        self._cap = cap

    def apply(self, cr):
        cr.set_line_width(self._width)
        cr.set_dash(self._dash)
        cr.set_line_cap(self._cap)
