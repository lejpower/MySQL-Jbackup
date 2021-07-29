#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import os
import os.path
import subprocess
from jbackup.lib.etc.jbackup_get_date import jbackup_get_date
from jbackup.lib.etc.jbackup_error import jbackup_error
from jbackup.lib.log.jbackup_logging import Logging

class jbackup_search_info:
### START DEF ###
   def __init__(self, item, log_file):
      self.rb = jbackup_error()
      self.log_file = log_file
      self.info = []
      if (item == "backup"):
         ##keep_phrases = ["Created backup directory",
         keep_phrases = ["Executing FLUSH TABLES WITH READ LOCK",
                        "Starting to backup non-InnoDB",
                        "Transaction log of lsn",
                        "All tables unlocked",
                        "backup - [OK]",
                        "backup_directory ="]
      elif (item == "applylog"):
         keep_phrases = ["decompress - [OK]",
                        "remove qp files - [OK]",
                        "apply-log - [OK]"]
      elif (item == "restore"):
         keep_phrases = ["restore - [OK]"]

      with open(log_file) as f:
         f = f.readlines()

      for phrase in keep_phrases:
         for line in f:
            if phrase in line:
               self.info.append(line)
               break

      if (len(keep_phrases) != len(self.info)):
         self.rb.raise_err(True,3012, self.log_file)
      else:
         pass

   def _get_applylog_result(self, item):
      #applylog results
      if (item == "decompress"):
         if (self.info[0].split(" ")[5].split('\n')[0] == "[OK]"):
            result = 1
         else:
            result = 0
      elif (item == "remove_qp"):
         if (self.info[0].split(" ")[5].split('\n')[0] == "[OK]"):
            result = 1
         else:
            result = 0
      elif (item == "applylog"):
         if (self.info[0].split(" ")[5].split('\n')[0] == "[OK]"):
            result = 1
         else:
            result = 0

      return result

   def _get_restore_result(self):
      #restore results
      if (self.info[0].split(" ")[5].split('\n')[0] == "[OK]"):
         result = 1
      else:
         result = 0

      return str(result)

   def _get_ftwrl(self):
      # lock time
      tmp_exec_FTWRL = self.info[0].split(" ")[3:5]
      exec_FTWRL = tmp_exec_FTWRL[0] + " " + tmp_exec_FTWRL[1]
      return exec_FTWRL

   def _get_lock_start(self):
      tmp_locked_tbl = self.info[1].split(" ")[3:5]
      locked_tbl = tmp_locked_tbl[0] + " " + tmp_locked_tbl[1]
      return locked_tbl

   def _get_tran_info(self):
      # transaction log
      tmp_tran = self.info[2].split(" ")
      start_tran = tmp_tran[8][1:][:-1]
      end_tran = tmp_tran[10][1:][:-1]
      return start_tran , end_tran

   def _get_lock_end(self):
      tmp_unlocked_tbl = self.info[3].split(" ")[3:5]
      unlocked_tbl = tmp_unlocked_tbl[0] + " " + tmp_unlocked_tbl[1]
      return unlocked_tbl

   def _get_backup_result(self):
      #backup results
      if (self.info[4].split(" ")[5].split('\n')[0] == "[OK]"):
         result = 1
      else:
         result = 0

      return str(result)

   def _get_backup_result_dir(self):
      #backup result directory
      backup_result_dir = self.info[5].split(" ")[5].split('\n')[0]
      return backup_result_dir

###################################

### END DEF ###
