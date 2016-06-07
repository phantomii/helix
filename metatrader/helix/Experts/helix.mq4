//+------------------------------------------------------------------+
//|                                                        helix.mq4 |
//|              Copyright 2016, Eugene Frolov eugene@frolov.net.ru. |
//|                                     https://helix.synapse.net.ru |
//+------------------------------------------------------------------+
#property copyright "Copyright 2016, Eugene Frolov eugene@frolov.net.ru."
#property link      "https://helix.synapse.net.ru"
#property version   "1.00"
#property strict
//--- input parameters
input string   helix_server = "http://192.168.1.102";
input string   api_version = "v1";
input string   broker_name = "Forex Club"; //"58ab0b86-3944-4b9a-806b-be949d175236";
input string   instrument_name = "Bitcoin"; //"6b4bd34a-9f53-48f7-b489-dfdbe4416ad6";

#include <helix_client/client.mqh>

HelixClient       client(helix_server, api_version);

HelixBroker       broker;
HelixInstrument   instrument;


int get_error_code(int answer_code) {
   if ( answer_code == -1)
      return GetLastError();
   return answer_code;
}

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit() {

   int hcode = 0;

   int err_code = client.health_check(); 
   if (err_code == ERR_NO_ERROR) {
      hcode = client.get_broker(broker_name, broker);
      if (hcode != ERR_NO_ERROR) return hcode;
      hcode = client.get_instrument(broker, instrument_name, instrument);
      if (hcode != ERR_NO_ERROR) return hcode;   
      return(INIT_SUCCEEDED);
   } else {
      PrintFormat("Connect to %s filed with err code: %d", helix_server,
                  get_error_code(err_code));
      return(INIT_FAILED);
   };
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick(){
   MqlTick tick;
   if (!SymbolInfoTick(Symbol(), tick)) return;
   client.create_tick(broker, instrument, tick);
}

