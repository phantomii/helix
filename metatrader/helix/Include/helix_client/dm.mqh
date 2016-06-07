//+------------------------------------------------------------------+
//|                                                           dm.mqh |
//|              Copyright 2016, Eugene Frolov eugene@frolov.net.ru. |
//|                                     https://helix.synapse.net.ru |
//+------------------------------------------------------------------+
#property copyright "Copyright 2016, Eugene Frolov eugene@frolov.net.ru."
#property link      "https://helix.synapse.net.ru"
#property strict


class AbstractHelixObject {
   protected:
      string m_uuid;
   public:
      AbstractHelixObject(){};
      virtual string get_id() {
         return m_uuid;
      };
};


class HelixBroker : public AbstractHelixObject {
   protected:
      string m_name;
   public:
      HelixBroker(string uuid, string name) {
        init(uuid, name);
      };
      
      HelixBroker(const HelixBroker &abroker) {
         init(abroker.m_uuid, abroker.m_name);
      };
      
      HelixBroker(){};
      
      void init(string uuid, string name) {
         m_uuid = uuid;
         m_name = name;
      };
      
      string get_name() {
         return m_name;
      };
};


class HelixInstrument: public AbstractHelixObject {
   protected:
      string m_name;
      string m_ticker_symbol;  
      int m_digits;
   public:
      HelixInstrument(string uuid, string name, string ticker_symbol, int digits){
         init(uuid, name,ticker_symbol, digits);
      };
      
      HelixInstrument(const HelixInstrument &inst){
         init(inst.m_uuid, m_name, m_ticker_symbol, m_digits);
      };
      
      HelixInstrument(){};
      
      void init(string uuid, string name, string ticker_symbol, int digits){
         m_uuid = uuid;
         m_name = name;
         m_ticker_symbol = ticker_symbol;
         m_digits = digits;
      };
      
      string get_name() {
         return m_name;
      };
      
      string get_ticker_symbol() {
         return m_ticker_symbol;
      };
      
      int get_digits() {
         return m_digits;
      };
};
