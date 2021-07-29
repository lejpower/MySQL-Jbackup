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
from jbackup.lib.etc.jbackup_error import jbackup_error
from jbackup.lib.chk.jbackup_chk_time import jbackup_chk_time
from jbackup.lib.etc.jbackup_cnf_info import jbackup_cnf_info
from jbackup.lib.etc.jbackup_cnf_info import jbackup_init_value
import sys
import os
import os.path
import subprocess

class jbackup_run_check:
   def _exec_check(self,db_con_mng, init_process, pid_file, log_file, get_time):

      rb = jbackup_error()
      init_info = init_process._get_init_info(db_con_mng, log_file)

      cl_fqdn = init_info["cl_fqdn"]
      db_management_tool_id = init_info["db_management_tool_id"]

      # check current time
      current_time = get_time._get_current_time()
      ##current_time = jbackup_chk_time._get_current_time(log_file)

      shrt_cl_fqdn = cl_fqdn.split(".")[0]

      # Connect ClientDB
      get_clientDB_info = jbackup_cnf_info(log_file)
      cl_hostname, cl_port, cl_user, cl_password, cl_err_code = get_clientDB_info._get_clientDB(log_file)

      chk_dir = jbackup_chk_dir(log_file)
      chk_sql = jbackup_col_sql()

      backup_chk_sql = chk_sql.backup_chk_sql(cl_fqdn, current_time)

      tmp_backup_chk, tmp_backup_chk_err_code = db_con_mng._execute(backup_chk_sql)
      if (tmp_backup_chk_err_code == 1):
         rb.raise_err(False,1021, log_file)

      restore_chk_sql = chk_sql.restore_chk_sql(cl_fqdn, current_time)
      tmp_restore_chk, tmp_restore_chk_err_code = db_con_mng._execute(restore_chk_sql)
      if (tmp_restore_chk_err_code == 1):
         rb.raise_err(False,1021, log_file)

      #time_check
      tm_chk = jbackup_chk_time()

      Logging._logging(log_file, "[Check operation flag]")
      if (tmp_backup_chk_err_code == 0):
         bk_book_id = tmp_backup_chk[0][0]
         backup_host = tmp_backup_chk[0][1]
         full_backup_flag = tmp_backup_chk[0][2]
         backup_time = tmp_backup_chk[0][3]

         backup_flag = tm_chk._chk_time(backup_time, log_file , "backup")
         Logging._logging(log_file, "backup operation flag = " + str(backup_flag))
      else:
         backup_flag = 0
         full_backup_flag = 0
         Logging._logging(log_file, "backup operation flag = " + str(backup_flag))

      # Flag check
      if (tmp_restore_chk_err_code == 0):
         restore_id = tmp_restore_chk[0][0]
         dst_host = tmp_restore_chk[0][1]
         src_dir = tmp_restore_chk[0][2]
         restore_time = tmp_restore_chk[0][3]
         # id,dst_host,src_dir,restore_time

         restore_flag = tm_chk._chk_time(restore_time, log_file, "restore")
         Logging._logging(log_file, "restore operation flag = " + str(restore_flag))
      else:
         restore_flag = 0
         Logging._logging(log_file, "restore operation flag = " + str(restore_flag))

      Logging._logging_blank(log_file)

      # Backup part
      init_flag = 0 # no initial process -> check option flag

      if (backup_flag == 1 and full_backup_flag == 1):
         try:
            sql_retention_period = chk_sql.retention_period(db_management_tool_id)
            tmp_retention_period, tmp_retention_period_err_code = db_con_mng._execute(sql_retention_period)
            if (tmp_retention_period_err_code == 1):
               rb.raise_err(False,1021, log_file)
            init_process._init_process(init_flag , ["backup"])
         except Exception as err:
            Logging._logging(log_file, str(err))
            rb.raise_err(True,7001, log_file)
         else:
            backup_proc = 0

         try:
            init_process._init_process(init_flag , ["remove","-d",str(tmp_retention_period[0][0])])
            #init_process._init_process(init_flag , ["remove","-d","185"])
         except Exception as err:
            Logging._logging(log_file, str(err))
            rb.raise_err(True,7003, log_file)
         else:
            remove_proc = 0

         if (backup_proc == 0 and remove_proc == 0):
            backup_chk_result = chk_sql.backup_chk_result(bk_book_id, cl_fqdn)
            tmp_backup_chk_result, tmp_jbackup_chk_result_err_code = db_con_mng._execute(backup_chk_result)
            if (tmp_jbackup_chk_result_err_code == 1):
               rb.raise_err(True,1021, log_file)
            Logging._logging(log_file, "backup reservation id = " + str(bk_book_id) + " full backup operation finished!")
         else:
            rb.raise_err(True,7001, log_file)
      elif (backup_flag == 1 and full_backup_flag == 0):
         try:
            sql_retention_period = chk_sql.retention_period(db_management_tool_id)
            tmp_retention_period, tmp_retention_period_err_code = db_con_mng._execute(sql_retention_period)
            if (tmp_retention_period_err_code == 1):
                rb.raise_err(False,1021, log_file)

            init_process._init_process(init_flag , ["binary"])
         except Exception as err:
            Logging._logging(log_file, str(err))
            rb.raise_err(True,7002, log_file)
         else:
             binary_proc = 0

         try:
             init_process._init_process(init_flag , ["remove","-d",str(tmp_retention_period[0][0])])
             #init_process._init_process(init_flag , ["remove","-d","185"])
         except Exception as err:
             Logging._logging(log_file, str(err))
             rb.raise_err(True,7003, log_file)
         else:
             remove_proc = 0

         if (binary_proc == 0 and remove_proc == 0):
            backup_chk_result = chk_sql.backup_chk_result(bk_book_id, cl_fqdn)
            tmp_backup_chk_result, tmp_jbackup_chk_result_err_code = db_con_mng._execute(backup_chk_result)
            if (tmp_jbackup_chk_result_err_code == 1):
               rb.raise_err(True,1021, log_file)
            Logging._logging(log_file, "backup_id = " + str(bk_book_id) + " binlog backup operation finished!")
         else:
            rb.raise_err(True,7002, log_file)


      # Restore part
      if (restore_flag == 1):

         ####################
         ## check backup_result -->  backup_status in backup_reservations!!!
         ## chk_sql.restore_bf_chk_bk_result()
         ####################

         try:
            init_process._init_process(init_flag , ["applylog","-d",src_dir])
         except Exception as err:
            Logging._logging(log_file, str(err))
            rb.raise_err(True,7004, log_file)
         else:
            applylog_proc = 0

         try:
            init_process._init_process(init_flag , ["restore","-d",src_dir])
         except Exception as err:
            Logging._logging(log_file, str(err))
            rb.raise_err(True,7005, log_file)
         else:
            restore_proc = 0

         if (applylog_proc == 0 and restore_proc == 0):
            restore_chk_result = chk_sql.restore_chk_result(restore_id, cl_fqdn)
            tmp_backup_chk_result, tmp_jbackup_chk_result_err_code = db_con_mng._execute(restore_chk_result)
            if (tmp_jbackup_chk_result_err_code == 1):
               rb.raise_err(True,1021, log_file)
            Logging._logging(log_file, "restore_id = " + str(restore_id) + " restore operation finished!")
         else:
            rb.raise_err(True,7005, log_file)

      # remove pid file
      init_process._del_pid(pid_file, log_file)

      Logging._logging(log_file, "End jbackup check")
      Logging._logging_blank(log_file)
      Logging._logging_blank(log_file)
      Logging._logging_blank(log_file)
