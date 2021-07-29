#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import subprocess
import os
import re
import sys
import os.path
import socket
import configparser
from jbackup.lib.log.jbackup_logging import Logging

class jbackup_init_value():
   def __init__(self):
      # initial arguments
      self.init_conf = "/usr/local/mysql/.cnf/.jbackup.cnf"
      self.tmp_binlog_dir = '/MYSQL/binlog/'
      self.tmp_binlog_name = 'binarylog'
      # log directory
      self.backup_log_dir = "/usr/local/mysql/backup/NFS"

   def _get_init_value(self):
      return self.init_conf , self.tmp_binlog_dir, self.tmp_binlog_name, self.backup_log_dir

class jbackup_cnf_info():
   def __init__(self, log_file):
      init_value = jbackup_init_value()
      self.init_conf , self.tmp_binlog_dir, self.tmp_binlog_name, self.backup_log_dir = init_value._get_init_value()
      self.log_file = log_file

   def _con_manageDB(self):
      err_code = 0
      Logging._logging(self.log_file, "[Get manageDB information]")
      if (os.path.isfile(self.init_conf)):
         try:
            conf_file = configparser.ConfigParser()
            conf_file.read(self.init_conf)
         except configparser.Error as err:
            # self.rb.raise_err(True,1009,self.log_file)
            err_code = 1009
         except Exception as err:
            # self.rb.raise_err(True,1009,self.log_file)
            err_code = 1009
         else:
            mng_hostname = conf_file.get("manageDB","hostname")
            mng_port     = conf_file.get("manageDB","port")
            mng_user     = conf_file.get("manageDB","user")
            mng_password = conf_file.get("manageDB","password")
            Logging._logging(self.log_file, "Succeed in getting manageDB information!")
      else:
         Logging._logging(self.log_file, "Please check cnf file!")
         #self.rb.raise_err(True,1009,self.log_file)
         err_code = 1009

      Logging._logging_blank(self.log_file)
      return (mng_hostname, mng_port, mng_user, mng_password, err_code)

   def _con_clientDB(self):
      err_code = 0
      Logging._logging(self.log_file, "[Get clientDB information]")
      if (os.path.isfile(self.init_conf)):
         try:
            conf_file = configparser.ConfigParser()
            conf_file.read(self.init_conf)
         except configparser.Error as err:
            #self.rb.raise_err(True,1010,self.log_file)
            err_code = 1010
         except Exception as err:
            #self.rb.raise_err(True,1010,self.log_file)
            err_code = 1010
         else:
            cl_hostname = conf_file.get("clientDB","hostname")
            cl_port     = conf_file.get("clientDB","port")
            cl_user     = conf_file.get("clientDB","user")
            cl_password = conf_file.get("clientDB","password")
            Logging._logging(self.log_file, "Succeed in getting clientDB information!")
      else:
         Logging._logging(log_file, "Please check cnf file!")
         #self.rb.raise_err(True,1010,self.log_file)
         err_code = 1010
      return (cl_hostname, cl_port, cl_user, cl_password, err_code)

   def _get_manageDB(self, log_file):
       mng_hostname, mng_port, mng_user, mng_password, err_code = self._con_manageDB()
       return mng_hostname, mng_port, mng_user, mng_password, err_code

   def _get_clientDB(self, log_file):
       cl_hostname, cl_port, cl_user, cl_password, err_code = self._con_clientDB()
       return cl_hostname, cl_port, cl_user, cl_password, err_code

   def _get_hostname(self):
      try:
         name = os.uname()[1]
      except:
         try:
            name = socket.gethostbyname(socket.gethostname())
         except Exception as err:
            Logging._logging(self.log_file, "Can not get hostname")
            Logging._logging(self.log_file, str(err))
            err_code = 1
      else:
         err_code = 0

      return name , err_code
###################################

### END DEF ###
