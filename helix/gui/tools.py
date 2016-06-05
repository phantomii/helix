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


class LogMessagesTool(gtk.Alignment):

    def __init__(self):
        super(LogMessagesTool, self).__init__()
        self.set_padding(padding_top=5, padding_bottom=5,
                         padding_left=10, padding_right=10)

        main_box = gtk.Box(
            orientation=gtk.Orientation.VERTICAL,
            spacing=3)

        main_box.pack_start(self._build_toolbar(), False, True, 3)
        main_box.pack_start(self._build_log_space(), True, True, 10)

        self.add(main_box)

    def _build_toolbar(self):
        toolbar = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=3)
        toolbar.pack_start(gtk.Button(label="Copy Messages"),
                           False, True, 0)
        toolbar.pack_start(gtk.Button(label="Clear Messages"),
                           False, True, 0)
        return toolbar

    def _build_log_space(self):
        mes_scrolled_window = gtk.ScrolledWindow()
        mes_scrolled_window.set_min_content_width(200)
        mes_scrolled_window.set_min_content_height(200)
        mes_text_view = gtk.TextView()
        textbuffer = mes_text_view.get_buffer()
        textbuffer.set_text(
            "This is some text inside of a Gtk.TextView. "
            + "Select text and click one of the buttons 'bold', 'italic', "
            + "or 'underline' to modify the text accordingly.")
        mes_scrolled_window.add(mes_text_view)
        return mes_scrolled_window


class StrategyTesterTool(gtk.Alignment):

    def __init__(self):
        super(StrategyTesterTool, self).__init__()

        self.set_padding(padding_top=5, padding_bottom=5,
                         padding_left=10, padding_right=10)
        main_box = gtk.Box(orientation=gtk.Orientation.VERTICAL,
                           spacing=3)
        main_box.pack_start(self._build_strategy_toolbar(), False, True, 3)
        main_box.pack_start(self._build_params_toolbar(), False, True, 3)
        main_box.pack_start(self._build_log_space(), True, True, 10)

        self.add(main_box)

    def _build_strategy_toolbar(self):
        toolbar = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=3)
        toolbar.pack_start(gtk.ComboBox(), True, True, 0)
        toolbar.pack_start(gtk.Button(label="Open..."), False, True, 0)
        toolbar.pack_start(gtk.Button(label="Edit..."), False, True, 0)
        return toolbar

    def _build_params_toolbar(self):
        toolbar = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=3)

        # Left side
        left_params = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=0)
        left_params.pack_start(gtk.CheckButton(label="Visual Mode"),
                               False, True, 0)
        left_params.pack_start(gtk.CheckButton(label="Optimisation"),
                               False, True, 0)
        left_params.pack_start(gtk.CheckButton(label="Show Messages"),
                               False, True, 0)

        # Right side
        right_params = gtk.Box(orientation=gtk.Orientation.VERTICAL,
                               spacing=3)
        # Right top side
        right_top_params = gtk.Box(orientation=gtk.Orientation.HORIZONTAL,
                                   spacing=3)
        right_top_params.pack_start(gtk.Button(label="Account..."),
                                    False, True, 0)
        right_top_params.pack_start(gtk.Button(label="Instruments..."),
                                    False, True, 0)
        right_top_params.pack_start(
            gtk.Button(label="01.01.2015 - 01.01.2016"), False, True, 0)
        right_top_params.pack_start(gtk.ComboBox(width_request=200),
                                    False, True, 0)
        right_top_params.pack_start(gtk.ComboBox(), True, True, 0)
        # Right bottom side
        right_bottom_params = gtk.Box(orientation=gtk.Orientation.HORIZONTAL,
                                      spacing=3)
        copy_button = gtk.Button(image=gtk.Image.new_from_stock(
            gtk.STOCK_COPY, gtk.IconSize.BUTTON))
        clear_button = gtk.Button(image=gtk.Image.new_from_stock(
            gtk.STOCK_CLEAR, gtk.IconSize.BUTTON))
        custom_settings_button = gtk.Button(label='Custom settings...')
        progress_bar = gtk.ProgressBar(show_text=True)
        speed_label = gtk.Label(label='Test Speed:')
        speed_scale = gtk.Scale(draw_value=False, width_request=200)
        forward_button = gtk.Button(image=gtk.Image.new_from_stock(
            gtk.STOCK_MEDIA_FORWARD, gtk.IconSize.BUTTON))
        pause_button = gtk.Button(image=gtk.Image.new_from_stock(
            gtk.STOCK_MEDIA_PAUSE, gtk.IconSize.BUTTON))
        start_button = gtk.Button(image=gtk.Image.new_from_stock(
            gtk.STOCK_MEDIA_PLAY, gtk.IconSize.BUTTON))
        right_bottom_params.pack_start(copy_button, False, True, 0)
        right_bottom_params.pack_start(clear_button, False, True, 0)
        right_bottom_params.pack_start(custom_settings_button,
                                       False, False, 0)
        right_bottom_params.pack_start(progress_bar, True, True, 0)
        right_bottom_params.pack_start(speed_label, False, True, 0)
        right_bottom_params.pack_start(speed_scale, False, True, 0)
        right_bottom_params.pack_start(forward_button, False, True, 0)
        right_bottom_params.pack_start(pause_button, False, True, 0)
        right_bottom_params.pack_start(start_button, False, True, 0)

        right_params.pack_start(right_top_params, False, True, 0)
        right_params.pack_end(right_bottom_params, False, True, 0)

        toolbar.pack_start(left_params, False, True, 0)
        toolbar.pack_start(right_params, True, True, 0)

        return toolbar

    def _build_log_space(self):
        scrolled_space = gtk.ScrolledWindow()
        scrolled_space.set_min_content_height(200)
        scrolled_space.add(gtk.TextView())

        return scrolled_space
