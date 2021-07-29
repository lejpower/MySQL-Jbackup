#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import os.path
import sys
import multiprocessing
from jbackup.lib.log.jbackup_logging import Logging

class jbackup_chk_error:
### START DEF ###

   # disk size check
   def _chk_err(self, code):
      err_msg = {\
         # Init process
         1000: "Init Error - Can not get hostname and db_management_tool id", \
         1001: "Init Error - Can not connect to db_management_tool", \
         1003: "Can not get Mysql status using ps command", \
         1004: "Can not get data directory information (--datadir, cmd: ps -ef)", \
         1005: "Can not get defaults-file information (--defaults-file, cmd: ps -ef)", \
         1006: "Please check cnfiguration file , Last name may be not .cnf", \
         1007: "Already existed Pid file!" ,\
         1008: "cannot be opened Pid file!" ,\
         1009: "Can not get manageDB infomation!",\
         1010: "Can not get clientDB infomation!" ,\
         1011: "It can not find log-bin option in the conf file!" ,\
         ## 1012 -> doesn't need it
         1012: "Can not read backup configuration file!" ,\
         1101: "Please check to install Xtrabackup!!!" ,\
         1102: "Xtabackup - [ERROR]" ,\
         1103: "Please check to install Innobackupex!!!" ,\
         1104: "Innobackupex - [ERROR]" ,\
         #check directory , file
         1013: "Can not create directory path!" ,\
         1014: "Can not create directory!" ,\
         1015: "Can not get Backup directory information from ManageDB!(please check initial registration once again!)" ,\
         1016: "Can not create remove directory!" ,\
         1017: "Can not create remove directory path!" ,\
         1018: "Can not remove target directory!" ,\
         1019: "Can not remove target file!" ,\
         1024: "Can not get binary directory!",\
         1025: "Can not get target directory!",\
         1026: "Can not copy binary files!",\
         1027: "Can not get cnf file!" ,\
         1028: "Can not copy cnf file to backup directory!" ,\
         1030: "Can not change directory user and group (mysql:mysql)" ,\
         1031: "Can not remove PID file!" ,\
         1032: "Can not copy binary-log files!" ,\
         #db_management_tool Connection
         ## 1019 double
         1019: "Can not get db_management_tool id from db_management_tool-MYSQL",\
         #Mysql Connection
         1020: "MySQL Connection Error" ,\
         1021: "MySQL Execution Error" ,\
         1022: "Local MySQL Connection Error" ,\
         1023: "Can not connect to ManageDB" ,\
         1029: "please check backup result directory (/BASE_DIR/SECURITY_LEVEL/YEAR/MONTH/DAY/HOSTNAME/BACKUP_DATA)" ,\
         # Check Python, Xtrabackup , CPU
         2001: "Can not get CPU information" ,\
         2002: "Can not calculate CPU count" ,\
         2003: "Can not get Python version" ,\
         #Backup & Restore Execution
         3001: "Can not execute Xtrabackup!" ,\
         3002: "Backup error!!!" ,\
         3003: "Apply-log error!!!" ,\
         3004: "(qpress) Nothing target directory!",\
         3005: "cannot change directory",\
         3006: "Can not remove qp file" ,\
         3007: "Decompress error!!!" ,\
         3008: "Restore error!!!" ,\
         3009: "Can not get any information in the mysql cnf file!!!" ,\
         3010: "Can not find innodb_data_file_path in the mysql cnf file!!!" ,\
         3011: "Can not find datadir in the mysql cnf file!!!" ,\
         3012: "Can not get any log result, because there is not backup log file" ,\
         3013: "binary-log backup error!" ,\
         #jbackup check
         7001: "Happened any troubles -  jbackup backup process!" ,\
         7002: "Happened any troubles -  jbackup backup process!" ,\
         7003: "Happened any troubles -  jbackup remove process!" ,\
         7004: "Happened any troubles -  jbackup applylog process!" ,\
         7005: "Happened any troubles -  jbackup restore process!" ,\
         7007: "Already existed Pid file for jbackup check"
         }
      return err_msg[code]

   def _print_help(self):
      pass




### END DEF ###
