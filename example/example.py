from py_cron_schedule import CronSchedule, CronFormatError

if __name__ == '__main__':
  cs = CronSchedule()
  # cs.add_task("s_test","* */1 * * * * *",lambda :print("s"))
  # cs.add_task("ms_test","*/500 * * * * * *",lambda :print("ms"))
  cs.add_task("now_test", "* * * * * *", lambda: print("1"))
  cs.start()
