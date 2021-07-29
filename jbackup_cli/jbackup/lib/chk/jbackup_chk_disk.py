#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import os.path
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.chk.jbackup_byte2human import jbackup_byte2human

class jbackup_chk_disk:
### START DEF ###
   
   # disk size check
   def _size_chk(self,tmp_target_dir,log_file):
      target_dir = tmp_target_dir.replace(" ","")
      chk_disk = os.statvfs(target_dir)
      
      tmp_total = chk_disk.f_frsize * chk_disk.f_blocks
      tmp_used = chk_disk.f_frsize * (chk_disk.f_blocks-chk_disk.f_bfree)
      tmp_free = chk_disk.f_frsize * chk_disk.f_bavail
      
      change_size = jbackup_byte2human()
      total = change_size.bytes2human(tmp_total) 
      used = change_size.bytes2human(tmp_used) 
      free = change_size.bytes2human(tmp_free) 
      self.free_m = tmp_free /1024 /1024
      
      Logging._logging(log_file, "TOTAL - " + str(total))
      Logging._logging(log_file, "USED  - " + str(used))
      Logging._logging(log_file, "FREE  - " + str(free))
   
   def _compare_tbl_size(self,each_tbl_size, log_file):
      if (self.free_m <= each_tbl_size[1]):
         Logging._logging(log_file, "Maxium table size - [" + each_tbl_size[0] + " , " + str(each_tbl_size[1]) + "M ]")
         Logging._logging(log_file, "Please check Disk size once again!" )
         raise SystemExit
      else:
         Logging._logging(log_file, "Maxium table size - [" + each_tbl_size[0] + " , " + str(each_tbl_size[1]) + "M ]")
      
   
### END DEF ###
