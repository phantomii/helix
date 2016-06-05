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

from helix.gui.gtk import gio
from helix.gui.gtk import gtk
from helix.gui import windows


LOG = logging.getLogger(__name__)


class Application(gtk.Application):

    def __init__(self):
        super(Application, self).__init__(
            application_id='com.github.phantomii.helix',
            flags=gio.ApplicationFlags.FLAGS_NONE)
        self.window = None

    def do_activate(self, *args, **kwargs):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = windows.ApplicationWindow(
                application=self,
                title="Python treading platform")

        self.window.show_all()

    def on_quit(self, action, param):
        self.quit()
