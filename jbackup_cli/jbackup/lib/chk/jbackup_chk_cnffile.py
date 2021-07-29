#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import os
import os.path
import copy
import ConfigParser
from collections import OrderedDict
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.etc.jbackup_error import jbackup_error

class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict, self).__setitem__(key, value)

class jbackup_chk_cnffile:
### START DEF ###

   def __init__(self):
       self.rb = jbackup_error()

   # get any information from Mysql cnf file
   def get_binary_info_from_cnf(self, cnf_file,tmp_binlog_dir, tmp_binlog_name, log_file):
      if (os.path.isfile(cnf_file)):
         try:
            parser = ConfigParser.RawConfigParser(dict_type = MultiOrderedDict, allow_no_value=True)
            parser.read(cnf_file)
         except ConfigParser.Error as err:
            Logging._logging(log_file, str(err))
            self.rb.raise_err(True,1027,log_file)
         except Exception as err:
            Logging._logging(log_file, str(err))
            self.rb.raise_err(True,1027,log_file)
         else:
            try:
               item = parser.get("mysqld","log-bin")[0]
            except ConfigParser.NoOptionError:
               tmp_flag = 0
            else:
               tmp_flag = 1

            if (tmp_flag == 1):
                try:
                   binlog_dir = os.path.split(item)[0]
                   binlog_name = os.path.split(item)[1]
                except Exception as err:
                   Logging._logging(log_file, str(err))
                   Logging._logging(log_file, "It can not find log-bin option in the conf file!")
                   binlog_dir = tmp_binlog_dir
                   binlog_name = tmp_binlog_name
                   Logging._logging(log_file, "Setting default log-bin directory : " + binlog_dir)
                else:
                   Logging._logging(log_file, "log-bin directory = " + str(binlog_dir))
            elif (tmp_flag == 0):
               Logging._logging(log_file, "It can not find log-bin option in the conf file!")
               binlog_dir = tmp_binlog_dir
               binlog_name = tmp_binlog_name
               Logging._logging(log_file, "Setting default log-bin directory : " + binlog_dir)
      else:
         Logging._logging(log_file, "Can not get MySQL configuration file!!!")
         binlog_dir = tmp_binlog_dir
         binlog_name = tmp_binlog_name
         Logging._logging(log_file, "Setting default log-bin directory : " + binlog_dir)

      return binlog_dir , binlog_name



   def get_restore_info_from_cnf(self, cnf_file, item, log_file):
      if (os.path.isfile(cnf_file)):
         try:
            parser = ConfigParser.RawConfigParser(dict_type = MultiOrderedDict, allow_no_value=True)
            parser.read(cnf_file)
         except ConfigParser.Error as err:
            self.rb.raise_err(True,1027,log_file)
         except Exception as err:
            self.rb.raise_err(True,1027,log_file)
         else:
            try:
                result = parser.get("mysqld",item)[0]
            except ConfigParser.NoOptionError:
                Logging._logging(log_file, "It can not find " + str(item) + " option in the conf file!")
                Logging._logging(log_file, "cnf file : " + str(cnf_file))
                self.rb.raise_err(True,3009,log_file)
            except Exception as err:
                Logging._logging(log_file, "It can not find " + str(item) + " option in the conf file!")
                Logging._logging(log_file, "cnf file : " + str(cnf_file))
                self.rb.raise_err(True,3009,log_file)
            else:
                Logging._logging(log_file, str(item) + " directory = " + str(result))
            finally:
                if (result == '' or result == u'' ):
                   Logging._logging(log_file, "It can not find " + str(item) + " option in the conf file!")
                   Logging._logging(log_file, "cnf file : " + str(cnf_file))
                   self.rb.raise_err(True,3009,log_file)
      else:
         Logging._logging(log_file, "Can not get MySQL configuration file!!!")
         Logging._logging(log_file, "cnf file : " + str(cnf_file))
         self.rb.raise_err(True,1027,log_file)

      return os.path.join(item,result)


   def edit_original_cnf(self, cnf_file, target, log_file):
      # innodb_data_home_dir , innodb_buffer_pool size, server_id
      if (target == "svr_id"):
         item = 'server_id'
         replace_item, err_code = self.cnf_search_item(item, cnf_file, log_file)
         textToReplace = 'server_id = 9999\n'
         if (err_code == 0):
            self.cnf_replace_item(cnf_file, replace_item, textToReplace)
         else:
            pass
      elif (target == "in_buf"):
         item = 'innodb_buffer_pool_size'
         replace_item, err_code = self.cnf_search_item(item, cnf_file, log_file)
         buff_size = self.calculate_buff()
         textToReplace = 'innodb_buffer_pool_size                 = ' + str(buff_size) + 'G\n'
         if (err_code == 0):
            self.cnf_replace_item(cnf_file, replace_item, textToReplace)
         else:
            pass
      elif (target == "in_home_dir"):
         item1 = 'innodb_data_file_path'
         item2 = 'innodb_data_home_dir'
         replace_item1, err_code1 = self.cnf_search_item(item1, cnf_file, log_file)
         inno_home_dir, inno_data_value = self.cnf_create_dir(replace_item1)
         textToReplace1 = item1 + " = " + inno_data_value + "\n"
         textToReplace2 = item2 + " = " + inno_home_dir + "\n"
         replace_item2, err_code2 = self.cnf_search_item(item2, cnf_file, log_file)

         if (err_code1 == 0 and err_code2 == 0 and replace_item2.split("=")[1].replace(" ", "") in ['\n', ' ']):
            self.cnf_replace_item(cnf_file, replace_item1, textToReplace1)
            self.cnf_replace_item(cnf_file, replace_item2, textToReplace2)
         else:
            pass


   def cnf_search_item(self, item, cnf_file, log_file):
      replace_item = " "
      with open(cnf_file, 'r') as inF:
         for line in inF:
            if item in line:
               replace_item = line

      if(replace_item != " "):
         err_code = 0
      else:
         Logging._logging(log_file, "Can not find to replace an item in the original.cnf")
         Logging._logging(log_file, "Please check :: " + item)
         err_code = 1
      return replace_item , err_code


   def cnf_replace_item(self, cnf_file, replace_item, textToReplace):
      f1=open(cnf_file,'r').read()
      f2=open(cnf_file,'w')
      m=f1.replace(replace_item,textToReplace)
      f2.write(m)
      f2.close()


   def cnf_create_dir(self, replace_item):
      if(replace_item == ""):
          self.rb.raise_err(True,3010,log_file)

      tmp = replace_item.split('=')[1]
      original_tmp = copy.copy(tmp)
      tmp.replace(" ","")
      tmp.replace("\"","")
      tmp.replace("\'","")

      tmp = tmp.split(':')[0]
      inrequire_cnt = 0
      path_cnt = 0
      for s in tmp:
        if (s != "/"):
          inrequire_cnt = inrequire_cnt + 1
        else:
          break;

      for s in tmp:
         if (s == "/"):
            path_cnt = path_cnt + 1

      tmp = tmp[inrequire_cnt:]
      tmp_split = tmp.split("/")
      inno_home_dir = "/"
      for t in range(path_cnt):
          inno_home_dir = os.path.join(inno_home_dir, tmp_split[t])

      inno_data_value = original_tmp.replace((inno_home_dir + "/"), "")
      return inno_home_dir, inno_data_value


   def calculate_buff(self):
      mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
      mem_gib = mem_bytes/(1024.**3)
      buff_size = int(mem_gib*0.75)
      return buff_size
### END DEF ###
