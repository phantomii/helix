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


import copy
import unittest

from helix.market import order_books
from helix.market import orders


class OrderBookTestCase(unittest.TestCase):

    def setUp(self):
        self._order_book = order_books.OrderBook()

    def tearDown(self):
        del self._order_book

    def test_ask_and_bid_price_raises_error_if_orderbook_empty(self):
        self.assertRaises(order_books.NoQuotas, self._order_book.get_ask)
        self.assertRaises(order_books.NoQuotas, self._order_book.get_bid)

    def test_ask_and_bid_price__returns_default_if_orderbook_empty(self):
        self.assertEqual(self._order_book.get_ask(default=1), 1)
        self.assertEqual(self._order_book.get_bid(default=2), 2)

    def test_ask_and_bid_price_positive(self):
        position_sell1 = orders.SellOrderPosition(price=1.24251)
        position_sell2 = orders.SellOrderPosition(price=1.24250)
        position_buy1 = orders.BuyOrderPosition(price=1.25261)
        position_buy2 = orders.BuyOrderPosition(price=1.24250)

        self._order_book._ask_positions[1.25261] = position_buy1
        self._order_book._bid_positions[1.24251] = position_sell1
        self._order_book._ask_positions[1.25260] = position_buy2
        self._order_book._bid_positions[1.24250] = position_sell2

        self.assertEqual(1.25260, self._order_book.get_ask())
        self.assertEqual(1.24251, self._order_book.get_bid())

    def test_add_positions_one(self):
        self._order_book._ask_positions[1.20000] = [
            orders.SellOrderPosition(price=1.20000) for i in xrange(100)]
        self._order_book._bid_positions[1.10000] = [
            orders.BuyOrderPosition(price=1.10000) for i in xrange(100)]

        self._order_book.add([
            orders.SellOrderPosition(price=1.19000) for i in xrange(50)])
        self._order_book.add([
            orders.BuyOrderPosition(price=1.10000) for i in xrange(50)])

        self.assertEqual(len(self._order_book.get_ask_positions(1.20000)), 100)
        self.assertEqual(len(self._order_book.get_ask_positions(1.19000)), 50)
        self.assertEqual(len(self._order_book.get_bid_positions(1.10000)), 150)
        self.assertEqual(self._order_book.get_ask(), 1.19000)
        self.assertEqual(self._order_book.get_bid(), 1.10000)

    def test_add_sell_positions_one(self):
        self._order_book._ask_positions[1.20000] = [
            orders.SellOrderPosition(price=1.20000) for i in xrange(100)]
        self._order_book._bid_positions[1.10000] = [
            orders.BuyOrderPosition(price=1.10000) for i in xrange(100)]
        self._order_book._bid_positions[1.09999] = [
            orders.BuyOrderPosition(price=1.09999) for i in xrange(10)]
        self._order_book._bid_positions[1.09000] = [
            orders.BuyOrderPosition(price=1.09000) for i in xrange(100)]

        self._order_book.add([
            orders.SellOrderPosition(price=1.09000) for i in xrange(200)])

        self.assertEqual(len(self._order_book.get_ask_positions(1.20000)), 100)
        self.assertEqual(len(self._order_book.get_bid_positions(1.09000)), 10)
        self.assertEqual(self._order_book.get_ask(), 1.20000)
        self.assertEqual(self._order_book.get_bid(), 1.09000)

    def test_add_buy_positions_one(self):
        self._order_book._ask_positions[1.09000] = [
            orders.SellOrderPosition(price=1.09000) for i in xrange(100)]
        self._order_book._ask_positions[1.10000] = [
            orders.SellOrderPosition(price=1.10000) for i in xrange(100)]
        self._order_book._bid_positions[1.00000] = [
            orders.BuyOrderPosition(price=1.00000) for i in xrange(100)]

        self._order_book.add([
            orders.BuyOrderPosition(price=1.09500) for i in xrange(200)])

        self.assertEqual(len(self._order_book.get_ask_positions(1.09000)), 0)
        self.assertEqual(len(self._order_book.get_ask_positions(1.10000)), 100)
        self.assertEqual(len(self._order_book.get_bid_positions(1.00000)), 100)
        self.assertEqual(len(self._order_book.get_bid_positions(1.09500)), 100)
        self.assertEqual(self._order_book.get_ask(), 1.10000)
        self.assertEqual(self._order_book.get_bid(), 1.09500)

    def test_remove_positions(self):
        buy_positions = [
            orders.BuyOrderPosition(price=1) for i in xrange(100)]
        sell_positions = [
            orders.SellOrderPosition(price=1.2) for i in xrange(100)]

        self._order_book._ask_positions[1.2] = copy.copy(sell_positions)
        self._order_book._bid_positions[1] = copy.copy(buy_positions)

        self.assertEqual(self._order_book.remove(sell_positions[50:]), [])
        self.assertEqual(self._order_book.remove(buy_positions[:50]), [])

        self.assertEqual(self._order_book._ask_positions[1.2],
                         sell_positions[:50])
        self.assertEqual(self._order_book._bid_positions[1],
                         buy_positions[50:])
