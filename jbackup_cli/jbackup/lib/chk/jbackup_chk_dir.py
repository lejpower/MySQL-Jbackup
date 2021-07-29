#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import os
import os.path
import shutil
import time
from pwd import getpwnam
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.con.jbackup_con_mysql import jbackup_con_mysql
from jbackup.lib.etc.jbackup_error import jbackup_error

class jbackup_chk_dir:
### START DEF ###
     def __init__(self, tmp_log_file):
        self.log_file = tmp_log_file
        self.rb = jbackup_error()

     def _create_init_backup_path(self,db_management_tool_id, db_con_mng):
         tmp_get_strg_id, tmp_get_strg_id_err_code = db_con_mng._execute("select * from backup.backup_dir where db_management_tool_id =" + str(db_management_tool_id) + ";")
         if (tmp_get_strg_id_err_code == 1):
             self.rb.raise_err(True,1021, self.log_file)

         try:
            storage_id = tmp_get_strg_id[0][2]
            security_id = tmp_get_strg_id[0][3]
         except Exception as err:
            self.rb.raise_err(True,1015, self.log_file)
         else:
            mount_condition_id, mount_condition_id_err_code = db_con_mng._execute("select mount_condition_id from jbackup_view.storages where id =" + str(storage_id) + ";")
            strg_dir, strg_dir_err_code = db_con_mng._execute("select mount_point from jbackup_view.mount_conditions where id =" + str(mount_condition_id[0][0]) + ";")
            tmp_backup_dir = strg_dir[0][0]
            security_level, security_level_err_code = db_con_mng._execute("select * from backup.strg_security_level where security_id =" + str(security_id) + ";")
            if (strg_dir_err_code == 1 or security_level_err_code == 1):
               self.rb.raise_err(True,1021, self.log_file)
         
         try:
            init_backup_dir = os.path.join(tmp_backup_dir,str(security_level[0][1]))
         except Exception as err:
            Logging._logging(self.log_file, "Can not create initial backup directory!")
            self.rb.raise_err(True,1013, self.log_file)

         return init_backup_dir, storage_id, security_id

     def _create_backup_path(self,backup_dir, time_array, cl_fqdn):
          result = backup_dir
          try:
             for a in time_array[0:3]:
                result = result + "/" + str(a)

             result = result + "/" + str(cl_fqdn.replace(" ",""))

             if isinstance(time_array, tuple):
                result = os.path.join(result,time_array[3])
          except Exception as err:
             Logging._logging(self.log_file, "Can not create backup directory!")
             self.rb.raise_err(False,1013, self.log_file)
          else:
             return result.replace(" ","")

     def _create_remove_path_date(self,backup_dir, time_array, cl_fqdn):
          result = backup_dir
          try:
             for a in time_array[0:3]:
                result = result + "/" + str(a)

             if isinstance(time_array, tuple):
                result = os.path.join(result,time_array[3])

             result = os.path.join(result, cl_fqdn)
          except Exception as err:
             self.rb.raise_err(True,1016, self.log_file)
          else:
             return result.replace(" ","")

     def _create_remove_path_gene(self,init_backup_dir, time_array, gene, cl_fqdn):
        exist_dir1 = []
        list_len = 0

        for g in range(12):
            tmp_result1 = init_backup_dir
            tmp = {}

            try:
                for a in time_array[0:2]:
                    tmp_result1 = tmp_result1 + "/" + str(a)
                if isinstance(time_array, tuple):
                    tmp_result1 = os.path.join(tmp_result1,time_array[3])
            except Exception as err:
                self.rb.raise_err(True,1017, self.log_file)
            else:
                if (self._exist_dir(tmp_result1)):
                    tmp[time_array[1]] = sorted(map(int, os.listdir(tmp_result1)))
                    tmp["year"] = time_array[0]
                    list_len = list_len + len(os.listdir(tmp_result1))
                    exist_dir1.append(tmp)
                    exist_dir_size = len(exist_dir1)
                else:
                    exist_dir_size = 0

                # previous month
                if (int(time_array[1]) != 1):
                    tmp = time_array[1] - 1
                    time_array[1] = tmp
                elif (int(time_array[1]) == 1):
                    tmp = time_array[0] - 1
                    time_array[0] = tmp
                    time_array[1] = 12

        # Next step
        exist_dir1.reverse()
        monthes = []

        for i in exist_dir1:
            tmp = list(i.keys())
            tmp.remove('year')
            monthes.append(tmp[0])

        rm_count = 0
        target_count = 0
        remove_dir = []
        last_full_backup = False
        for i in range(len(monthes)):
            target_year1 = exist_dir1[i]["year"]
            target_month1 = monthes[i]

            target_day1 = exist_dir1[i][monthes[i]]
            for j in target_day1:
                rm_target_path1 = os.path.join(init_backup_dir,str(target_year1),str(target_month1),str(j), cl_fqdn)
                if (self._exist_dir(rm_target_path1)):
                    tmp_last_dir = sorted(os.listdir(rm_target_path1))

                    for d in tmp_last_dir:
                        if (d == 'binary-log'):
                            remove_dir.append([0,os.path.join(rm_target_path1,d)])
                        elif (d[2] == '-' and d[5] == '-'):
                            remove_dir.append([1,os.path.join(rm_target_path1,d)])
                            target_count = target_count + 1

        if (target_count < gene):
            Logging._logging(self.log_file, "Already, it only remains " + str(target_count) + " privious backup data!")
        else:
            for d in remove_dir:
                if(last_full_backup == False):
                    if(d[0] == 1):
                        if (rm_count == (target_count - gene)):
                            last_full_backup = True
                        rm_count = rm_count + 1

                if(last_full_backup == True):
                    Logging._logging(self.log_file, "[REMAIN]  - " + str(d[1]))
                else:
                    err_code = self._rm_dir(d[1])
                    if (len(os.listdir(os.path.dirname(d[1]))) == 0):
                        err_code = self._rm_dir(os.path.dirname(os.path.dirname(d[1])))

     def _exist_dir(self,tmp_target_dir):
          target_dir = tmp_target_dir.replace(" ","")
          return os.path.isdir(target_dir)

     def _rm_dir(self,target_dir):
          try:
             shutil.rmtree(target_dir.replace(" ",""))
             time.sleep(0.5)
          except OSError as e:
             Logging._logging(self.log_file, "target directory - " + str(target_dir))
             self.rb.raise_err(True,1018, self.log_file)
             err_code = 1
          except Exception as e:
             Logging._logging(self.log_file, "target directory - " + str(target_dir))
             Logging._logging(self.log_file, str(e))
             self.rb.raise_err(True,1018, self.log_file)
          else:
             Logging._logging(self.log_file, "[REMOVED] - " + str(target_dir))
             err_code = 0

          return err_code

     def _exist_file(self,target_file):
        return os.path.isfile(target_file)

     def _create_dir(self, target_dir):
        try:
           os.makedirs(target_dir)
        except OSError as e:
           if (self._exist_dir(target_dir)):
              Logging._logging(self.log_file, "Already existed (" + target_dir + ")")
           else:
              Logging._logging(self.log_file, str(e))
              self.rb.raise_err(True,1014, self.log_file)
        except Exception as e:
           Logging._logging(self.log_file, str(e))
           self.rb.raise_err(True,1014, self.log_file)
        else:
           Logging._logging(self.log_file, "Created (" + target_dir + ")")

     def _move_dir(self, target_dir, log_file):
          current_name = os.listdir(target_dir)
          full_path_current_name = [ os.path.join(target_dir,d) for d in os.listdir(target_dir)  ]
          newest = max(full_path_current_name, key=os.path.getctime)

          for d in current_name:
             if (newest == os.path.join(target_dir,d) and self._exist_dir(os.path.join(target_dir,d)) == True):
                new_name = d.split('_')[1]
                try:
                   os.rename(os.path.join(target_dir,d),os.path.join(target_dir,new_name))
                except Exception as e:
                   log = "Can not rename backup directory :" + str(os.path.join(target_dir,d))
                   log = log + " to " + str(os.path.join(target_dir,new_name))
                   Logging._logging(log_file, log)
                   Logging._logging(log_file, 'backup_directory = ' + str(os.path.join(target_dir,d)))
                else:
                   log = "Rename backup directory :" + str(os.path.join(target_dir,d))
                   log = log + " to " + str(os.path.join(target_dir,new_name))
                   Logging._logging(log_file, log)
                   Logging._logging(log_file, 'backup_directory = ' + str(os.path.join(target_dir,new_name)))
          return new_name

     def get_binary_log_list(self, binlog_dir, binlog_name, log_file):
          binlog_list = []
          try:
             tmp_binlog_list = os.listdir(binlog_dir)
          except Exception as err:
             Logging._logging(log_file, str(err))
          else:
             for i in range(len(tmp_binlog_list)):
                if (tmp_binlog_list[i].find(binlog_name) >= 0 and tmp_binlog_list[i].find('index') < 0):
                   binlog_list.append(tmp_binlog_list[i])

             try:
                binlog_list.sort()
                del binlog_list[-1]
             except Exception as e:
                Logging._logging(log_file, 'Can not remove latest binary file!')
                Logging._logging(log_file, 'Please check binary-log directory!')
                Logging._logging(log_file, str(e))
                binlog_list = []
             else:
                # create full path
                i = 0
                for l in binlog_list:
                    binlog_list[i] = os.path.join(binlog_dir,l)
                    i = i + 1

          return binlog_list

     def exec_chown(self, path):
        uid = getpwnam('mysql').pw_uid
        gid = getpwnam('mysql').pw_gid
        try:
           os.chown(path, uid, gid)
           for item in os.listdir(path):
              if (item != 'product'):
                 itempath = os.path.join(path, item)
                 if os.path.isfile(itempath):
                    os.chown(itempath, uid, gid)
                 elif os.path.isdir(itempath):
                    os.chown(itempath, uid, gid)
                    self.exec_chown(itempath)
        except Exception as e:
           Logging._logging(self.log_file, str(e))
           self.rb.raise_err(True,1030, self.log_file)
### END DEF ###
