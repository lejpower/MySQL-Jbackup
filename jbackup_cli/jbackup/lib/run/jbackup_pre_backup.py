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
from jbackup.lib.etc.jbackup_cnf_info import jbackup_cnf_info
from jbackup.lib.etc.jbackup_cnf_info import jbackup_init_value
from jbackup.lib.etc.jbackup_error import jbackup_error
import sys
import os
import os.path
import shutil
import configparser

class jbackup_pre_backup:
   def _exec_backup(self, db_con_mng, init_process, log_file, pid_file, get_time):

      #--------------------------------------------------------
      # Initial Process START

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
##      current_time = jbackup_chk_time._get_current_time(log_file)
      current_time = get_time._get_current_time()
      backup_dir = chk_dir._create_backup_path(init_backup_dir, current_time, cl_fqdn)
      chk_dir._create_dir(backup_dir)

      # Connect ClientDB
      get_clientDB_info = jbackup_cnf_info(log_file)
      cl_hostname, cl_port, cl_user, cl_password, cl_err_code = get_clientDB_info._get_clientDB(log_file)
      if (cl_err_code != 0):
         rb.raise_err(False,1010, log_file)

      # processing message to DB
      backup_type = 1
      db_con_mng._bk_process_to_db(backup_id, db_management_tool_id, cl_fqdn, cl_port, storage_id, security_id, current_time, bk_start_time, backup_type, log_file)

      # get DB information
      Logging._logging_blank(log_file)
      data_dir, cnf_file = init_process._get_db_info(log_file)

      # check backup_result table
      chk_manageDB, chk_manageDB_err_code = db_con_mng._execute("show tables from backup like '%backup_result%';")
      if (chk_manageDB_err_code == 1):
         rb.raise_err(True,1021, log_file)

      # get option value
      tmp_option_info, tmp_option_info_err_code = db_con_mng._execute("select * from backup.option_info where db_management_tool_id =" + str(db_management_tool_id) + ";")
      if (tmp_option_info_err_code == 1):
         rb.raise_err(True,1021, log_file)
      lock_wait_timeout = tmp_option_info[0][2]
      lock_wait_threshold = tmp_option_info[0][3]

      # processing message to DB
      ## backup_type = 1
      ## db_con_mng._bk_process_to_db(backup_id, db_management_tool_id, cl_fqdn, cl_port, storage_id, security_id, current_time, bk_start_time, backup_type, log_file)

      # Initial Process END
      #--------------------------------------------------------

      Logging._logging(log_file, "Start jbackup backup")

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
      xtra_ver = chk_backup._chk_backup(py_ver, log_file)

      # connection check (manageDB)
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check ManageDB]")
      if (len(chk_manageDB) == 0):
         Logging._logging(log_file, "ManageDB connection - [ERROR]")
         rb.raise_err(True,1023,log_file)
      else:
         Logging._logging(log_file, "ManageDB connection - [OK]")

      # check directory
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check directory]")
      ## chk_dir._create_dir(backup_dir, log_file)
      if (chk_dir._exist_dir(backup_dir)):
         Logging._logging(log_file, "backup directory(" + backup_dir + ") - [OK]")
      else:
         Logging._logging(log_file, "backup directory(" + backup_dir + ") - [ERROR]")
         rb.raise_err(True,1025,log_file)

      ## if (chk_dir._exist_dir(backup_log_dir)):
      ##   Logging._logging(log_file, "backup log base directory(" + backup_log_dir + ") - [OK]")
      ## else:
      ##    Logging._logging(log_file, "backup log base directory(" + backup_log_dir + ") - [ERROR]")
      ##   raise SystemExit

      if (chk_dir._exist_dir(data_dir)):
         Logging._logging(log_file, "data directory(" + data_dir + ") - [OK]")
      else:
         Logging._logging(log_file, "data directory(" + data_dir + ") - [ERROR]")
         rb.raise_err(True,1025,log_file)

      # check disk-size
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check disk(source)] - " + data_dir)
      chk_disk = jbackup_chk_disk()
      chk_disk._size_chk(data_dir, log_file)
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check disk(storage)] - " + backup_dir)
      chk_disk._size_chk(backup_dir, log_file)

      # check CPU count
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check CPU]")
      cpu_cnt = chk_sys._cpu_chk()
      Logging._logging(log_file, "CPU COUNT  - " + str(cpu_cnt))
      para_cnt = chk_sys._get_para_opt()
      Logging._logging(log_file, "Select backup option (--parallel) - " + str(para_cnt))

      # check MySQL
      db_con_cl = jbackup_con_mysql()
      db_con_cl._init_parameter(cl_hostname,cl_port,cl_user,cl_password, log_file)

      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check Mysql process]")
      local_mysql_chk = db_con_cl._local_mysql_chk()
      Logging._logging_blank(log_file)

      ### Now, It is skipping !!!###
      # # check Max DB size
      # Logging._logging_blank(log_file)
      # Logging._logging(log_file, "[Check max database size]")
      # chk_tbl_size = db_con_cl._tbl_size_chk(log_file)
      # chk_disk._compare_tbl_size(chk_tbl_size,log_file)
      ### Now, It is skipping !!!###

      # check files
      Logging._logging(log_file, "[Check files]")
      if (chk_dir._exist_file(cnf_file)):
         Logging._logging(log_file, "conf file(" + cnf_file + ") - [OK]")
      else:
         Logging._logging(log_file, "conf file(" + cnf_file + ") - [ERROR]")
         rb.raise_err(True,1027,log_file)

      # execute backup
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Execute backup cmd]")
      run_backup = jbackup_run_backup()
      run_backup._exec_backup(cl_user , cl_password, cl_hostname, cl_port, cnf_file, backup_dir, para_cnt,log_file, lock_wait_timeout, lock_wait_threshold, xtra_ver)
      Logging._logging_blank(log_file)

      # rename backup directory
      new_backup_dir_name = chk_dir._move_dir(backup_dir, log_file)

      # Copy conf file to backup_dir
      Logging._logging_blank(log_file)
      ori_cnf = os.path.join(backup_dir,new_backup_dir_name,"original.cnf")
      try:
         shutil.copy(cnf_file , ori_cnf)
      except Exception as e:
         Logging._logging(log_file, str(e))
         rb.raise_err(True,1028,log_file)
      else:
         Logging._logging(log_file, "conf file copied - " + str(ori_cnf))
         Logging._logging_blank(log_file)

      # get backup_end_time
      get_time = jbackup_get_date()
      bk_end_time = get_time._get_now_ymdhms_log()
      Logging._logging(log_file, "jbackup End Time - " + str(bk_end_time))
      Logging._logging_blank(log_file)

      # 20160908 - edit by juni #
      Logging._logging(log_file,"--------------------")
      Logging._logging(log_file, "before - _bk_process_to_db")
      Logging._logging(log_file,"--------------------")
      # 20160908 - edit by juni #

      # result to DB
      db_con_mng._bk_result_to_db(backup_id, new_backup_dir_name, bk_end_time, log_file)

      # remove pid file
      init_process._del_pid(pid_file, log_file)

      Logging._logging(log_file, "End jbackup backup")
      Logging._logging_blank(log_file)
      Logging._logging_blank(log_file)
      Logging._logging_blank(log_file)
