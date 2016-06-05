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


#property copyright "Copyright (c) 2015, Eugene Frolov S. http://helix.synapse.net.ru/"
#property link      "http://helix.synapse.net.ru"
#property version   "1.0"
#property strict

#include "enginelib.mq4";

input string API_FOLDER = "Helix";

input bool ASYNC_MODE = false;


FileEngine engine();

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit() {
	if (engine.init(Symbol(), API_FOLDER, ASYNC_MODE)) {
		return(INIT_SUCCEEDED);
	} else {
		return(INIT_FAILED);
	}
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason) {

}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick() {
	int x = 5;
	PrintFormat("%d %d", x++, x);
	engine.onTick(Ask, Bid);
}