import re
import os
import time
import logging
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

  def add_task(self,
               cron_name: AnyStr,
               cron_format: AnyStr,
               task: Callable,
               *args,
               **kwargs) -> bool:
    if self.__task_dict.get(cron_name) is None:
      self.__task_dict[cron_name] = {
        "timer": CronTimer(cron_format),
        "func": task,
        "args": args,
        "kwargs": kwargs,
      }
      logger.info("Add task successfully.")
      return True
    else:
      logging.warning("Add task failed: Already have the same name task")
      return False

  def del_task(self,
               cron_name: AnyStr) -> bool:
    if cron_name in self.__task_dict:
      self.__task_dict.pop(cron_name)
      logger.info("Delete task successfully.")
      return True
    else:
      logging.warning("Delete task failed: Task does not exist")
      return False

  def start(self,
            hook_in_start: Callable = None,
            hook_in_end: Callable = None,
            min_schedule_ms=0.5) -> None:
    if not self.__task_dict:
      logger.warning("Task queue is empty.")
      return

    self.__running = True
    while self.__running:
      if hook_in_start is not None: hook_in_start()

      for _, task in self.__task_dict.items():
        timer = task["timer"]
        func = task["func"]
        args = task["args"]
        kwargs = task["kwargs"]
        if timer.check():
          func(*args, **kwargs)

      if hook_in_end is not None: hook_in_end()
      time.sleep(min_schedule_ms / 1000)

  def stop(self) -> None:
    self.__running = False


class CronTimer(object):
  # 需要检查两种，第一个是 next time(star、every)，第二个是当前日期是否匹配(number 类)
  # (min, max, millisecond)
  TIME_RANGE = [
    (1, 7, 1000 * 60 * 60 * 24 * 7),
    (1, 12, 1000 * 60 * 60 * 24 * 30),
    (1, 30, 1000 * 60 * 60 * 24),
    (0, 23, 1000 * 60 * 60),
    (0, 59, 1000 * 60),
    (0, 59, 1000),  # second
    (0, 99, 1),  # millisecond
  ]

  def __calculate_next_time(self) -> float:
    next_time = time.time()

    for cron_unit_parts_index in range(len(self.__cron_data)):
      cron_unit_parts = self.__cron_data[cron_unit_parts_index]
      if len(cron_unit_parts) == 2:
        num = int(cron_unit_parts[1])
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

    for cron_unit_index in range(len(cron_list)):
      cron_unit = cron_list[cron_unit_index]
      std_range = CronTimer.TIME_RANGE[cron_unit_index]

      # */5 or 5 or *
      if re.search(r"[^0-9*/]", cron_unit) is None:
        cron_unit_parts = cron_unit.split("/")
        if len(cron_unit_parts) > 2:
          raise CronFormatError("[" + cron_unit + "] format error")
        elif len(cron_unit_parts) == 2:
          if (cron_unit_parts[0] != "*" or
              len(re.findall("\d+", cron_unit)) != 1):
            raise CronFormatError("[" + cron_unit + "] format error")
          else:
            self.__cron_data.append(["every"] + cron_unit_parts)
            continue
        elif len(cron_unit_parts) == 1:
          if cron_unit_parts[0] == "*":
            self.__cron_data.append(["star"] + cron_unit_parts)
            continue
          else:
            if re.match("\d+$", cron_unit_parts[0]) is not None:
              num = int(cron_unit_parts[0])
              if num < std_range[0] or num > std_range[1]:
                raise CronFormatError("[" + str(num) + "] out of range")
              else:
                self.__cron_data.append(["number"] + cron_unit_parts)
                continue
        # 1-4
        elif re.search(r"[^0-9\-]", cron_unit) is None:
          pass
        # 1,2,3
        elif re.search(r"[^0-9,]", cron_unit) is None:
          pass
        else:
          raise CronFormatError("[" + str(cron_unit_parts) + "] format error")

        self.__cron_data.append(cron_unit_parts)

    self.__next_time = self.__calculate_next_time()

  def check(self) -> bool:
    if time.time() > self.__next_time:
      self.__next_time = self.__calculate_next_time()
      return True
    else:
      return False


class CronFormatError(Exception):
  pass
