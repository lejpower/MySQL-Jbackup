#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-16
#######################
# initial check python version

import sys
import subprocess

try:
   p = sys.version
except subprocess.CalledProcessError as e:
   print(e)
   sys.exit(1)
except Exception as e:
   print(e)
   sys.exit(1)
else:
   version = str(p).split(" ")[0].split(".")[0]

if(int(version) == 2):
   from email.MIMEText import MIMEText
   from email.Utils import formatdate
elif(int(version) >= 3):
   ## from email.MIMEText import MIMEText
   from email.mime.text import MIMEText
else:
   print("Please check Python version!!!")
   sys.exit(1)

import smtplib
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.etc.jbackup_cnf_info import jbackup_cnf_info


class rabackup_send_mail:
### START DEF ###
   def __init__(self, log_file, head_flag):
      err_flag = {1:"ERROR" , 2:"SUCCESS}"}
      self.log_file = log_file
      chk_system = jbackup_cnf_info(self.log_file)
      self.hostname, err_code = chk_system._get_hostname()
      self.from_addr = "${EMAIL}"
      self.to_addr = ["${EMAIL}"]
      self.head = err_flag[head_flag]

   def _create_message(self):
       try:
          tmp = open(self.log_file,'r')
       except Exception as err:
          Logging._logging(self.log_file, str(err))
          sys.exit(1)
       else:
          msg = MIMEText(tmp.read())
       finally:
          tmp.close()
          msg['Subject'] = "[jbackup][" + self.head +"] - " + str(self.hostname)
          msg['From'] = self.from_addr
          msg['To'] = ', '.join(self.to_addr)
          msg['Date'] = formatdate()
       return msg

   def _send(self):
       body = self._create_message()
       s = smtplib.SMTP("localhost", 25)
       to_addr_count = len(self.to_addr)
       num = 0
       Logging._logging(self.log_file, "[Sent Email]")
       for  num in range(to_addr_count):
          try:
             #print("sent")
             s.sendmail(self.from_addr, self.to_addr[num],  body.as_string())
          except Exception as err:
             Logging._logging(self.log_file, str(err))
             sys.exit(1)
          else:
             Logging._logging(self.log_file, str(self.to_addr[num]))
             Logging._logging_blank(self.log_file)
             Logging._logging_blank(self.log_file)
       s.close()
### END DEF ###
