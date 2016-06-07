//+------------------------------------------------------------------+
//|                                                       errors.mqh |
//|              Copyright 2016, Eugene Frolov eugene@frolov.net.ru. |
//|                                     https://helix.synapse.net.ru |
//+------------------------------------------------------------------+
#property copyright "Copyright 2016, Eugene Frolov eugene@frolov.net.ru."
#property link      "https://helix.synapse.net.ru"
#property strict

// Code errors
const int ERR_HELIX_START_CODE                     = 70000;
const int ERR_HELIX_OBJECT_NOT_FOUND               = ERR_HELIX_START_CODE + 404;
const int ERR_HELIX_UNKNOWN_ERROR                  = ERR_HELIX_START_CODE + 500;

const int ERR_HELIX_CANT_PARSE_JSON                = ERR_HELIX_START_CODE + 1001;

const int ERR_HELIX_HAS_MANY_OBJECTS               = ERR_HELIX_START_CODE + 2001;


int get_helix_error_code(int http_code){
   return ERR_HELIX_START_CODE + http_code;
}