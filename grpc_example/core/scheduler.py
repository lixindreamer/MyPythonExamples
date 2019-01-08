# -*- coding: utf-8 -*-
"""
@author  : xin_li
@file    : scheduler.py
@time    : 2018/11/16 16:42
@description: 运行于一个独立的线程中，用于执行定时更新对象的任务，
"""
# @Time    : 2018/11/16 16:42
# @Author  : xin_li
# @Site    :
# @File    : scheduler.py
# @Software: PyCharm

import time
import datetime
from queue import Queue,Empty
import threading
from typing import Callable, Sequence
from util.type_checker import LimitedInteger


_ONE_DAY_SECONDS = 60 * 60 * 24

_TASK_QUEUE = Queue()


class Job:
    _hour = LimitedInteger("_hour", lower=0, upper=23)
    _minute = LimitedInteger("_minute", lower=0, upper=59)

    def __init__(self, target: Callable, interval: int = None, hour: int = None, minute: int = None):
        self._target = target
        self._hour = hour or 0
        self._minute = minute or 0
        self._scheduler = dict()
        self._pre_run_time = None
        self._next_fire_time = None
        if interval is None and hour is None and minute is None:
            raise ValueError("Must provide one of the values interval, hour, minute at least")

        # 如果interval不为None,优先使用interval
        if interval is not None:
            self._scheduler["interval"] = interval
        else:
            self._scheduler["hour"] = self._hour
            self._scheduler["minute"] = self._minute

    def __repr__(self):
        return "Job:interval={},hour={},minute={}".format(str(self._scheduler.get("interval", None)),
                                                          str(self._scheduler.get("hour", None)),
                                                          str(self._scheduler.get("minute", None)))

    @property
    def pre_run_time(self):
        return self._pre_run_time

    def execute(self):
        self._target()

    def update_next_fire_time(self):
        """
        更新下一个运行时间。该函数在每次任务被放入到任务队列后执行一次。
        :return:
        """
        # 将上一次运行时间更新为当前时间
        self._pre_run_time = time.time()

        if "interval" in self._scheduler:
            self._next_fire_time = self._pre_run_time + self._scheduler["interval"]
        else:
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            next_run_datetime = datetime.datetime(year=tomorrow.year,
                                                  month=tomorrow.month,
                                                  day=tomorrow.day,
                                                  hour=self._scheduler["hour"],
                                                  minute=self._scheduler["minute"])
            self._next_fire_time = next_run_datetime.timestamp()

    @property
    def next_fire_time(self):
        if self._next_fire_time is not None:
            return self._next_fire_time


class Scheduler:
    def __init__(self, jobs:Sequence[Job]):
        self._jobs = jobs
        self._running = True
        self._sleep_seconds = 5

    def terminate(self):
        self._running = False

    def _run(self):
        """
        执行任务
        :return:
        """
        while self._running:
            try:
                due_job = _TASK_QUEUE.get(False)
                due_job.execute()
            except Empty:
                time.sleep(1)

        print("Scheduler Run exits!")

    def _trigger(self):
        """
        将job的下一次执行时间小于等于当前时间的任务放入任务队列
        :return:
        """
        while self._running:
            for job_obj in self._jobs:
                if job_obj.pre_run_time is None or job_obj.next_fire_time <= time.time():
                    _TASK_QUEUE.put(job_obj)
                    job_obj.update_next_fire_time()

            time.sleep(self._sleep_seconds)

        print("Scheduler Trigger exits!")

    def start(self):
        trigger_thread = threading.Thread(target=self._trigger,daemon=False)
        run_thread = threading.Thread(target=self._run,daemon=False)
        trigger_thread.start()
        run_thread.start()


if __name__ == '__main__':
    def func():
        print(time.time())
    def func2():
        print("abc")

    job = Job(func, interval=10,hour=4,minute=0)
    job2 = Job(func2,hour=5,minute=0)

    print(job,job2)

    scheduler = Scheduler([job,job2])
    scheduler.start()
    while True:
        time.sleep(10)
