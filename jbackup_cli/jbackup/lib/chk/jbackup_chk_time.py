#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import os.path
import os
import sys
import multiprocessing
from datetime import datetime, date
import datetime as dt
import time
from jbackup.lib.log.jbackup_logging import Logging

class jbackup_chk_time:
### START DEF ###

   # disk size check
   def _chk_time(self,reserve_time, log_file, flag):
      now_time = datetime.now()
      #format = "%a %b %d %H:%M"
      #str_reserve_time = reserve_time.strftime(format)
      #str_now_time = (now_time).strftime(format)

      lrt = reserve_time.timetuple()
      lnt = now_time.timetuple()
      ## Logging._logging(log_file, "Time interval(" + str(flag) + ") : " + str(lrt.tm_min - lnt.tm_min) + " mins")

      if (len(lrt) == len(lnt)):
         if (lrt.tm_year != lnt.tm_year):
            return_flag = 0
            Logging._logging(log_file, "Time interval(" + str(flag) + ") : " + str(lrt.tm_year - lnt.tm_year) + " year")
         elif (lrt.tm_mon != lnt.tm_mon):
            return_flag = 0
            Logging._logging(log_file, "Time interval(" + str(flag) + ") : " + str(lrt.tm_mon - lnt.tm_mon) + " month")
         elif (lrt.tm_mday != lnt.tm_mday):
            return_flag = 0
            Logging._logging(log_file, "Time interval(" + str(flag) + ") : " + str(lrt.tm_mday - lnt.tm_mday) + " day")
         # elif (lrt.tm_hour != lnt.tm_hour):
            # return_flag = 1
            ## return_flag = 0
         else:
            #if ((lrt.tm_min - lnt.tm_min) == 180):
            return_flag = 1
            #else:
            #   return_flag = 0
      else:
         Logging._logging(log_file, "Please check reservation time format!")
         raise SystemExit

      return return_flag

##   @staticmethod
##   def _get_current_time(log_file):
##      current_date = []
##      try:
##         now_time = datetime.now().time().strftime('%H_%M_%S')
##         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
##         print(datetime.now())
##         today = date.today()
##         current_date.append(today.year)
##         current_date.append(today.month)
##         current_date.append(today.day)
##         current_date.append(now_time)
##      except Exception as err:
##         Logging._logging(log_file, "Can not get current time!")
##         Logging._logging(log_file, str(err))
##         raise SystemExit
##      else:
##         return current_date

##   @staticmethod
##   def _get_before_time(log_file, bf_day):
##      before_date = []
##      try:
##         today = date.today()
##         bf_date = (today - dt.timedelta(days=bf_day))
##         before_date.append(bf_date.year)
##         before_date.append(bf_date.month)
##         before_date.append(bf_date.day)
##      except Exception as err:
##         Logging._logging(log_file, "Can not get current time!")
##         Logging._logging(log_file, str(err))
##         raise SystemExit
##      else:
##         return before_date

### END DEF ###
