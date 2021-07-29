# -*- coding: utf-8 -*-
import sys
import os
import os.path
import configparser
from jbackup.lib.con.jbackup_con_mysql import jbackup_con_mysql
from jbackup.lib.con.jbackup_con_db_management_tool import jbackup_con_db_management_tool
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.chk.jbackup_chk_dir import jbackup_chk_dir
from jbackup.lib.chk.jbackup_chk_disk import jbackup_chk_disk
from jbackup.lib.chk.jbackup_chk_system import jbackup_chk_system
from jbackup.lib.chk.jbackup_chk_backup import jbackup_chk_backup
from jbackup.lib.run.jbackup_run_applylog import jbackup_run_applylog
from jbackup.lib.con.jbackup_col_sql import jbackup_col_sql
from jbackup.lib.etc.jbackup_error import jbackup_error
from jbackup.lib.etc.jbackup_get_date import jbackup_get_date
from jbackup.lib.etc.jbackup_cnf_info import jbackup_cnf_info
from jbackup.lib.etc.jbackup_cnf_info import jbackup_init_value

class jbackup_pre_applylog:
   def _exec_applylog(self, db_con_mng, init_process, log_file, pid_file, applylog_dir, get_time):

      #--------------------------------------------
      # Initial Process START

      # get backup_end_time
      bk_start_time = get_time._get_now_ymdhms_log()
      Logging._logging(log_file, "jbackup Start Time - " + str(bk_start_time))
      Logging._logging_blank(log_file)

      rb = jbackup_error()
      init_info = init_process._get_init_info(db_con_mng, log_file)

      cl_fqdn = init_info["cl_fqdn"]
      db_management_tool_id = init_info["db_management_tool_id"]

      # Starting Logging
      cnf_file = os.path.join(applylog_dir, "backup-my.cnf")

      # Connect ClientDB
      get_clientDB_info = jbackup_cnf_info(log_file)
      cl_hostname, cl_port, cl_user, cl_password, cl_err_code = get_clientDB_info._get_clientDB(log_file)

      chk_dir = jbackup_chk_dir(log_file)
      chk_sql = jbackup_col_sql()

      init_backup_dir, storage_id, security_id = chk_dir._create_init_backup_path(db_management_tool_id, db_con_mng)

      # get backup date from applylog_dir
      if (applylog_dir[-1:] == '/'):
          get_backup_result = applylog_dir[:-1].split('/')[-5:]
      else:
          get_backup_result = applylog_dir.split('/')[-5:]

      # Initial Process END
      #--------------------------------------------------------

      Logging._logging(log_file, "Start jbackup apply-log")

      # get instance_id from db_management_tool
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check db_management_tool id]")
      Logging._logging(log_file, "db_management_tool_id = " + str(db_management_tool_id))

      # check python version
      chk_sys = jbackup_chk_system(log_file)
      py_ver = chk_sys._python_ver()
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check Python]")
      chk_sys._python_logging()

      #check backup package
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check Backup Package]")
      chk_backup = jbackup_chk_backup()
      chk_backup._chk_backup(py_ver, log_file)

      # check files
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check files]")
      if (chk_dir._exist_file(cnf_file) == 0 or chk_dir._exist_file(cnf_file + ".qp") == 0 ):
        Logging._logging(log_file, "conf file(" + cnf_file + ") - [OK]")
      else:
        Logging._logging(log_file, "conf file(" + cnf_file + ") - [ERROR]")
        rb.raise_err(False,1027, log_file)

      # execute decompress
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Execute decompress]")
      run_applylog = jbackup_run_applylog()
      run_applylog._exec_decomp(applylog_dir,log_file)
      Logging._logging_blank(log_file)

      # execute apply-log
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Execute apply-log]")
      run_applylog._exec_applylog(cl_user , cl_password, cl_hostname, cnf_file, applylog_dir, log_file)
      Logging._logging_blank(log_file)

      # get backup_end_time
      get_time = jbackup_get_date()
      bk_end_time = get_time._get_now_ymdhms_log()
      Logging._logging(log_file, "jbackup End Time - " + str(bk_end_time))
      Logging._logging_blank(log_file)

      # result to DB
      db_con_mng._applylog_result_to_db(db_management_tool_id, cl_fqdn, cl_port, storage_id, security_id, get_backup_result, log_file)
      Logging._logging_blank(log_file)

      # remove pid file
      init_process._del_pid(pid_file, log_file)

      Logging._logging(log_file, "End jbackup apply-log")
      Logging._logging_blank(log_file)
      Logging._logging_blank(log_file)
      Logging._logging_blank(log_file)
