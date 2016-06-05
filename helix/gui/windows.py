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

from helix.gui.charts import factory as chart_factory
from helix.gui.gtk import gtk
from helix.gui import tools


LOG = logging.getLogger(__name__)


class ApplicationWindow(gtk.ApplicationWindow):

    def __init__(self, application, title):
        super(ApplicationWindow, self).__init__(application=application,
                                                title=title)
        content = self._build_window_content()
        self.add(content)

    def _build_window_content(self):
        box = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=3)

        box.pack_start(self._build_charts(), True, True, 0)
        box.pack_start(self._build_tools(), False, True, 0)
        box.pack_start(self._build_status_bar(), False, True, 0)

        return box

    def _build_charts(self):
        self._charts_notebook = gtk.Notebook()
        # TODO(efrolov): Load charts here
        self.add_chart('Test', chart_factory.build_chart())

        return self._charts_notebook

    def add_chart(self, instrument_name, chart):
        self._charts_notebook.append_page(chart,
                                          gtk.Label(instrument_name))

    def _build_tools(self):
        tools_notebook = gtk.Notebook()

        tools_notebook.append_page(self._build_log_messages(),
                                   gtk.Label('Messages'))
        tools_notebook.append_page(self._build_strategy_tester(),
                                   gtk.Label('Strategy Tester'))

        return tools_notebook

    def _build_strategy_tester(self):

        return tools.StrategyTesterTool()

    def _build_log_messages(self):
        return tools.LogMessagesTool()

    def _build_status_bar(self):
        return gtk.Statusbar()
