#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import datetime
import datetime as dt

class jbackup_get_date:
### START DEF ###
    def __init__(self):
        self.d = dt.datetime.today()

    def _get_execution_id(self, tmp_db_management_tool_id, backup_flag):
        db_management_tool_id = str(tmp_db_management_tool_id)
        head = self.d.strftime("%y%m%d")
        tail = self.d.strftime("%H%M%S")
        if (len(db_management_tool_id) == 1):
            result = "000" + db_management_tool_id
        elif (len(db_management_tool_id) == 2):
            result = "00" + db_management_tool_id
        elif (len(db_management_tool_id) == 3):
            result = "0" + db_management_tool_id
        elif (len(db_management_tool_id) == 4):
            result = db_management_tool_id

        # don't use backup_flag (20160830)
        self.id = int(head+result+tail)
        return self.id

    def _get_now_hms(self):
        ##d = datetime.datetime.today()
        get_now = self.d.strftime("%H%M%S")
        return get_now

    def _get_now_ymd(self):
        ##d = datetime.datetime.today()
        get_now = self.d.strftime("%Y%m%d")
        return get_now

    def _get_now_ymdm(self):
        ##d = datetime.datetime.today()
        get_now = self.d.strftime("%Y%m%d_%H%M")
        return get_now

    def _get_now_ymdhms(self):
        ##d = datetime.datetime.today()
        get_now = self.d.strftime("%Y%m%d_%H%M%S")
        return get_now

    def _get_now_ymdhms_log(self):
        ##d = datetime.datetime.today()
        get_now = self.d.strftime("%Y-%m-%d %H:%M:%S")
        return get_now

    def _get_current_time(self):
        current_date = []
        now_time = self.d.strftime('%H_%M_%S')
        today = self.d
        current_date.append(today.year)
        current_date.append(today.month)
        current_date.append(today.day)
        current_date.append(now_time)
        return current_date

    def _get_before_time(self, bf_day):
        before_date = []
        today = self.d
        bf_date = (today - dt.timedelta(days=bf_day))
        before_date.append(bf_date.year)
        before_date.append(bf_date.month)
        before_date.append(bf_date.day)
        return before_date

###################################

### END DEF ###
