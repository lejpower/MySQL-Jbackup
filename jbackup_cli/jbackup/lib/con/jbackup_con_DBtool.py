#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-07-30
#######################

import json, requests
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.log.jbackup_search_info import jbackup_search_info
from jbackup.lib.etc.jbackup_error import jbackup_error
from jbackup.lib.con.jbackup_col_sql import jbackup_col_sql

class jbackup_con_db_management_tool:
### START DEF ###
    def __init__(self, tmp_log_file, db_con_mng):
        self.log_file = tmp_log_file
        self.rb = jbackup_error()
        self.db_con_mng = db_con_mng

## abolish to connect to db_management_tool-mysql
##   def _connectiondb_management_tool(self, uri):
##      for i in range(6):
##         try:
##            resp = requests.get(uri[0][0], timeout=10)
##            self.data = resp.json()
##         except requests.exceptions.RequestException as e:
##            Logging._logging(self.log_file, "Can not connect to db_management_tool-mysql!")
##            Logging._logging(self.log_file, "Please check db_management_tool-mysql!")
##            self.err_code = 1
##            continue
##         except Exception as e:
##            Logging._logging(self.log_file, "Can not connect to db_management_tool-mysql!")
##            Logging._logging(self.log_file, "Please check db_management_tool-mysql!")
##            self.err_code = 1
##            continue
##         else:
##            self.err_code = 0
##            self.data = resp.json()
##            break
##
##      return self.err_code

    def get_db_management_tool_id(self, cl_fqdn):
        chk_sql = jbackup_col_sql()
        db_management_tool_id_chk_sql = chk_sql.db_management_tool_id_chk_sql(cl_fqdn)
        db_management_tool_id, tmp_backup_chk_err_code = self.db_con_mng._execute(db_management_tool_id_chk_sql)
        return db_management_tool_id[0][0]

## abolish to connect to db_management_tool-mysql
##   def _get_db_management_tool_id(self, cl_fqdn):
##      if (len(self.data) == 0 or self.err_code == 1):
##         Logging._logging(self.log_file, "Can not get db_management_tool_id - [ERROR]")
##         Logging._logging(self.log_file, "Please check hostname or register db_management_tool!!!")
##         err_code = 1
##         #raise SystemExit
##      else:
##         for i in self.data:
##            if (cl_fqdn == i.get('instance').get('host_name')):
##               backup_id = i.get('instance').get('id')
##               break
##            else:
##               backup_id = 0
##               continue
##
##         if (backup_id == 0):
##            ## Logging._logging(self.log_file, "Can not get db_management_tool id from db_management_tool-MYSQL")
##            Logging._logging(self.log_file, "Please check hostname or register db_management_tool!!!")
##            self.rb.raise_err(True,1019, self.log_file)
##            ## raise SystemExit
##         else:
##            err_code = 0
##            return backup_id, err_code

### END DEF ###
