#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2015-12-02
#######################
import sys
import mysql.connector
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.chk.jbackup_chk_error import jbackup_chk_error
from jbackup.lib.alert.jbackup_email import rabackup_send_mail
from jbackup.lib.etc.jbackup_cnf_info import jbackup_cnf_info
from jbackup.lib.etc.jbackup_cnf_info import jbackup_init_value
from jbackup.lib.con.jbackup_col_sql import jbackup_col_sql
from jbackup.lib.etc.jbackup_get_date import jbackup_get_date

class jbackupError(Exception):

   def __init__(self, code):
      chk_err = jbackup_chk_error()
      self.code = code
      self.msg = chk_err._chk_err(self.code)

class jbackupError_updateDB():
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
         self.rb.raise_err(False,9999, log_file)
      except Exception as err:
         Logging._logging(self.log_file, "[MYSQL ERROR] " + str(err))
         self.rb.raise_err(False,9999, log_file)
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
         self.rb.raise_err(False,9999, self.log_file)
      except Exception as err:
         Logging._logging(self.log_file, "[MYSQL ERROR] " + str(err))
         Logging._logging(self.log_file, sql)
         err_code = 1
         self.rb.raise_err(False,9999, self.log_file)
      else:
         err_code = 0
         result = []
         for row in cur:
            result.append(row)

         cnx.close()
         cur.close()

      return result, err_code

   def _bk_error_to_db(self, backup_id):
      # get backup_end_time
      get_time = jbackup_get_date()
      bk_end_time = get_time._get_now_ymdhms_log()
      Logging._logging(self.log_file, "jbackup End Time - " + str(bk_end_time))
      Logging._logging_blank(self.log_file)

      # search some information in log-file
      srch_result = []
      srch_result.append(str(backup_id))
      srch_result.append(str(3)) #backup_result : error
      srch_result.append(bk_end_time)

      cnx , cur = self._connection()

      sql = self.jbackup_sql.backup_err_result(srch_result)

      result, result_err_code = self._execute(sql)
      if (result_err_code == 0):
         Logging._logging(self.log_file, "[Record Backup Error Result To DB]")
         Logging._logging(self.log_file, sql)
         Logging._logging(self.log_file, "::INSERTED")

   def _restore_error_to_db(self, restore_id):
      # get backup_end_time
      get_time = jbackup_get_date()
      restore_end_time = get_time._get_now_ymdhms_log()
      Logging._logging(self.log_file, "jbackup End Time - " + str(restore_end_time))
      Logging._logging_blank(self.log_file)

      # search some information in log-file
      srch_result = []
      srch_result.append(str(restore_id))
      srch_result.append(str(3)) #restore_result : error
      srch_result.append(restore_end_time)

      cnx , cur = self._connection()

      sql = self.jbackup_sql.restore_up_result(srch_result)

      result, result_err_code = self._execute(sql)
      if (result_err_code == 0):
         Logging._logging(self.log_file, "[Record Restore Error Result To DB]")
         Logging._logging(self.log_file, sql)
         Logging._logging(self.log_file, "::INSERTED")

class jbackup_error():
   def raise_err(self, DBupdate, code, log_file):
      if (code != 9999):
         try:
            raise jbackupError(code)
         except jbackupError as e:
            if (DBupdate == True):
               # Connect ManageDB
               get_mngDB_info = jbackup_cnf_info(log_file)
               mng_hostname, mng_port, mng_user, mng_password, err_code = get_mngDB_info._get_manageDB(log_file)
               if (err_code != 0):
                  Logging._logging(log_file, "Can not get manageDB infomation!")
                  Logging._logging(log_file, "Can not connect to manageDB!")
                  self.raise_err(False,9999, log_file)
               else:
                  #Update ManageDB
                  execution_id = Logging._get_execution_id()
                  db_con_mng = jbackupError_updateDB()
                  db_con_mng._init_parameter(mng_hostname, mng_port, mng_user, mng_password, log_file)
                  if (str(execution_id)[0] == '1'):
                     db_con_mng._bk_error_to_db(execution_id)
                  elif (str(execution_id)[0] == '2'):
                     db_con_mng._restore_error_to_db(execution_id)
            else: #DBupdate == True
               pass

            Logging._logging(log_file, e.msg)
            Logging._logging_blank(log_file)
            Logging._logging(log_file, "jbackup Error [" + str(code) + "] - terminate this process")
            Logging._logging_blank(log_file)

      else: #code != 9999
         Logging._logging_blank(log_file)
         Logging._logging(log_file, "It has not been updated backup status(error) in the ManageDB by jbackup_cli!")
         Logging._logging(log_file, "jbackup Error [" + str(code) + "] - terminate this process")
         Logging._logging_blank(log_file)

      if(code != 7007):
         send_mail = rabackup_send_mail(log_file, 1)
         send_mail._send()

      sys.exit(code)

###################################

### END DEF ###
