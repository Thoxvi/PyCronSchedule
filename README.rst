PyCronSchedule
==============

|Travis|

Python's crontab syntax scheduler.

Features
--------

-  [x] Easy to use and feature-rich API
-  [x] Scheduling unit is a function
-  [x] Syntax similar to Linux
   `Crontab <http://man7.org/linux/man-pages/man5/crontab.5.html>`__
   timing tasks
-  [x] Provides millisecond precision
-  [ ] Use multi-process optimization

Usage
-----

``shell script $ pip install py-cron-schedule``

.. code:: python

    from py_cron_schedule import CronSchedule, CronFormatError

    if __name__ == '__main__':
      cs = CronSchedule()
      cs.add_task("ms", "* * * * * * *", lambda: print("Every Millsecond"))
      cs.add_task("sec", "* * * * * *", lambda: print("Every Second"))
      cs.add_task("min", "* * * * *",lambda :print("Every Minute"))
      cs.add_task("hour", "0 * * * *",lambda :print("Every Hour"))
      
      cs.start()

API Documentation
-----------------

-  [x] [简体中文](./doc/zh-CN/README.md)
-  [ ] [English](./doc/en-US/README.md)

License
-------

1. Under the Creative Commons GPL-3.0 Unported license. See the LICENSE
   file for details.
2. Under the Anti 996 License. See the Anti 996 LICENSE file for
   details.

.. |Travis| image:: https://travis-ci.org/Thoxvi/PyCronSchedule.svg?branch=master
   :target: https://travis-ci.org/Thoxvi/PyCronSchedule/settings#
