//+------------------------------------------------------------------+
//|                                                 helix_client.mqh |
//|              Copyright 2016, Eugene Frolov eugene@frolov.net.ru. |
//|                                     https://helix.synapse.net.ru |
//+------------------------------------------------------------------+
#property copyright "Copyright 2016, Eugene Frolov eugene@frolov.net.ru."
#property link      "https://helix.synapse.net.ru"
#property strict

#include <helix_client/dm.mqh>
#include <helix_client/errors.mqh>
#include <helix_client/jason.mqh>


class HTTPAnswer {
   private:
      string m_body;
      string m_headers;
   public:
      HTTPAnswer(){};
      HTTPAnswer(string body, string headers) {
         init(body, headers);
      };
      HTTPAnswer(const HTTPAnswer &answer) {
         init(answer.m_body, answer.m_headers);
      };

      void init(string body, string headers) {
         m_body = body;
         m_headers = headers;
      }

      string get_body(){
         return m_body;
      };

      string get_headers() {
         return m_headers;
      };
};

class HelixClient {
   protected:
      string m_url;
      string m_ver;

      string m_content_type;
   public:
      HelixClient(string url, string version) {
         m_url = url;
         m_ver = version;
         m_content_type = "application/json";
      };

      int health_check() {
         HTTPAnswer result;
         int err_code = get(get_version_url(), "", result);
         if ( err_code == 200 )
            return ERR_NO_ERROR;
         return get_helix_error_code(err_code);
      };

      int get_broker(string abroker_name, HelixBroker &abroker) {
         HTTPAnswer result;
         int hcode = get(get_brokers_url(), StringFormat("name=%s", abroker_name), result);
         if (hcode == 200){
            CJAVal js(NULL, jtUNDEF);
            if (!js.Deserialize(result.get_body())) return ERR_HELIX_CANT_PARSE_JSON;
            if (ArraySize(js.m_e) == 0) return ERR_HELIX_OBJECT_NOT_FOUND;
            if (ArraySize(js.m_e) > 1) return ERR_HELIX_HAS_MANY_OBJECTS;
            abroker.init(js.m_e[0]["uuid"].ToStr(), js.m_e[0]["name"].ToStr());
            return ERR_NO_ERROR;
         };
         return get_helix_error_code(hcode);
      };

      int get_instrument(HelixBroker &abroker, string name, HelixInstrument &ainstrument){
         HTTPAnswer result;
         int hcode = get(get_instruments_url(abroker), StringFormat("name=%s", name), result);
         if (hcode == 200){
            CJAVal js(NULL, jtUNDEF);
            if (!js.Deserialize(result.get_body())) return ERR_HELIX_CANT_PARSE_JSON;
            if (ArraySize(js.m_e) == 0) return ERR_HELIX_OBJECT_NOT_FOUND;
            if (ArraySize(js.m_e) > 1) return ERR_HELIX_HAS_MANY_OBJECTS;
            ainstrument.init(js.m_e[0]["uuid"].ToStr(), js.m_e[0]["name"].ToStr(),
                             js.m_e[0]["ticker-symbol"].ToStr(), js.m_e[0]["digits"].ToInt());
            return ERR_NO_ERROR;
         };
         return get_helix_error_code(hcode);
      };

      int create_tick(HelixBroker &abroker, HelixInstrument &ainstrument, MqlTick &tick){
         HTTPAnswer result;
         CJAVal js;
         js["timestamp"] = tick.time_msc / 1000;
         js["ask"] = tick.ask;
         js["bid"] = tick.bid;
         js["ask-volume"] = (double)tick.volume;
         js["bid-volume"] = (double)tick.volume;
         string b = js.Serialize();
         char body[];
         StringToCharArray(b, body, 0, StringLen(b));
         int hcode = post(get_ticks_url(abroker, ainstrument), "", body, result);
         if (hcode == 201) {
            return ERR_NO_ERROR;
         }
         return get_helix_error_code(hcode);
      }

   private:
      string get_headers(){
         return StringFormat("Content-Type: %s", m_content_type);
      };

      string get_version_url(){
         return StringFormat("%s/%s/", m_url, m_ver);
      };

      string get_brokers_url(){
         return StringFormat("%sbrokers/", get_version_url());
      };

      string get_instruments_url(HelixBroker &abroker){
         return StringFormat("%s%s/instruments/", get_brokers_url(), abroker.get_id());
      };

      string get_ticks_url(HelixBroker &abroker, HelixInstrument &ainstrument){
         return StringFormat("%s%s/ticks/", get_instruments_url(abroker),
                             ainstrument.get_id());
      };

      int post(string url, string params, char &body[], HTTPAnswer &result) {
         return do_request("POST", url, params, body, result);
      };

      int get(string url, string params, HTTPAnswer &result) {
         char body[];
         return do_request("GET", url, params, body, result);
      };

      int do_request(string method, string url, string params, char &body[], HTTPAnswer &result) {
         char response_body[];
         string headers;
         if (params != "") url = StringFormat("%s?%s", url, params);
         int res = WebRequest(method, url, get_headers(), 0, body, response_body, headers);
         result.init(CharArrayToString(response_body), headers);
         return res;
      };
};
