# -*- coding: utf-8 -*-
from jbackup.lib.con.jbackup_con_mysql import jbackup_con_mysql
from jbackup.lib.con.jbackup_con_db_management_tool import jbackup_con_db_management_tool
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.log.jbackup_search_info import jbackup_search_info
from jbackup.lib.chk.jbackup_chk_dir import jbackup_chk_dir
from jbackup.lib.chk.jbackup_chk_disk import jbackup_chk_disk
from jbackup.lib.chk.jbackup_chk_system import jbackup_chk_system
from jbackup.lib.chk.jbackup_chk_time import jbackup_chk_time
from jbackup.lib.chk.jbackup_chk_backup import jbackup_chk_backup
from jbackup.lib.etc.jbackup_get_date import jbackup_get_date
from jbackup.lib.run.jbackup_run_backup import jbackup_run_backup
from jbackup.lib.etc.jbackup_error import jbackup_error
import sys
import os
import os.path
import configparser

class jbackup_run_remove:
   def _exec_remove(self, db_con_mng, init_process, log_file, pid_file, opt, opt_flag, get_time):

      #--------------------------------------------------------
      # Initial Process START
      # rb = jbackup_error(log_file)
      init_info = init_process._get_init_info(db_con_mng, log_file)

      # get backup_end_time
      bk_start_time = get_time._get_now_ymdhms_log()
      Logging._logging(log_file, "jbackup Start Time - " + str(bk_start_time))
      Logging._logging_blank(log_file)

      cl_fqdn = init_info["cl_fqdn"]
      db_management_tool_id = init_info["db_management_tool_id"]

      chk_dir = jbackup_chk_dir(log_file)
      init_backup_dir, storage_id, security_id = chk_dir._create_init_backup_path(db_management_tool_id, db_con_mng)

      if (opt_flag == 1):
         bf_day = opt

         # get target date
         Logging._logging(log_file, "[Remove Previous Backup Directory Using Date]")
         before_time = get_time._get_before_time(bf_day)
         ##before_time = jbackup_chk_time._get_before_time(log_file, bf_day)
         remove_dir = chk_dir._create_remove_path_date(init_backup_dir, before_time, cl_fqdn)
         Logging._logging(log_file, "remove target directory : " + str(remove_dir))

         if (chk_dir._exist_dir(remove_dir)):
            chk_dir._rm_dir(remove_dir)
         else:
            Logging._logging(log_file, "Can not find remove_dir!")
      elif (opt_flag == 2):
         gene = opt

         # get target date
         Logging._logging(log_file, "[Remove Previous Backup Directory Using Generation]")
         current_time = get_time._get_current_time( )
         ##current_time = jbackup_chk_time._get_current_time(log_file)
         chk_dir._create_remove_path_gene(init_backup_dir, current_time, gene, cl_fqdn)
         ## Logging._logging(log_file, "remove target directory : " + str(remove_dir))

      else:
         Logging._logging(log_file, "Something wrong to give argument!")

      # get backup_end_time
      get_time = jbackup_get_date()
      Logging._logging_blank(log_file)
      bk_end_time = get_time._get_now_ymdhms_log()
      Logging._logging(log_file, "jbackup End Time - " + str(bk_end_time))
      Logging._logging_blank(log_file)

      # remove pid file
      init_process._del_pid(pid_file, log_file)

      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Finish - Remove Previous Backup Directory]")
      Logging._logging_blank(log_file)

      #################################
