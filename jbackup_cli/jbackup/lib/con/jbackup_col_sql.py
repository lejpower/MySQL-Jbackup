#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

from jbackup.lib.log.jbackup_logging import Logging

class jbackup_col_sql:
### START DEF ###
    def __init__(self):
        self.db1 = 'backup'
        self.db2 = 'jbackup_view'

    # get db_management_tool_id
    def db_management_tool_id_chk_sql(self, arg1):
        sql = "SELECT db_management_tool_id FROM backup.backup_dir WHERE host = \'" + str(arg1) + "\' ;"
        return sql

    # get mount information
    def get_mount_conditions_sql(self, arg1):
        sql = "SELECT c.remote_path, c.mount_point, c.filesystem_type, c.mount_option, c.dump_flag, c.fsck_option "
        sql = sql + "FROM " + self.db2 + ".storages as s INNER JOIN "
        sql = sql + self.db2 + ".mount_conditions as c ON s.mount_condition_id = c.id "
        sql = sql + "WHERE c.id = " + str(arg1) + " ;"
        return sql

    # for jbackup check
    def retention_period(self, arg1):
        sql = "SELECT days FROM backup.retention_period WHERE retention_period_id = "
        sql = sql + "(SELECT retention_period_id FROM backup.backup_dir WHERE db_management_tool_id = " + str(arg1) + " );"
        return sql

    def backup_chk_sql(self, arg1, arg2):
        current_time = str(arg2[0]) + "-" + str(arg2[1]) + "-" + str(arg2[2]) + " " + str(arg2[3].replace("_",":"))
        # 2015-10-23 00:00:00

        sql = "select id,host,full_backup_flag,backup_time from "
        sql = sql + self.db2 + ".backup_reservations where host =\'" + str(arg1) + "\' and "
        sql = sql + "backup_time <= \'" + current_time + "\' and "
        sql = sql + "backup_status = 0 limit 1"
        return sql

    def backup_chk_result(self, arg1, arg2):
        sql = "UPDATE " + self.db2 + ".backup_reservations "
        sql = sql + "SET backup_status = 1 "
        ## sql = sql + ", backup_id = (SELECT backup_id FROM backup.backup_result where "
        ## sql = sql + " host =\'" + str(arg2) + "\' ORDER BY backup_id DESC LIMIT 1) "
        sql = sql + "where id =" + str(arg1) + " and "
        sql = sql + " host =\'" + str(arg2) + "\' ; "
        return sql

    def backup_ins_result_process(self, arg1_array):
        sql = "INSERT INTO backup.backup_result"
        sql = sql + "(`backup_result_id`,`db_management_tool_id`,`host`,`strg_id`,`security_level_id`,`backup_year`,"
        sql = sql + "`backup_month`,`backup_day`,`backup_time`,`backup_type`,`backup_result`,`backup_start_time`,`backup_end_time`,"
        sql = sql + "`ftwrl`,`lock_start`,`lock_end`,`tran_start`,`tran_end`) "
        sql = sql + "VALUES(" + arg1_array[0] + "," +arg1_array[1] + ",'" + arg1_array[2] + "'," + arg1_array[3] + "," + arg1_array[4] + "," + arg1_array[5]  + ","
        sql = sql + arg1_array[6]  + "," + arg1_array[7]  + ",'" + arg1_array[8] + "'," + arg1_array[9] + "," + arg1_array[10] + ",'" + arg1_array[11] + "','" + arg1_array[12] + "','"
        sql = sql + arg1_array[13] + "','" + arg1_array[14] + "','" + arg1_array[15] + "','" + arg1_array[16] + "','" + arg1_array[17] + "');"
        return sql

    def backup_up_result(self, arg1_array):
        sql = "UPDATE backup.backup_result set "
        sql = sql + "`backup_time` = '" + arg1_array[1]+ "' , `backup_result` = " + arg1_array[2] + ", "
        sql = sql + "`backup_end_time` = '" + arg1_array[3] + "' , `ftwrl` = '" + arg1_array[4] + "', "
        sql = sql + "`lock_start` = '" + arg1_array[5] + "' , `lock_end` = '" + arg1_array[6] + "', "
        sql = sql + "`tran_start` = '" + arg1_array[7] + "' , `tran_end` = '" + arg1_array[8] + "' "
        sql = sql + " WHERE `backup_result_id` = " + arg1_array[0] + ";"
        return sql

    def backup_err_result(self, arg1_array):
        sql = "UPDATE backup.backup_result set "
        sql = sql + "`backup_result` = " + arg1_array[1] + ", "
        sql = sql + "`backup_end_time` = '" + arg1_array[2] + "'"
        sql = sql + " WHERE `backup_result_id` = " + arg1_array[0] + ";"
        return sql

    def restore_chk_sql(self, arg1, arg2):
        current_time = str(arg2[0]) + "-" + str(arg2[1]) + "-" + str(arg2[2]) + " " + str(arg2[3].replace("_",":"))

        sql = "select id,dst_host,src_dir,restore_time from "
        sql = sql + self.db2 + ".restore_reservations where dst_host =\'" + str(arg1) + "\' and "
        sql = sql + "restore_time <= \'" + current_time + "\' and "
        sql = sql + "restore_status = 0 limit 1"
        return sql

    def restore_chk_result(self, arg1, arg2):
        sql = "UPDATE " + self.db2 + ".restore_reservations "
        sql = sql + "SET restore_status = 1 "
        sql = sql + "where id =" + str(arg1) + " and "
        sql = sql + " dst_host =\'" + str(arg2) + "\' ; "
        return sql

    def restore_ins_result_process(self, arg1_array):
        sql = "INSERT INTO backup.restore_result VALUES("
        for i,value in enumerate(arg1_array):
            if i == (len(arg1_array) - 1):
                sql += "'" + value + "'"
            else:
                sql += "'" + value + "'" + ", "
        else:
            sql += ");"
        return sql

    def restore_up_result(self, arg1_array):
        sql = "UPDATE backup.restore_result set "
        sql += "`restore_result`    =  " + arg1_array[1] + ", "
        sql += "`restore_end_time`  = '" + arg1_array[2] + "'"
        sql += " WHERE "
        sql += "`restore_result_id` = '" + arg1_array[0] + "';"
        return sql

    def restore_bf_chk_bk_result(self, arg1):
        sql = "SELECT " + self.db2 + ".backup_reservations "
        sql = sql + "where src_dir =\'" + str(arg1) + "\' ; "
        return sql

    def check_tbl(self, arg1):
        sql = "show tables from backup like '%" + arg1 + "%';"
        return sql

    def flush_log(self):
        sql = "FLUSH LOGS;"
        return sql

##   # for ###
## def applylog_get_src(self, arg1, arg2, arg3):
##      sql = "select strg_id,security_level_id,backup_year,backup_month,backup_day,backup_time "
##      sql = sql + "from " + self.db1 + "backup_result "
##      sql = sql + "where db_management_tool_id =" + str(arg1) + " host =" + str(arg2)
##      sql = sql + " and "
##      sql = sql + " and backup_result = 1 "
##      return sql
###################################

### END DEF ###
