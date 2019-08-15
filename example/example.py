import time
import datetime
from py_cron_schedule import CronSchedule, CronFormatError


def out(x):
    print(x)


if __name__ == '__main__':
    cs = CronSchedule()
    # cs.add_task("s_test","* */1 * * * * *",lambda :print("s"))
    # cs.add_task("ms_test","*/500 * * * * * *",lambda :print("ms"))
    date = time.localtime()
    day = date.tm_wday + 1
    mon = date.tm_mon
    hour = date.tm_hour
    min = date.tm_min
    sec = date.tm_sec
    ms = datetime.datetime.now().microsecond / 1000

    cs.add_task("now_test0", "* * * * * *", out, 0)
    cs.add_task("now_test1", "1 * * * * *", out, 1)
    cs.add_task("now_test2", "*/1 * * * * *", out, 2)
    cs.add_task("v0.0.5 error", str(min + 1) + " " + str(hour) + " * * 1-5", out, "h")
    cs.start(use_multi=True)
