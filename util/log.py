# -*- coding: utf-8 -*-
"""
@author: lixin
@file: log.py
@time: 2018/12/20 11:37
@software: PyCharm
@description: Only for Linux. 拓展了logging中的TimedRotatingFileHandler，保证在多进程下写日志文件的安全性。
"""

import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time
from raven.handlers.logging import SentryHandler


try:
    import fcntl
except:
    pass


class SafeRotatingFileHandler(TimedRotatingFileHandler):
    """
    logging原生的TimedRotatingFileHandler不支持多进程操作，为保证写文件安全，
    本类重写doRollover方法，对日志加锁，保证同一时间只有一个进程切换文件。
    fcntl只在类unix系统中可用（是一个系统的c库）
    """

    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False,
                 atTime=None, bak_path=None):
        self.bak_path = bak_path
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)

    """
    Override getFilesToDelete & doRollover
    lines commanded by "##" is changed by lixin
    """

    def getFilesToDelete(self):
        """
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName, baseName = os.path.split(self.baseFilename)
        # begin 因为增加了将备份日志放入到指定文件夹的选项，所以当指定了back_path后，在清理过期日志文件时需要更换文件的路径 #
        if self.bak_path is not None:
            dirName = self.bak_path
        #  end  #

        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if self.extMatch.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        return result

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." +
                                     time.strftime(self.suffix, timeTuple))

        # 将历史日志放入到备份文件夹中
        if self.bak_path is not None:
            dfn = os.path.join(self.bak_path, os.path.basename(dfn))

        ### begin 用于保证在多进程下日志文件切换的安全，对正在切换的日志加锁，仅对类Unix系统有效 ###
        # if os.path.exists(dfn):
        #     os.remove(dfn)
        # self.rotate(self.baseFilename, dfn)
        if os.path.exists(self.baseFilename):
            # 对于文件的 close() 操作会使文件锁失效,不需使用fcntl.LOCK_UN解锁
            with open(self.baseFilename) as base_file:
                if fcntl in globals():
                    fcntl.flock(base_file, fcntl.LOCK_EX)
                if not os.path.exists(dfn):
                    self.rotate(self.baseFilename, dfn)
        ### end ###

        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


class ProjectLogging(object):
    def __init__(self, logger_name, log_format=None):
        self.logger = logging.getLogger(logger_name)
        self.format = logging.Formatter(log_format,datefmt="%Y-%m-%d %H:%M:%S")

    def add_time_rotating_file_handler(self, file, backup_count=30, when='MIDNIGHT', interval=1, bak_path=None):
        '''
        添加一个按日分割的日志handler,每天的日志都保存在相应的文件中
        :param file: 日志文件名
        :param backup_count: 保留的备份日志数量
        :return:
        '''
        if not os.path.isdir(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
        file_handler = SafeRotatingFileHandler(file, when=when, interval=interval,
                                               backupCount=backup_count, bak_path=bak_path)
        file_handler.setFormatter(self.format)
        self.logger.addHandler(file_handler)

    def add_sentry_handler(self,dsn):
        '''
        添加sentry handler
        :param dsn: sentry dsn address
        :type dsn: str
        :return:
        '''
        handler = SentryHandler(dsn)
        self.logger.addHandler(handler)

    def add_rotating_file_handler(self, file, backup_count=30):
        '''
        添加一个按文件大小分割的日志handler,默认日志大小为20M
        :param file: 日志文件名
        :param backup_count: 保留的备份日志数量
        :return:
        '''
        if not os.path.isdir(os.path.dirname(file)):
            os.mkdirs(os.path.dirname(file))
        file_handler = logging.handlers.RotatingFileHandler(file, maxBytes=1 * 1024 * 1024 * 20,
                                                            backupCount=backup_count)
        file_handler.setFormatter(self.format)
        self.logger.addHandler(file_handler)

    def add_stream_handler(self):
        console = logging.StreamHandler()
        console.setFormatter(self.format)
        self.logger.addHandler(console)

    def set_level(self, level):
        level_dict = {'critical': logging.CRITICAL, 'error': logging.ERROR,
                      'warning': logging.WARNING, 'info': logging.INFO,
                      'debug': logging.DEBUG, 'notset': logging.NOTSET}
        assert level in level_dict.keys()
        self.logger.setLevel(level_dict[level])

    def info(self, msg,*args,**kwars):
        self.logger.info(msg,*args,**kwars)

    def warning(self, msg,*args,**kwars):
        self.logger.warning(msg,*args,**kwars)

    def debug(self, msg,*args,**kwars):
        self.logger.debug(msg,*args,**kwars)

    def error(self, msg,*args,**kwars):
        self.logger.error(msg,*args,**kwars)

    def exception(self, msg,*args,**kwars):
        self.logger.exception(msg,*args,**kwars)

if __name__ == '__main__':
    pass