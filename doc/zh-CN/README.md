# PyCronSchedule

欢迎使用 Python 的 `Crontab` 语法调度器！此库能过做到 `定时、周期地执行函数` 的功能，同时提供丰富的接口和灵活的配置来满足各种各样的需求。

## 安装

`$ pip install py_cron_schedule`

## 使用

```python
from py_cron_schedule import CronSchedule, CronFormatError

cs = CronSchedule()

try:
  cs.add_task(
    "task_name",
    "* * * * * *",
    lambda: print("Hello, PyCronSchedule!"))
except CronFormatError as e:
  print(e)

cs.start()
```

## 基本介绍

### Crontab 语法

如果你不了解 `Crontab` 的话，建议先阅读相应文档来了解其`基本语法`，以便理解后续内容，下面是推荐文档

- [Linux Tools Quick Tutorial(中文)](https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html)
- [Man 手册(英文)](http://man7.org/linux/man-pages/man5/crontab.5.html)

### 背景

> **为了方便阐述，下面将 `PyCronSchedule` 简写为 `PCS`**

PCS 提供了和 Crontab 相似的语法，并在其基础上做了部分扩展，使其可选地支持 `秒`、`毫秒` 级精度，并扩展 Crontab 的动作部分，使其支持 Python 函数。

下面是每位所代表的意义：

```text
[毫秒] [秒] 分 时 日 月 周
```

放在代码里来理解的话就是

```python
from py_cron_schedule import CronSchedule
cs = CronSchedule()

# 即每分钟执行一次
cs.add_task(
  "Every Min",
  "* * * * *",
  lambda x: print(x),
  "Min"
)

# 更复杂的例如下面这个，即从每年的 7 月 14 日的 12 点到 15 点的各个第 5,6,7 分钟，每秒执行一次预设的任务
cs.add_task(
  "hbd",
  "*/1000 */60 5,6,7 12-15 14 7 *",
  lambda x: print(x),
  "hbd"
)
```

可以看到，除了 Crontab 能提供到的分钟级精度外，PCS 能够额外的提供秒和毫秒等更精确的精度，同时由于高精度是可选的，所以也能够同时兼容 Crontab 原生语法

### 特性

- [x] 简单易用且功能丰富的 API
- [x] 调度单位为函数
- [x] 使用扩展的 Linux Crontab 解析语法
- [x] 支持到毫秒级精度
- [x] 使用多进程优化

## API 介绍

模块对外暴露了两个 Class 接口

- CronSchedule：调度器主类
  - add_task：添加任务
  - del_task：删除任务
  - update_task：更新任务
  - check_once：执行可执行的任务
  - start：开始执行调度
  - stop：停止调度
- CronFormatError：Crontab 语法错误类，里面会有详细的错误提示

### CronSchedule

#### add_task

> 添加成功则返回 True，否则 Flase；

参数|类型|描述
---|---|---
task_name|AnyStr|如果已存在同名，则添加失败
cron_format|AnyStr|Crontab 语法
task|Callable|执行函数，可为 Lambda
*args|List|执行函数参数
**kwargs|Dict|执行函数参数

#### del_task

> 删除成功则返回 True，否则 Flase；

参数|类型|描述
---|---|---
task_name|AnyStr|需要删除的 task 名

#### update_task

> 更新成功则返回 True，否则 Flase；

参数|类型|描述
---|---|---
task_name|AnyStr|如果不存在此任务，则更新失败
cron_format|AnyStr|Crontab 语法
task|Callable|执行函数，可为 Lambda
*args|List|执行函数参数
**kwargs|Dict|执行函数参数

#### check_once

> 无返回值；检查所有的 Task，如果发现满足执行条件，则执行

参数|类型|描述
---|---|---
use_multi|Bool|是否启用多进程优化，由于多进程不支持 Lambda 作为 Task，所以默认为 False

#### start

> 无返回值；开始进入调度循环(循环执行 check_once)

hook_when_start|Callable|每次开始执行 check_once 前会执行一次
hook_when_end|Callable|每次 check_once 执行结束后执行一次
min_schedule_ms|Float|循环等待的时间，单位为毫秒，默认 0.5ms 检查一次
use_multi|Bool|是否启用多进程优化，由于多进程不支持 Lambda 作为 Task，所以默认为 False

#### stop

> 无返回值；让循环条件为 False，以此终止循环

## Issue

关于项目的问题可以直接提 Issue，其他问题可以发送邮件至 [A@Thoxvi.com](mailto:A@Thoxvi.com) 来获取更多信息
