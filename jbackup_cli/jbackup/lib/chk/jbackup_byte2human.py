#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

class jbackup_byte2human:
### START DEF ###
   def bytes2human(self, n):
      symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
      prefix = {}
      for i, s in enumerate(symbols):
         prefix[s] = 1 << (i+1)*10
      for s in reversed(symbols):
         if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
      
      return "%sB" % n
### END DEF ###
