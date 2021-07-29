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
from jbackup.lib.etc.jbackup_error import jbackup_error
from jbackup.lib.con.jbackup_con_mysql import jbackup_con_mysql
from jbackup.lib.con.jbackup_con_db_management_tool import jbackup_con_db_management_tool
from jbackup.lib.chk.jbackup_chk_dir import jbackup_chk_dir
from jbackup.lib.chk.jbackup_chk_system import jbackup_chk_system
from jbackup.lib.chk.jbackup_chk_option import jbackup_chk_option
from jbackup.lib.run.jbackup_pre_backup import jbackup_pre_backup
from jbackup.lib.run.jbackup_pre_restore import jbackup_pre_restore
from jbackup.lib.run.jbackup_pre_applylog import jbackup_pre_applylog
from jbackup.lib.run.jbackup_pre_binary import jbackup_pre_binary
from jbackup.lib.run.jbackup_run_remove import jbackup_run_remove
from jbackup.lib.run.jbackup_run_check import jbackup_run_check
from jbackup.lib.etc.jbackup_get_date import jbackup_get_date
from jbackup.lib.etc.jbackup_cnf_info import jbackup_cnf_info
from jbackup.lib.etc.jbackup_cnf_info import jbackup_init_value

class jbackup_init():
### START DEF ###
   def __init__(self, argv):
      # initial arguments
      get_init_value = jbackup_init_value()
      self.init_conf , self.tmp_binlog_dir, self.tmp_binlog_name , self.backup_log_dir = get_init_value._get_init_value()
      self.opt_argv = argv

      # selected log file_name
      if (self.opt_argv[0] in ['backup']):
          self.log_file = Logging._create_log_file("backup", self.backup_log_dir)
      elif (self.opt_argv[0] in ['apply-log' , 'applylog']):
          self.log_file = Logging._create_log_file("applylog", self.backup_log_dir)
      elif (self.opt_argv[0] in ['restore']):
          self.log_file = Logging._create_log_file("restore", self.backup_log_dir)
      elif (self.opt_argv[0] in ['check']):
          self.log_file = Logging._create_log_file("check", self.backup_log_dir)
      elif (self.opt_argv[0] in ['remove'] and len(argv) == 3 and (argv[1] in ['-d', '--date','-g','--generation']) ):
          self.log_file = Logging._create_log_file("remove", self.backup_log_dir)
      elif (self.opt_argv[0] in ['binary']):
          self.log_file = Logging._create_log_file("binary", self.backup_log_dir)
      else:
         chk_opt = jbackup_chk_option()
         chk_opt._chk_err()
         sys.exit(1)

      self.rb = jbackup_error()

      self.get_time = jbackup_get_date()

   def _init_process(self, init_flag, check_argv):

      if (init_flag == 1):
          proc_argv = self.opt_argv
          proc_log_file = self.log_file
      elif (init_flag == 0):
          proc_argv = check_argv
          proc_log_file = Logging._create_log_file(check_argv[0], self.backup_log_dir)

      # Starting Logging
      if(len(proc_argv) == 1 and proc_argv[0] in ['backup']):
         pid_file = self._get_pid(self.backup_log_dir, "backup", proc_log_file)
      elif(len(proc_argv) == 4 and proc_argv[0] in ['backup'] and proc_argv[1] in ['--with_remove'] and self.opt_argv[2] in ['-d', '--date','-g', '--generation']):
         # backup
         pid_file = self._get_pid(self.backup_log_dir, "backup", proc_log_file)
         # remove
         if((len(proc_argv) == 4) and (proc_argv[2] in ['-d', '--date']) and int(proc_argv[3]) > 0):
            bf_day = int(proc_argv[3])
            rm_pid_file = self._get_pid(self.backup_log_dir, "remove", proc_log_file)
         elif ((len(proc_argv) == 4) and (proc_argv[2] in ['-g', '--generation']) and int(proc_argv[3]) > 0):
            gene = int(proc_argv[3])
            rm_pid_file = self._get_pid(self.backup_log_dir, "remove", proc_log_file)
      elif(len(proc_argv) == 3 and proc_argv[0] in ['apply-log' , 'applylog']):
         if (proc_argv[1] in ['-d', '--dir']):
            src_dir = str(proc_argv[2])
            pid_file = self._get_pid(self.backup_log_dir, "applylog", proc_log_file)
         else:
            chk_opt = jbackup_chk_option()
            chk_opt._print_help()
            sys.exit(1)
      elif(len(proc_argv) == 3 and proc_argv[0] in ['restore']):
         if (proc_argv[1] in ['-d', '--dir']):
            src_dir = str(proc_argv[2])
            pid_file = self._get_pid(self.backup_log_dir, "restore", proc_log_file)
         else:
            chk_opt = jbackup_chk_option()
            chk_opt._print_help()
            sys.exit(1)
      elif(len(proc_argv) == 1 and proc_argv[0] in ['check']):
         Logging._logging(proc_log_file, "Start jbackup check")
         Logging._logging_blank(proc_log_file)
         pid_file = self._get_pid(self.backup_log_dir, "check", proc_log_file)
      elif(len(proc_argv) == 3 and proc_argv[0] in ['remove']):
         if((len(proc_argv) == 3) and (proc_argv[1] in ['-d', '--date']) and int(proc_argv[2]) > 0):
            bf_day = int(proc_argv[2])
            pid_file = self._get_pid(self.backup_log_dir, "remove", proc_log_file)
         elif ((len(proc_argv) == 3) and (proc_argv[1] in ['-g', '--generation']) and int(proc_argv[2]) > 0):
            gene = int(proc_argv[2])
            pid_file = self._get_pid(self.backup_log_dir, "remove", proc_log_file)
         else:
            chk_opt = jbackup_chk_option()
            chk_opt._chk_err()
            sys.exit(1)
      elif(len(proc_argv) == 1 and proc_argv[0] in ['binary']):
         pid_file = self._get_pid(self.backup_log_dir, "binary", proc_log_file)
      else:
         chk_opt = jbackup_chk_option()
         chk_opt._chk_err()
         sys.exit(1)

      # Connect ManageDB
      get_mngDB_info = jbackup_cnf_info(proc_log_file)
      mng_hostname, mng_port, mng_user, mng_password, err_code = get_mngDB_info._get_manageDB(proc_log_file)

      if (err_code != 0):
            self.rb.raise_err(False,1009, proc_log_file)
      else:
           pass

      db_con_mng = jbackup_con_mysql()
      db_con_mng._init_parameter(mng_hostname, mng_port, mng_user, mng_password, proc_log_file)

      if(len(proc_argv) == 1 and proc_argv[0] in ['backup']):
         jbackup_backup = jbackup_pre_backup()
         jbackup_backup._exec_backup(db_con_mng, self, proc_log_file, pid_file, self.get_time)
      elif(len(proc_argv) == 4 and proc_argv[0] in ['backup'] and proc_argv[1] in ['--with_remove'] and proc_argv[2] in ['-d', '--date','-g', '--generation']):
         # backup
         jbackup_backup = jbackup_pre_backup()
         jbackup_backup._exec_backup(db_con_mng, self, proc_log_file, pid_file, self.get_time)
         # remove
         jbackup_remove = jbackup_run_remove()
         if (proc_argv[2] in ['--date' , '-d']):
            opt_flag = 1
            jbackup_remove._exec_remove(db_con_mng, self, proc_log_file, rm_pid_file, bf_day, opt_flag, self.get_time)
         elif (proc_argv[2] in ['--generation', '-g']):
            opt_flag = 2
            jbackup_remove._exec_remove(db_con_mng, self, proc_log_file, rm_pid_file, gene, opt_flag, self.get_time)
      elif(len(proc_argv) == 3 and proc_argv[0] in ['apply-log' , 'applylog']):
         if (proc_argv[1] in ['-d', '--dir']):
            jbackup_applylog = jbackup_pre_applylog()
            jbackup_applylog._exec_applylog(db_con_mng, self, proc_log_file, pid_file, src_dir, self.get_time)
         else:
            chk_opt = jbackup_chk_option()
            chk_opt._chk_err()
            sys.exit(1)
      elif(len(proc_argv) == 3 and proc_argv[0] in ['restore']):
         if (proc_argv[1] in ['-d', '--dir']):
            jbackup_restore = jbackup_pre_restore()
            jbackup_restore._exec_restore(db_con_mng, self, proc_log_file, pid_file, src_dir, self.get_time)
         else:
            chk_opt = jbackup_chk_option()
            chk_opt._chk_err()
            sys.exit(1)
      elif(len(proc_argv) == 1 and proc_argv[0] in ['check']):
         jbackup_check = jbackup_run_check()
         jbackup_check._exec_check(db_con_mng, self, pid_file, proc_log_file, self.get_time)
      elif(len(proc_argv) == 3 and proc_argv[0] in ['remove']):
         jbackup_remove = jbackup_run_remove()
         if (proc_argv[1] in ['--date' , '-d']):
            opt_flag = 1
            jbackup_remove._exec_remove(db_con_mng, self, proc_log_file, pid_file, bf_day, opt_flag, self.get_time)
         elif (proc_argv[1] in ['--generation', '-g']):
            opt_flag = 2
            jbackup_remove._exec_remove(db_con_mng, self, proc_log_file, pid_file, gene, opt_flag, self.get_time)
      elif(len(proc_argv) == 1 and proc_argv[0] in ['binary']):
         jbackup_binary = jbackup_pre_binary()
         jbackup_binary._exec_binary_backup(db_con_mng, self, proc_log_file, pid_file, self.get_time)
      else:
         chk_opt = jbackup_chk_option()
         chk_opt._chk_err()
         sys.exit(1)


   def _get_init_info(self,db_con_mng, log_file):
      init_info={}
      # get fqdn
      chk_system = jbackup_cnf_info(log_file)
      cl_fqdn, cl_fqdn_err_code = chk_system._get_hostname()

      # get instance_id from db_management_tool
