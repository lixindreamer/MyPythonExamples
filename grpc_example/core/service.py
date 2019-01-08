# -*- coding: utf-8 -*-
"""
@author: lixin
@file: service.py
@time: 2018/12/28
@software: PyCharm
@description: 定义GPRC service 以及服务启动和退出函数，通过linux signal SIGHUB退出应用。
"""

from concurrent import futures
import time
import multiprocessing
import threading
import signal
import grpc
from core.scheduler import Scheduler


# 通过发送SIGHUP信号给主进程，使主进程优雅地退出，
# 在退出前处理完未完成的任务并关闭所有打开的资源
def _signal_hanlder(signum, frame):
    raise SystemExit


signal.signal(signal.SIGHUP, _signal_hanlder)


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

# 当前线程池和进程池混合使用，需要先创建好进程池实例，然后在多线程中共用一个进程池
_POOL = multiprocessing.Pool(processes=5)


class QuoteService(quote_service_pb2_grpc.QuoteServiceServicer):
    """
    继承quote_service_pb2_grpc.QuoteServiceServicer,实现服务中具体的function
    """

    def IsTradingDate(self, request, context):
        return quote_service_pb2.BooleanResult(True)


def start_server(server_address: str):
    """
    启动gRPC服务
    :param server_address: 服务地址ip:port
    :return:
    """

    # 创建一个线程用于执行定时任务
    scheduler = Scheduler([])
    scheduler.start()
    # gRPC 目前只支持concurrent.futures.ThreadPoolExecutor
    # 参考https://grpc.io/grpc/python/grpc.html#create-server
    thread_pool = futures.ThreadPoolExecutor(max_workers=10)
    grpc_server = grpc.server(thread_pool,
                              maximum_concurrent_rpcs=10)
    quote_service_pb2_grpc.add_QuoteServiceServicer_to_server(QuoteService(), grpc_server)
    grpc_server.add_insecure_port(server_address)
    grpc_server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    # 在进程关闭前关闭所有资源
    except (KeyboardInterrupt, SystemExit):
        # 必须要首先关闭进程池，用join方法阻塞主线程
        _POOL.close()
        _POOL.join()
        print("POOL is closed!")
        # 然后关闭grpc server,等待时间设为20秒，保证请求能正常返回
        grpc_server.stop(20)
        print("grpc server is closed!")
        # 保证所有后台资源都合理的关闭掉
        scheduler.terminate()
        print("Service exits.")


if __name__ == '__main__':
    pass
