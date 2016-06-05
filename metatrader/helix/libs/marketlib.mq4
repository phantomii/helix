//+------------------------------------------------------------------+
//|         Copyright 2015, S.Y.N.A.P.S.E Technology (Eugene Frolov) |
//|                                      http://helix.synapse.net.ru |
//+------------------------------------------------------------------+

//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.

class Tick {
	protected:
		string m_symbol;
		datetime m_datetime;
		double m_ask;
		double m_bid;

	public:
		Tick (const string symbol, const datetime tick_time,
			  const double ask, const double bid) {
			m_symbol = symbol;
			m_datetime = tick_time;
			m_ask = ask;
			m_bid = bid;
		}
}