##      db_management_tool_uri, db_management_tool_uri_err_code = db_con_mng._execute("select uri from backup.db_management_tool_uri;")
##      if (db_management_tool_uri_err_code == 1):
##         self.rb.raise_err(False,1021, log_file)
##
##      if (cl_fqdn_err_code == 0 and db_management_tool_uri_err_code == 0):
##         t = jbackup_con_db_management_tool(log_file)
##         condb_management_tool_err_code = t._connectiondb_management_tool(db_management_tool_uri)
##      else:
##         self.rb.raise_err(False,1000,log_file)
##
##      if (condb_management_tool_err_code == 0):
##       db_management_tool_id, db_management_tool_id_err_code = t._get_db_management_tool_id(cl_fqdn)
##      else:
##         self.rb.raise_err(False,1001,log_file)

      t = jbackup_con_db_management_tool(log_file, db_con_mng)
      db_management_tool_id = t.get_db_management_tool_id(cl_fqdn)
      init_info = {"cl_fqdn":cl_fqdn, "db_management_tool_id":db_management_tool_id}
      return init_info

   def _get_db_info(self, log_file):
      try:
         p = subprocess.Popen("ps -ef | grep mysql | grep -v mysqld_safe",shell=True,stdout=subprocess.PIPE)
      except subprocess.CalledProcessError as err:
         self.rb.raise_err(True,1003,log_file)
      except Exception as err:
         self.rb.raise_err(True,1003,log_file)
      else:
         try:
            stdout = str(p.communicate()[0])
         except Exception as err:
            self.rb.raise_err(True,1003,log_file)
         else:
            if (re.search('--datadir', stdout)):
               data_dir = stdout.split("--datadir=")[1].split(" ")[0]
            else:
               self.rb.raise_err(True,1004,log_file)

            if (re.search('--defaults-file', stdout)):
               cnf_file = str(stdout).split("--defaults-file=")[1].split(" ")[0]
            else:
               self.rb.raise_err(True,1005,log_file)

         try:
            cnf_file = cnf_file.split('\\n')[0]
         except:
            self.rb.raise_err(True,1005,log_file)
         else:
            if (cnf_file[-3:len(cnf_file)] != "cnf"):
               self.rb.raise_err(True,1006,log_file)

         return data_dir , cnf_file


   def _get_pid(self, target_dir, name, log_file):
      pid = str(os.getpid())
      file_name = 'jbackup_' + name + '.pid'
      target_file = os.path.join(target_dir,file_name)

      if (os.path.isfile(target_file)):
         if ( name == "check"):
             Logging._logging(log_file, str(target_file))
             self.rb.raise_err(False,7007,log_file)
         else:
             Logging._logging(log_file, str(target_file))
             self.rb.raise_err(False,1007,log_file)
      else:
         try:
            pid_logging = open(target_file,'w')
         except IOError as e:
            Logging._logging(log_file, "cannot be opened : " + str(target_file))
            self.rb.raise_err(False,1008,log_file)
         except Exception as e:
            Logging._logging(log_file, "cannot be opened : " + str(target_file))
            self.rb.raise_err(False,1008,log_file)
         else:
            Logging._logging(log_file, 'PID FILE : ' + str(target_file))
            pid_logging.write(pid + '\n')

      return target_file

   def _del_pid(self, pid_file, log_file):
      if (os.path.isfile(pid_file)):
         try:
            os.remove(pid_file)
         except Exception as e:
            self.rb.raise_err(False,1031,log_file)
         else:
            Logging._logging(log_file, "removed pid file! - " + str(pid_file))
      else:
         Logging._logging(log_file, "Nothing pid file!")

##   def _read_backup_cnf(self, backup_info_file, log_file):
##      if (os.path.isfile(backup_info_file)):
##         conf_file = configparser.ConfigParser()
##         try:
##            conf_file.read(backup_info_file)
##         except configparser.Error as err:
##            self.rb.raise_err(True,1012,log_file)
##
##         backup_user = conf_file.get("client","user")
##         backup_password = conf_file.get("client","password")
##         master_user = conf_file.get("master","user")
##         master_password = conf_file.get("master","password")
##
##      else:
##         print("Nothing backup configuration file!")
##         print("Please check backup conf file!")

##      return (master_user, master_password, backup_user, backup_password)
###################################

### END DEF ###
