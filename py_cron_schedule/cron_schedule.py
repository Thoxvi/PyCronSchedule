import re
import os
import time
import logging
import datetime
import multiprocessing

from typing import AnyStr, Callable

__all__ = [
  "CronSchedule",
  "CronFormatError"
]

logger = logging.getLogger("CronSchedule")


class CronSchedule(object):
  def __init__(self):
    self.__task_dict = {}
    self.__running = False
    self.__processing_pool = multiprocessing.Pool()

  def add_task(self,
               task_name: AnyStr,
               cron_format: AnyStr,
               task: Callable,
               *args,
               **kwargs) -> bool:
    if self.__task_dict.get(task_name) is None:
      self.__task_dict[task_name] = {
        "timer": CronTimer(cron_format),
        "func": task,
        "args": args,
        "kwargs": kwargs,
      }
      logger.info("Add task [" + task_name + "] successfully.")
      return True
    else:
      logging.warning("Add task failed: Already have the same name task")
      return False

  def del_task(self,
               task_name: AnyStr) -> bool:
    if task_name in self.__task_dict:
      self.__task_dict.pop(task_name)
      logger.info("Delete task successfully.")
      return True
    else:
      logging.warning("Delete task failed: Task does not exist")
      return False

  def update_task(self,
                  task_name: AnyStr,
                  cron_format: AnyStr,
                  task: Callable,
                  *args,
                  **kwargs) -> bool:
    if not self.del_task(task_name):
      return False
    else:
      self.add_task(task_name,
                    cron_format,
                    task,
                    *args,
                    **kwargs)
      return True

  def check_once(self, use_multi=False) -> None:
    if not self.__task_dict:
      logger.warning("Task queue is empty.")
      return
    for task_name, task in self.__task_dict.items():
      if task["timer"].check():
        try:
          if use_multi:
            self.__processing_pool.apply(
              task["func"],
              task["args"],
              task["kwargs"]
            )
          else:
            task["func"](
              *task["args"],
              **task["kwargs"]
            )
        except Exception as e:
          logger.warning("Capture an exception in task [" + task_name + "]: " + str(e))

  def start(self,
            hook_when_start: Callable = None,
            hook_when_end: Callable = None,
            min_schedule_ms: float = 0.5,
            use_multi: bool = False) -> None:
    if not self.__task_dict:
      logger.warning("Task queue is empty.")
      return

    self.__running = True
    while self.__running:
      if hook_when_start is not None: hook_when_start()
      self.check_once(use_multi=use_multi)
      if hook_when_end is not None: hook_when_end()
      time.sleep(min_schedule_ms / 1000)

  def stop(self) -> None:
    self.__running = False


