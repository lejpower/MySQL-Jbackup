#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import os
import os.path
import subprocess
from jbackup.lib.etc.jbackup_get_date import jbackup_get_date

#class jbackup_logging:
class Logging:
### START DEF ###
   @staticmethod
   def _create_log_file(type, tmp_dir):
      get_host = os.uname()[1].split(".")[0]

      get_date = jbackup_get_date()
      log_time = get_date._get_now_ymd()

      if (type != 'check'):
         if (os.path.isdir(tmp_dir)):
             log_file = tmp_dir + "/" + type + "_" + get_host + "_" + log_time + ".log"

             if (os.path.isfile(log_file)):
                mv_old_log = Logging._mv_log(log_file)

             Logging._logging(log_file, "[Created Log File] - " + log_file)
             Logging._logging_blank(log_file)
         else:
             try:
                os.makedirs(tmp_dir)
             except OSError as e:
                print(e)
                tmp_dir = "/var/log"
             except Exception as e:
                print(e)
                tmp_dir = "/var/log"
             finally:
                log_file = tmp_dir + "/" + type + "_" + get_host + "_" + log_time + ".log"

                if (os.path.isfile(log_file)):
                   mv_old_log = Logging._mv_log(log_file)

                Logging._logging(log_file, "[Created Log File] - " + log_file)
                Logging._logging_blank(log_file)

      elif (type == 'check'):
         if (os.path.isdir(tmp_dir)):
            log_file = tmp_dir + "/" + type + "_" + get_host + ".log"

            if (os.path.isfile(log_file)):
               pass
            else:
               Logging._logging(log_file, "[Created Log File] - " + log_file)
               Logging._logging_blank(log_file)

         else:
             try:
                os.makedirs(tmp_dir)
             except OSError as e:
                print(e)
                tmp_dir = "/var/log"
             except Exception as e:
                print(e)
                tmp_dir = "/var/log"
             finally:
                log_file = tmp_dir + "/" + type + "_" + get_host + ".log"
                Logging._logging_blank(log_file)

      return log_file

   @staticmethod
   def _mv_log(log_file):
      get_time = jbackup_get_date()
      change_time = get_time._get_now_hms()
      old_log_file = log_file.split(".log")[0] + '_' + change_time + '.log'

      try:
         os.rename(log_file, old_log_file)
      except IOError as e:
         print("Can not move " + log_file)
         print(e)
         Logging._logging(log_file , "Can not move " + log_file)
         Logging._logging(log_file , e)
         raise SystemExit
      else:
         Logging._logging(log_file , "[Moved Old Log]")
         Logging._logging(log_file , log_file + " to " + old_log_file)
         Logging._logging_blank(log_file)

   @staticmethod
   def _logging(log_file, msg):
      try:
         logging = open(log_file,'a')
      except IOError:
         print("cannot be opened : " + log_file)
      except Exception as e:
         print(e)
      else:
         get_time = jbackup_get_date()
         logging_time = get_time._get_now_ymdhms_log()
         logging.write("[" + logging_time + "] : " + str(msg) + "\n")
         print("["+ str(logging_time) + "] : " + str(msg))
      finally:
         logging.close()

   @staticmethod
   def _logging_blank(log_file):
      try:
         logging = open(log_file,'a')
      except IOError:
         print("cannot be opened : " + log_file)
      else:
         logging.write("\n")
         print("")

      logging.close()

   @staticmethod
   def _send_execution_id(id):
      global execution_id
      execution_id = id

   @staticmethod
   def _get_execution_id():
      return execution_id
###################################

### END DEF ###
