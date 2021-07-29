# -*- coding: utf-8 -*-
import sys
import os
import os.path
import shutil
import configparser
from jbackup.lib.con.jbackup_con_mysql import jbackup_con_mysql
from jbackup.lib.con.jbackup_con_db_management_tool import jbackup_con_db_management_tool
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.chk.jbackup_chk_dir import jbackup_chk_dir
from jbackup.lib.chk.jbackup_chk_disk import jbackup_chk_disk
from jbackup.lib.chk.jbackup_chk_cnffile import jbackup_chk_cnffile
from jbackup.lib.chk.jbackup_chk_system import jbackup_chk_system
from jbackup.lib.chk.jbackup_chk_backup import jbackup_chk_backup
from jbackup.lib.chk.jbackup_chk_restore import jbackup_chk_restore
from jbackup.lib.run.jbackup_run_restore import jbackup_run_restore
from jbackup.lib.etc.jbackup_error import jbackup_error
from jbackup.lib.etc.jbackup_get_date import jbackup_get_date
from jbackup.lib.etc.jbackup_cnf_info import jbackup_cnf_info
from jbackup.lib.etc.jbackup_cnf_info import jbackup_init_value


class jbackup_pre_restore:
   def _exec_restore(self, db_con_mng, init_process, log_file, pid_file, restore_dir, get_time):

      #--------------------------------------------------------
      # Initial Process START

      # get restore_start_time
      restore_start_time = get_time._get_now_ymdhms_log()
      Logging._logging(log_file, "jbackup Start Time - " + str(restore_start_time))
      Logging._logging_blank(log_file)

      rb = jbackup_error()
      init_info = init_process._get_init_info(db_con_mng, log_file)

      cl_fqdn = init_info["cl_fqdn"]
      db_management_tool_id = init_info["db_management_tool_id"]

      # create restore_id
      # backup_idとid生成ロジックが同じので、_get_execution_idを利用[今後メソッド名等修正した方がよい]
      restore_id = get_time._get_execution_id(db_management_tool_id, 2)
      Logging._send_execution_id(restore_id)
      Logging._logging(log_file, "[Restore ID]")
      Logging._logging(log_file, "Issued restore_id ::: " + str(restore_id))
      Logging._logging_blank(log_file)

      # Connect ClientDB
      get_clientDB_info = jbackup_cnf_info(log_file)
      cl_hostname, cl_port, cl_user, cl_password, cl_err_code = get_clientDB_info._get_clientDB(log_file)

      chk_dir = jbackup_chk_dir(log_file)
      init_backup_dir, storage_id, security_id = chk_dir._create_init_backup_path(db_management_tool_id, db_con_mng)

      if (restore_dir[-1:] == '/'):
         get_applylog_result = restore_dir[:-1].split('/')[-5:]
      else:
         get_applylog_result = restore_dir.split('/')[-5:]

      # processing message to DB
      db_con_mng._restore_process_to_db(restore_id, db_management_tool_id, cl_fqdn, storage_id, security_id, get_applylog_result, restore_start_time, log_file)

      # get restore info'
      chk_restore = jbackup_chk_restore()
      restore_cnf_sql = "select restore_cnf from backup.restore_info where db_management_tool_id =" + str(db_management_tool_id)

      # change restore_cnf in DB -> original.cnf
      cnf_file = os.path.join(restore_dir , 'original.cnf')
      restore_target_dir = chk_restore._get_restore_dir(cnf_file, log_file)

      # Initial Process END
      #--------------------------------------------------------

      ## # Starting Logging
      Logging._logging(log_file, "Start jbackup restore")

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

      # check directory
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check directory]")
      if (chk_dir._exist_dir(restore_dir)):
         Logging._logging(log_file, "backup/applylog directory(" + restore_dir + ") - [OK]")
      else:
         Logging._logging(log_file, "backup/applylog directory(" + restore_dir + ") - [ERROR]")
         rb.raise_err(True,1025, log_file)

      if (chk_dir._exist_dir(restore_target_dir)):
         Logging._logging(log_file, "target directory(" + restore_target_dir + ") - [OK]")
      else:
         Logging._logging(log_file, "target directory(" + restore_target_dir + ") - [ERROR]")
         rb.raise_err(True,1025, log_file)

      # check disk-size
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check disk]")
      chk_disk = jbackup_chk_disk()
      chk_disk._size_chk(restore_target_dir, log_file)

      # check files
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Check files]")
      if (chk_dir._exist_file(cnf_file)):
         Logging._logging(log_file, "conf file(" + cnf_file + ") - [OK]")
      else:
         Logging._logging(log_file, "conf file(" + cnf_file + ") - [ERROR]")
         rb.raise_err(True,1027, log_file)

      # innodb_data_home_dir , innodb_buffer_pool size, server_id
      read_cnf = jbackup_chk_cnffile()
      target = ["svr_id" , "in_buf", "in_home_dir"]
      for i in target:
          read_cnf.edit_original_cnf(cnf_file, i, log_file)

      # execute restore
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Execute restore cmd]")

      # get directory info from mysql cnf
      run_restore = jbackup_run_restore()
      innodb_data_dir = read_cnf.get_restore_info_from_cnf(cnf_file, "innodb_data_home_dir", log_file)
      innodb_log_dir = read_cnf.get_restore_info_from_cnf(cnf_file, "innodb_log_group_home_dir", log_file)

      # delete data_dir, innodb_data_dir, innodb_log_dir
      run_restore._remove_dir(restore_target_dir, log_file)
      run_restore._remove_dir(innodb_data_dir, log_file)
      run_restore._remove_dir(innodb_log_dir, log_file)

      # exec restore
      run_restore._exec_restore(cl_user , cl_password, cl_hostname, cl_port, cnf_file, restore_dir, log_file)

      # Copy conf file to restore_dir
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Copy cnf_file]")
      if (os.path.split(restore_target_dir)[0] != "/var/lib"):
         ori_cnf = os.path.join(os.path.split(restore_target_dir)[0],'var','my_' + restore_target_dir.split(os.sep)[2] + '.cnf')
      else:
         ori_cnf = os.path.join(restore_target_dir, "my.cnf")

      try:
        shutil.copy(cnf_file , ori_cnf)
      except Exception as e:
         Logging._logging(log_file, str(e))
         rb.raise_err(True,1028, log_file)
      else:
         Logging._logging(log_file, "conf file copied from original.cnf - " + str(ori_cnf))
         Logging._logging_blank(log_file)

      # Chown mysql user for restore_dir
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Chown MYSQL user and group]")
      chk_dir.exec_chown(restore_target_dir)

      # get restore_end_time
      get_time         = jbackup_get_date()
      restore_end_time = get_time._get_now_ymdhms_log()
      Logging._logging(log_file, "jbackup End Time - " + str(restore_end_time))
      Logging._logging_blank(log_file)

      # result to DB
      Logging._logging_blank(log_file)
      db_con_mng._restore_result_to_db(restore_id, get_applylog_result, restore_end_time, log_file)

      # remove pid file
      init_process._del_pid(pid_file, log_file)

      Logging._logging(log_file, "End jbackup backup")
      Logging._logging_blank(log_file)
      Logging._logging_blank(log_file)
      Logging._logging_blank(log_file)

#--------------------------------------------------------
