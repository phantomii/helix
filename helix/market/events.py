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


from helix.events import base


class _BaseOnOrderPosition(base.Event):

    def __init__(self, order_position):
        super(_BaseOnOrderPosition, self).__init__()
        self._order_position = order_position

    @property
    def order_position(self):
        return self._order_position


class OnOrderPositionSubmitted(_BaseOnOrderPosition):
    pass


class OnOrderPositionFilled(_BaseOnOrderPosition):
    pass
