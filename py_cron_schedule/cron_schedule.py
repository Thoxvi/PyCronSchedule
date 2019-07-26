import re
import os
import time
import logging
import multiprocessing

from typing import AnyStr, Callable

__all__ = [
  "CronSchedule",
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
            min_schedule_ms=1000) -> None:
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
  def __calculate_next_time(self) -> float:
    # TODO 根据算法计算出下一次执行的时间
    pass

  def __init__(self,
               cron_format: AnyStr):
    '''
    计算最小单位：微秒(以浮点形式，例如：1564157752.9863145)
    [毫秒] [秒] 分 时 日 月 周
    '''
    # TODO 解析 cron_format，并生成计算方式供计算使用

    self.__next_time = self.__calculate_next_time()

  def check(self) -> bool:
    if time.time() > self.__next_time:
      self.__next_time = self.__calculate_next_time()
      return True
    else:
      return False
