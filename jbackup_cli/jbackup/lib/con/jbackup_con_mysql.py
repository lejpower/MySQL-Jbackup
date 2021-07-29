#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import re
import mysql.connector
import socket
import subprocess
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.log.jbackup_search_info import jbackup_search_info
from jbackup.lib.etc.jbackup_error import jbackup_error
from jbackup.lib.con.jbackup_col_sql import jbackup_col_sql
from jbackup.lib.etc.jbackup_get_date import jbackup_get_date

class jbackup_con_mysql():
### START DEF ###
   def _init_parameter(self,hostname,port,user,password, log_file):
      self.host = hostname
      self.port = int(port)
      self.user = user
      self.passwd= password
      self.log_file = log_file
      self.rb = jbackup_error()
      # select queries
      self.jbackup_sql = jbackup_col_sql()

   def _connection(self):
      try:
         cnx = mysql.connector.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, charset='utf8')
         cur = cnx.cursor(buffered=True)
      except mysql.connector.Error as err:
         Logging._logging(self.log_file, "[MYSQL ERROR] " + str(err))
         self.rb.raise_err(False,1020, self.log_file)
      except Exception as err:
         Logging._logging(self.log_file, "[MYSQL ERROR] " + str(err))
         self.rb.raise_err(False,1020, self.log_file)
      else:
         return cnx , cur

   def _execute(self, sql):
      cnx , cur = self._connection()
      try:
         cur.execute(sql)
         cnx.commit()
      except mysql.connector.Error as err:
         Logging._logging(self.log_file, "[MYSQL ERROR] " + str(err))
         Logging._logging(self.log_file, sql)
         err_code = 1
         ## self.rb.raise_err(True,1021, self.log_file)
      except Exception as err:
         Logging._logging(self.log_file, "[MYSQL ERROR] " + str(err))
         Logging._logging(self.log_file, sql)
         err_code = 1
         ## self.rb.raise_err(True,1021, self.log_file)
      else:
         err_code = 0
         result = []
         for row in cur:
            result.append(row)

      cnx.close()
      cur.close()

      if (err_code == 1):
         self.rb.raise_err(True,1021, self.log_file)
      elif ((re.search('select', sql) or re.search('SELECT', sql)) and len(result) == 0):
         err_code = 2
      else:
         err_code = 0

      return result, err_code

   def _local_mysql_chk(self):
      # mysql daemon check
      cnx , cur = self._connection()

      try:
         c = cnx.is_connected()
      except subprocess.CalledProcessError as e:
         Logging._logging(self.log_file,str(e))
         self.rb.raise_err(True,1022, self.log_file)

      try:
         cur.execute("select version();")
         cnx.commit()
      except mysql.connector.Error as err:
         Logging._logging(self.log_file, "[MYSQL ERROR] " + str(err))
         self.rb.raise_err(True,1021, self.log_file)
      else:
         result = []
         for row in cur:
            result.append(row)

      try:
         if (float(result[0][0][:3]) >= 5.7):
            cur.execute("show variables like 'default_storage_engine';")
         else:
            cur.execute("show variables like 'storage_engine';")
         cnx.commit()
      except mysql.connector.Error as err:
         Logging._logging(self.log_file, "[MYSQL ERROR] " + str(err))
         self.rb.raise_err(True,1021, self.log_file)
      else:
         for row in cur:
            result.append(row)


      if (c == True):
         Logging._logging(self.log_file, "MySQL VERSION - " + result[0][0])
         Logging._logging(self.log_file, "MySQL ENGINE  - " + result[1][1])
         Logging._logging(self.log_file, "MySQL PROCESS - OK")
      else:
         Logging._logging(self.log_file, "MySQL VERSION - " + result[0][0])
         Logging._logging(self.log_file, "MySQL ENGINE  - " + result[1][1])
         Logging._logging(self.log_file, "MySQL PROCESS - ERROR")
         self.rb.raise_err(True,1022, self.log_file)

      cnx.close()
      cur.close()

   def _tbl_size_chk(self,log_file):
      # mysql table size
      sql1 = "select table_name, floor((data_length+index_length)/1024/1024) as size, engine from information_schema.tables "
      sql2 = "where ENGINE = 'Innodb' OR ENGINE = 'MyISAM' AND TABLE_TYPE = 'BASE TABLE' order by size DESC limit 1 ;"
      sql = sql1 + sql2
      cnx , cur = self._connection()

      try:
         cur.execute(sql)
         cnx.commit()
      except mysql.connector.Error as err:
         Logging._logging(log_file , "[MYSQL ERROR] " + str(err))
         self.rb.raise_err(True,1021, self.log_file)
      else:
         result = []
         for row in cur:
            result.append(row[0])
            result.append(int(row[1]))

      cnx.close()
      cur.close()
      return result

   def _bk_process_to_db(self, backup_id, db_management_tool_id, cl_hostname, cl_port, storage_id, security_id, current_time, bk_start_time, backup_type, log_file):
      # 20160908 - edit by juni #
      Logging._logging(log_file,"--------------------")
      Logging._logging(log_file, "inside - _bk_process_to_db")
      Logging._logging(log_file,"--------------------")
      # 20160908 - edit by juni #

      # search some information in log-file
      srch_result = []
      srch_result.append(str(backup_id))
      srch_result.append(str(db_management_tool_id))
      srch_result.append(cl_hostname)
      srch_result.append(str(storage_id))
      srch_result.append(str(security_id))

      srch_result.append(str(current_time[0])) #backup_year
      srch_result.append(str(current_time[1])) #backup_month
      srch_result.append(str(current_time[2])) #backup_day
      srch_result.append("-") #backup_time
      if (backup_type == 0):
         srch_result.append(str(0)) #backup_type
      elif (backup_type == 1):
         srch_result.append(str(1)) #backup_type

      srch_result.append("2") #backup_result
      srch_result.append(bk_start_time)
      srch_result.append("-")
      srch_result.append("-") #ftrwl
      srch_result.append("-") #st_lock
      srch_result.append("-") #end_lock
      srch_result.append("-")
      srch_result.append("-")

      cnx , cur = self._connection()

      # 20160908 - edit by juni #
      Logging._logging(log_file,"--------------------")
      Logging._logging(log_file, srch_result )
      Logging._logging(log_file,"--------------------")
      # 20160908 - edit by juni #

      sql = self.jbackup_sql.backup_ins_result_process(srch_result)

      result, result_err_code = self._execute(sql)
      if (result_err_code == 0):
         Logging._logging(log_file, "[Record Backup Result To DB]")
         Logging._logging(log_file, sql)
         Logging._logging(log_file, "::INSERTED")
      elif (result_err_code == 1):
         self.rb.raise_err(True,1021, log_file)

   def _bk_result_to_db(self, backup_id, new_backup_dir_name, bk_end_time, log_file):

      # search some information in log-file
      srch_log = jbackup_search_info("backup", log_file)
      srch_result = []
      srch_result.append(str(backup_id))
      srch_result.append(str(new_backup_dir_name)) #backup_time
      srch_result.append(srch_log._get_backup_result()) #backup_result
      srch_result.append(bk_end_time)
      srch_result.append(srch_log._get_ftwrl()) #ftrwl
      srch_result.append(srch_log._get_lock_start()) #st_lock
      srch_result.append(srch_log._get_lock_end()) #end_lock
      bin_file, bin_pos = srch_log._get_tran_info()
      srch_result.append(bin_file)
      srch_result.append(bin_pos)

      cnx , cur = self._connection()

      # 20160908 - edit by juni #
      Logging._logging(log_file,"--------------------")
      Logging._logging(log_file, srch_result )
      Logging._logging(log_file,"--------------------")
      # 20160908 - edit by juni #

      sql = self.jbackup_sql.backup_up_result(srch_result)
      Logging._logging(log_file,"success getting sql query for updating backup result")

      result, result_err_code = self._execute(sql)
      if (result_err_code == 0):
         Logging._logging(log_file, "[Record Backup Result To DB]")
         Logging._logging(log_file, sql)
         Logging._logging(log_file, "::INSERTED")
      elif (result_err_code == 1):
         self.rb.raise_err(True,1021, log_file)

   def _binlog_bk_result_to_db(self, backup_id, bk_end_time, binlog_bk_result, log_file):

      # search some information in log-file
      srch_result = []
      srch_result.append(str(backup_id))
      srch_result.append(bk_end_time.split(" ")[1].replace(":","-"))
      srch_result.append(str(binlog_bk_result)) #backup_result
      srch_result.append(bk_end_time)
      srch_result.append("-") #ftrwl
      srch_result.append("-") #st_lock
      srch_result.append("-") #end_lock
      srch_result.append("-")
      srch_result.append("-")

      cnx , cur = self._connection()

      sql = self.jbackup_sql.backup_up_result(srch_result)

      result, result_err_code = self._execute(sql)
      if (result_err_code == 0):
          Logging._logging(log_file, "[Record Backup Result To DB]")
          Logging._logging(log_file, sql)
          Logging._logging(log_file, "::INSERTED")
      elif (result_err_code == 1):
         self.rb.raise_err(True,1021, log_file)

   def _applylog_result_to_db(self, db_management_tool_id, cl_hostname, cl_port, storage_id, security_id, backup_result_path, log_file):
      # search some information in log-file
      srch_log = jbackup_search_info("applylog", log_file)
      decomp_result = str(srch_log._get_applylog_result("decompress"))
      qp_result = str(srch_log._get_applylog_result("remove_qp"))
      applylog_result = str(srch_log._get_applylog_result("applylog"))

      if (len(backup_result_path) != 5):
         self.rb.raise_err(True,1029, self.log_file)
      else:
         storage_id = str(storage_id)
         security_id = str(security_id)
         backup_year = str(backup_result_path[0])
         backup_month = str(backup_result_path[1])
         backup_day = str(backup_result_path[2])
         backup_time = str(backup_result_path[4])

      cnx , cur = self._connection()
      sql = "INSERT INTO backup.applylog_result"
      sql = sql + "(`db_management_tool_id`,`host`,`port`,`strg_id`,`security_level_id`,`backup_year`,`backup_month`,`backup_day`,`backup_time`,"
      sql = sql + "`decompress_result`,`remove_qp_result`,`applylog_result`) "
      sql = sql + "VALUES(" + str(db_management_tool_id) + ",'" + cl_hostname + "'," + cl_port + "," + storage_id + "," + security_id  + ","
      sql = sql + backup_year  + "," + backup_month  + "," + backup_day  + ",'" + backup_time + "','"
      sql = sql + decomp_result + "','" + qp_result + "','" + applylog_result + "');"

      result, result_err_code = self._execute(sql)
      if (result_err_code == 0):
          Logging._logging(log_file, "[Record Apply-Log Result To DB]")
          Logging._logging(log_file, sql)
          Logging._logging(log_file, "::INSERTED")
      elif (result_err_code == 1):
         self.rb.raise_err(True,1021, log_file)

   def _restore_process_to_db(self, resore_id, db_management_tool_id, cl_hostname, storage_id, security_id, applylog_result_path, restore_start_time, log_file):

      # search some information in log-file
      srch_result = []
      srch_result.append(str(resore_id))
      srch_result.append(str(db_management_tool_id))
      srch_result.append(cl_hostname)
      srch_result.append(str(storage_id))
      srch_result.append(str(security_id))
      srch_result.append(str(applylog_result_path[0])) #backup_year
      srch_result.append(str(applylog_result_path[1])) #backup_month
      srch_result.append(str(applylog_result_path[2])) #backup_day
      srch_result.append(str(applylog_result_path[4])) #backup_time
      srch_result.append("2")                          #backup_result
      srch_result.append(restore_start_time)
      srch_result.append("-")                          #restore_end_time

      # Build SQL
      sql = self.jbackup_sql.restore_ins_result_process(srch_result)

      result, result_err_code = self._execute(sql)
      if (result_err_code == 0):
          Logging._logging(log_file, "[Record Restore Result To DB]")
          Logging._logging(log_file, sql)
          Logging._logging(log_file, "::INSERTED")
      elif (result_err_code == 1):
         self.rb.raise_err(True,1021, log_file)

   def _restore_result_to_db(self, restore_id, applylog_result_path, restore_end_time, log_file):

      # search some information in log-file
      srch_log = jbackup_search_info("restore", log_file)
      srch_result = []
      srch_result.append(str(restore_id))
      srch_result.append(srch_log._get_restore_result()) #restore_result
      srch_result.append(restore_end_time)

      # Build SQL
      sql = self.jbackup_sql.restore_up_result(srch_result)

      result, result_err_code = self._execute(sql)
      if (result_err_code == 0):
          Logging._logging(log_file, "[Record Restore Result To DB]")
          Logging._logging(log_file, sql)
          Logging._logging(log_file, "::INSERTED")

   def _restore_error_to_db(self, restore_id, log_file):

      # get restore_error_end_time
      get_time         = jbackup_get_date()
      restore_error_end_time = get_time._get_now_ymdhms_log()
      Logging._logging(log_file, "jbackup End Time - " + str(restore_error_end_time))
      Logging._logging_blank(log_file)

      # search some information in log-file
      srch_result = []
      srch_result.append(str(restore_id))
      srch_result.append(str(3))           #restore_result : error
      srch_result.append(restore_error_end_time)

      # Build SQL
      sql = self.jbackup_sql.restore_up_result(srch_result)

      result, result_err_code = self._execute(sql)
      if (result_err_code == 0):
          Logging._logging(log_file, "[Record Restore Result To DB]")
          Logging._logging(log_file, sql)
          Logging._logging(log_file, "::INSERTED")
      elif (result_err_code == 1):
         self.rb.raise_err(True,1021, log_file)



###################################

### END DEF ###
