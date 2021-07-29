#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import os.path
import sys
import multiprocessing
from jbackup.lib.log.jbackup_logging import Logging

class jbackup_chk_option:
### START DEF ###

   # disk size check
   def _chk_err(self):
      print("Please check option!")
      print("you can check using help option : jbackup help")

   def _print_help(self):
      print("[jbackup option]")
      print("")
      print("backup")
      print(" : execute jbackup full backup")
      print("")
      print("backup --with_remove --generation <INTERVAL_GENERATION> or backup --with_remove -g <INTERVAL_GENERATION>")
      print(" : execute jbackup backup and remove using generation")
      print("")
      print("backup --with_remove --date <INTERVAL_DAY> or backup --with_remove -d <INTERVAL_DAY>")
      print(" : execute jbackup backup and remove using date")
      print("")
      print("applylog --dir <SOURCE_DIR>")
      print(" : execute jbackup apply-log")
      print("")
      print("apply-log -d <SOURCE_DIR>")
      print(" : execute jbackup apply-log , short option")
      print("")
      print("restore --dir <SOURCE_DIR>")
      print(" : execute jbackup restore")
      print("")
      print("restore --d <SOURCE_DIR>")
      print(" : execute jbackup restore , short option")
      print("")
      print("remove --generation <INTERVAL_GENERATION> or remove -g <INTERVAL_GENERATION>")
      print(" : execute jbackup remove using generation")
      print("")
      print("remove --date <INTERVAL_DAY> or remove -d <INTERVAL_DAY>")
      print(" : execute jbackup remove using date")
      print("")
      print("binary")
      print(" : execute jbackup binary backup")
      print("")
      print("check")
      print(" : execute jbackup check for using reservation via WEB")
      print("")
      print("help")
      print(" : print help")




### END DEF ###
