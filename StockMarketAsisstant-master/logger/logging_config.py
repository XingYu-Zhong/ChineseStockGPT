import logging
import colorlog
import datetime
import os

class Logging(object):

    def log(self, level='INFO'):  # 生成日志的主方法,传入对那些级别及以上的日志进行处理

        log_colors_config = {
            'DEBUG': 'white',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        logger = logging.getLogger()  # 创建日志器
        # levle = getattr(logging, level)  # 获取日志模块的的级别对象属性
        logger.setLevel(level)  # 设置日志级别
        # console_handler.setLevel(logging.DEBUG)
        # file_handler.setLevel(logging.INFO)

        log_folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logfiles")

        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)
        file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ".logger"
        log_path = os.path.join(log_folder_path, file_name)
        sh = logging.StreamHandler()  # 创建控制台日志处理器
        fh = logging.FileHandler(filename=log_path, mode='a', encoding="utf-8")  # 创建日志文件处理器
        # 创建格式器
        fmt = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)d [%(levelname)s] [%(funcName)s]: %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S')

        sh_fmt = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)d [%(levelname)s] [%(funcName)s]: %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=log_colors_config)
        # 给处理器添加格式
        sh.setFormatter(fmt=sh_fmt)
        fh.setFormatter(fmt=fmt)
        # 给日志器添加处理器，过滤器一般在工作中用的比较少，如果需要精确过滤，可以使用过滤器
        logger.addHandler(sh)
        logger.addHandler(fh)
        # if not logger.handlers:  # 作用,防止重新生成处理器

        return logger  # 返回日志器

logger = Logging().log()