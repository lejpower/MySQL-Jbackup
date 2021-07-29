# -*- coding: utf-8 -*-
from jbackup.lib.con.jbackup_con_mysql import jbackup_con_mysql
from jbackup.lib.con.jbackup_col_sql import jbackup_col_sql
from jbackup.lib.con.jbackup_con_db_management_tool import jbackup_con_db_management_tool
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.chk.jbackup_chk_dir import jbackup_chk_dir
from jbackup.lib.run.jbackup_pre_backup import jbackup_pre_backup
from jbackup.lib.run.jbackup_pre_restore import jbackup_pre_restore
from jbackup.lib.run.jbackup_pre_applylog import jbackup_pre_applylog
from jbackup.lib.chk.jbackup_chk_option import jbackup_chk_option
from jbackup.lib.chk.jbackup_chk_cnffile import jbackup_chk_cnffile
from jbackup.lib.run.jbackup_run_binary import jbackup_run_binary
from jbackup.lib.chk.jbackup_chk_time import jbackup_chk_time
from jbackup.lib.chk.jbackup_chk_system import jbackup_chk_system
from jbackup.lib.etc.jbackup_error import jbackup_error
from jbackup.lib.etc.jbackup_get_date import jbackup_get_date
from jbackup.lib.etc.jbackup_cnf_info import jbackup_cnf_info
from jbackup.lib.etc.jbackup_cnf_info import jbackup_init_value
import sys
import os
import os.path
import subprocess

class jbackup_pre_binary:
   def _exec_binary_backup(self,db_con_mng, init_process, log_file, pid_file, get_time):

      #############################################

      # get backup_end_time
      bk_start_time = get_time._get_now_ymdhms_log()
      Logging._logging(log_file, "jbackup Start Time - " + str(bk_start_time))
      Logging._logging_blank(log_file)

      rb = jbackup_error()
      init_info = init_process._get_init_info(db_con_mng, log_file)

      cl_fqdn = init_info["cl_fqdn"]
      db_management_tool_id = init_info["db_management_tool_id"]

      # create backup_id
      backup_id = get_time._get_execution_id(db_management_tool_id, 1)
      Logging._send_execution_id(backup_id)
      Logging._logging(log_file, "[Backup ID]")
      Logging._logging(log_file, "Issued backup_id ::: " + str(backup_id))
      Logging._logging_blank(log_file)

      chk_dir = jbackup_chk_dir(log_file)
      init_backup_dir, storage_id, security_id = chk_dir._create_init_backup_path(db_management_tool_id, db_con_mng)

      # get current time
      Logging._logging(log_file, "[Check Backup Directory]")
      current_time = get_time._get_current_time()
      ##current_time = jbackup_chk_time._get_current_time(log_file)
      tmp_binlog_backup_dir = chk_dir._create_backup_path(init_backup_dir, current_time, cl_fqdn)
      binlog_backup_dir = os.path.join(tmp_binlog_backup_dir , "binary-log")
      chk_dir._create_dir(binlog_backup_dir)

      # Connect ClientDB
      get_clientDB_info = jbackup_cnf_info(log_file)
      cl_hostname, cl_port, cl_user, cl_password, cl_err_code = get_clientDB_info._get_clientDB(log_file)
      ##cl_hostname, cl_port, cl_user, cl_password = init_process._con_clientDB(log_file)

      # processing message to DB
      backup_type = 0
      db_con_mng._bk_process_to_db(backup_id, db_management_tool_id, cl_fqdn, cl_port, storage_id, security_id, current_time, bk_start_time, backup_type, log_file)

      # get DB information
      Logging._logging_blank(log_file)
      data_dir, cnf_file = init_process._get_db_info(log_file)

      # select queries
      jbackup_sql = jbackup_col_sql()

      # check backup_result table
      chk_tbl_sql = jbackup_sql.check_tbl("backup_result")
      chk_manageDB, chk_manageDB_err_code = db_con_mng._execute(chk_tbl_sql)
      if (chk_manageDB_err_code == 1):
         rb.raise_err(True,1021, log_file)
      #chk_manageDB, chk_manageDB_err_code = db_con_mng._execute("show tables from backup like '%backup_result%';")

      # Connect DB client host
      db_con_cl = jbackup_con_mysql()
      db_con_cl._init_parameter(cl_hostname,cl_port,cl_user,cl_password, log_file)

      # Initial Process END
      #--------------------------------------------------------

      Logging._logging(log_file, "Start jbackup binary backup")

      # Get binlog directory
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Get Binary-log Directory]")
      read_cnf = jbackup_chk_cnffile()
      binlog_dir, binlog_name = read_cnf.get_binary_info_from_cnf(cnf_file, init_process.tmp_binlog_dir, init_process.tmp_binlog_name, log_file)

      # get instance_id from db_management_tool
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check db_management_tool id]")
      Logging._logging(log_file, "db_management_tool_id = " + str(db_management_tool_id))

      # check python version
      chk_sys = jbackup_chk_system(log_file)
      ## py_chk = chk_sys._python_chk(log_file)
      py_ver = chk_sys._python_ver()
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check Python]")
      chk_sys._python_logging()

      # connection check (manageDB)
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check ManageDB]")
      if (len(chk_manageDB) == 0):
         Logging._logging(log_file, "ManageDB connection - [ERROR]")
         rb.raise_err(True,1023, log_file)
      else:
         Logging._logging(log_file, "ManageDB connection - [OK]")

      # check directory
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check directory]")
      if (chk_dir._exist_dir(binlog_dir)):
         Logging._logging(log_file, "binary directory(" + binlog_dir + ") - [OK]")
      else:
         Logging._logging(log_file, "binary directory(" + binlog_dir + ") - [ERROR]")
         rb.raise_err(True,1024, log_file)

      # Flush log
      flush_sql = jbackup_sql.flush_log()
      flush_clientDB, flush_clientDB_err_code = db_con_cl._execute(flush_sql)
      if (flush_clientDB_err_code == 1):
         rb.raise_err(True,1021, log_file)

      # search binary file in directory
      binlog_list = chk_dir.get_binary_log_list(binlog_dir, binlog_name, log_file)

      # cp binary data
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Copy Binary-log]")
      run_binary_backup = jbackup_run_binary()
      binlog_bk_result = run_binary_backup._exec_backup(binlog_list , binlog_backup_dir, log_file)
      if (binlog_bk_result != 0):
          rb.raise_err(True,3013, log_file)
      else:
          binlog_bk_result = 1
      Logging._logging_blank(log_file)

      # (?) mysql purge binlog or clean binlog

      # get backup_end_time
      get_time = jbackup_get_date()
      bk_end_time = get_time._get_now_ymdhms_log()
      Logging._logging(log_file, "jbackup End Time - " + str(bk_end_time))
      Logging._logging_blank(log_file)

      # result to DB
      ##db_con_mng._bk_result_to_db(db_management_tool_id, cl_fqdn, cl_port, storage_id, security_id, current_time, new_backup_dir_name, bk_start_time, bk_end_time, log_file)
      db_con_mng._binlog_bk_result_to_db(backup_id, bk_end_time, binlog_bk_result, log_file)

      # remove pid file
      init_process._del_pid(pid_file, log_file)

      Logging._logging_blank(log_file)
      Logging._logging(log_file, "End jbackup binary backup")
      Logging._logging_blank(log_file)
      Logging._logging_blank(log_file)
      Logging._logging_blank(log_file)
