from py_cron_schedule import CronSchedule, CronFormatError


def out(x):
  print(x)


if __name__ == '__main__':
  cs = CronSchedule()
  # cs.add_task("s_test","* */1 * * * * *",lambda :print("s"))
  # cs.add_task("ms_test","*/500 * * * * * *",lambda :print("ms"))
  cs.add_task("now_test0",   "* * * * * *", out, 0)
  cs.add_task("now_test1",   "1 * * * * *", out, 1)
  cs.add_task("now_test2", "*/1 * * * * *", out, 2)

  cs.start(use_multi=True)