class CronTimer(object):
  # 需要检查两种，第一个是 next time(star、every)，第二个是当前日期是否匹配(number 类)
  # (min, max, millisecond)
  TIME_RANGE = [
    (1, 7, 1000 * 60 * 60 * 24 * 7),
    (1, 12, 1000 * 60 * 60 * 24 * 30),
    (1, 31, 1000 * 60 * 60 * 24),
    (0, 23, 1000 * 60 * 60),
    (0, 59, 1000 * 60),
    (0, 59, 1000),  # second
    (0, 999, 1),  # millisecond
  ]

  def __calculate_next_time(self) -> float:
    next_time = time.time() * 1000

    for cron_unit_parts_index in range(len(self.__cron_data)):
      cron_unit = self.__cron_data[cron_unit_parts_index]
      if cron_unit[0] == "every":
        num = int(cron_unit[1])
        next_time += num * CronTimer.TIME_RANGE[cron_unit_parts_index][2]

    return next_time

  def __init__(self,
               cron_format: AnyStr):
    '''
    计算最小单位：微秒(以浮点形式，例如：1564157752.9863145)
    [毫秒] [秒] 分 时 日 月 周
    '''
    self.__cron_data = []

    cron_format = cron_format.strip()
    cron_list = re.split("\s+", cron_format)[::-1]

    if len(cron_list) < 5 or len(cron_list) > 7:
      raise CronFormatError(
        "The number of [" + cron_format + "] format parameters is incorrect: " + str(len(cron_list)))

    if len(cron_list) == 5:
      cron_list.append("0")
    if len(cron_list) == 6:
      cron_list.append("*/1000")

    for cron_unit_index in range(len(cron_list)):
      cron_unit = cron_list[cron_unit_index]
      std_range = CronTimer.TIME_RANGE[cron_unit_index]

      # */5 or 5 or *
      if re.search(r"[^0-9*/]", cron_unit) is None:
        cron_unit_parts = cron_unit.split("/")
        if len(cron_unit_parts) > 2:
          raise CronFormatError("[" + cron_unit + "] format error")
        # */5
        elif len(cron_unit_parts) == 2:
          if (cron_unit_parts[0] != "*" or
              len(re.findall("\d+", cron_unit)) != 1 or
              int(cron_unit_parts[1]) < 1):
            raise CronFormatError("[" + cron_unit + "] format error")
          else:
            self.__cron_data.append(["every"] + [int(cron_unit_parts[1]) - 1])
            continue
        elif len(cron_unit_parts) == 1:
          if cron_unit_parts[0] == "*":
            self.__cron_data.append(["star"])
            continue
          else:
            if re.match("\d+$", cron_unit_parts[0]) is not None:
              num = int(cron_unit_parts[0])
              if num < std_range[0] or num > std_range[1]:
                raise CronFormatError("[" + str(num) + "] out of range")
              else:
                self.__cron_data.append(["number"] + [int(cron_unit_parts[0])])
                continue
            else:
              raise CronFormatError("[" + str(cron_unit) + "] format error")
        else:
          raise CronFormatError("[" + str(cron_unit) + "] format error")
      # 1-4
      elif re.search(r"[^0-9\-]", cron_unit) is None:
        cron_unit_parts = cron_unit.split("-")
        if len(cron_unit_parts) != 2:
          raise CronFormatError("[" + cron_unit + "] format error")
        # 1-2 2-1 1- -2
        for num in cron_unit_parts:
          num = int(num)
          if num < std_range[0] or num > std_range[1]:
            raise CronFormatError("[" + cron_unit + "] out of range")

        one = int(cron_unit_parts[0])
        two = int(cron_unit_parts[1])
        self.__cron_data.append(["number"] + list(range(one, two + 1)))

      # 1,2,3
      elif re.search(r"[^0-9,]", cron_unit) is None:
        cron_unit_parts = cron_unit.split(",")
        time_points = set()
        for num in cron_unit_parts:
          if num is "":
            raise CronFormatError("[" + cron_unit + "] format error")
          num = int(num)
          if num < std_range[0] or num > std_range[1]:
            raise CronFormatError("[" + cron_unit + "] out of range")
          time_points.add(num)
        self.__cron_data.append(["number"] + list(time_points))
      else:
        raise CronFormatError("[" + str(cron_unit) + "] format error")

    self.__next_time = self.__calculate_next_time()

  def check(self) -> bool:
    if time.time() * 1000 <= self.__next_time:
      return False

    '''[毫秒] [秒] 分 时 日 月 周，倒过来'''
    date = time.localtime()
    now_date = [
      date.tm_wday + 1,
      date.tm_mon,
      date.tm_mday,
      date.tm_hour,
      date.tm_min,
      date.tm_sec,
      datetime.datetime.now().microsecond / 1000
    ]

    for time_unit_index in range(len(self.__cron_data)):
      time_unit = self.__cron_data[time_unit_index]
      if time_unit[0] == "number":
        now = now_date[time_unit_index]
        if now not in time_unit[1:]:
          return False
      if time_unit[0] == "*":
        pass
      if time_unit[0] == "every":
        pass

    self.__next_time = self.__calculate_next_time()

    return True


class CronFormatError(Exception):
  pass
