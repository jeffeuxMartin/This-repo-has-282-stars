"""
專門用來列印日誌的程式
"""

import logging
import os
from logging import handlers
import sys, traceback

log_path = ""
logger = None


class Logger(object):
    # 日誌級別關係對應
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "crit": logging.CRITICAL,
    }

    def __init__(
        self,
        filename,
        level="info",
        when="D",
        backCount=3,
        fmt="%(asctime)s - %(pathname)s[line:%(lineno)d] -%(levelname)s: %(message)s",
    ):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 設定日誌格式
        self.logger.setLevel(self.level_relations.get(level))  # 設定日誌級別
        sh = logging.StreamHandler()  # 往螢幕上輸出
        sh.setFormatter(format_str)  # 設定螢幕上顯示的格式
        th = handlers.TimedRotatingFileHandler(
            filename=filename,
            when=when,
            backupCount=backCount,
            encoding="utf-8",
        )  # 往檔案裡寫入指定間隔時間自動生成檔案的處理器
        # 實例化 TimedRotatingFileHandler
        # interval 是時間間隔，backupCount 是備份檔案的個數，如果超過這個個數，就會自動刪除，when 是間隔的時間單位，單位有以下幾種：
        # S 秒
        # M 分
        # H 小時、
        # D 天、
        # W 每星期（ interval==0 時代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 設定檔案裡寫入的格式
        self.logger.addHandler(sh)  # 把物件加到 logger 裡
        self.logger.addHandler(th)


def init_log(path="log.txt"):
    global log_path, logger
    log_path = path
    logger = Logger(log_path, level="debug").logger


def get_logger():
    global logger
    return logger


def log_traceback(e):
    """
    log traceback info
    :param e: exception object
    :return: None
    """
    exc_type, exc_value, exc_traceback_obj = sys.exc_info()
    logger.error(
        "An error occurred ：{}".format(e.args)
        + "\nexc_type: %s" % exc_type
        + "\nexc_value: {}".format(exc_value)
        + "\nexc_traceback_obj: %s" % exc_traceback_obj
        + "\nTrace Back: %s" % traceback.extract_tb(exc_traceback_obj)
    )
