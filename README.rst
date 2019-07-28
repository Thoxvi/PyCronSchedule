PyCronSchedule
==============

|Travis| |PyPI| |Anti 996|

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
.. |PyPI| image:: https://img.shields.io/pypi/v/py-cron-schedule.svg
   :target: https://pypi.python.org/pypi/py-cron-schedule
.. |Anti 996| image:: https://camo.githubusercontent.com/a72e7743f15db219a6aba534f9de456e86268dd6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d416e74692532303939362d626c75652e7376673f7374796c653d666c61742d737175617265
   :target: https://github.com/996icu/996.ICU/blob/master/LICENSE
