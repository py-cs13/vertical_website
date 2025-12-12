import unittest
import logging
import os
import tempfile
from unittest.mock import patch, MagicMock
from logging_config import setup_logging, get_logger


class TestLogging(unittest.TestCase):
    """日志功能测试用例"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 保存原始的日志处理器
        self.original_handlers = logging.getLogger().handlers.copy()
        # 清除根日志器的处理器
        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)
    
    def tearDown(self):
        """测试后的清理工作"""
        # 清除所有处理器
        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)
        # 恢复原始处理器
        for handler in self.original_handlers:
            logging.getLogger().addHandler(handler)
    
    def test_logging_setup(self):
        """测试日志配置初始化"""
        setup_logging(logging.INFO)
        
        # 获取根日志器
        root_logger = logging.getLogger()
        
        # 验证根日志器级别
        self.assertEqual(root_logger.level, logging.INFO)
        
        # 验证处理器数量（控制台+文件）
        self.assertEqual(len(root_logger.handlers), 2)
        
        # 验证处理器类型
        handler_types = [type(handler).__name__ for handler in root_logger.handlers]
        self.assertIn('StreamHandler', handler_types)
        self.assertIn('RotatingFileHandler', handler_types)
    
    def test_logging_level_control(self):
        """测试日志记录级别控制"""
        setup_logging(logging.WARNING)
        
        # 获取日志器
        logger = get_logger(__name__)
        
        # 测试不同级别的日志记录
        with self.assertLogs(logger, level='WARNING') as cm:
            logger.debug("这是一个DEBUG级别的日志")  # 不应该被记录
            logger.info("这是一个INFO级别的日志")    # 不应该被记录
            logger.warning("这是一个WARNING级别的日志")  # 应该被记录
            logger.error("这是一个ERROR级别的日志")    # 应该被记录
            
            # 验证日志记录数量
            self.assertEqual(len(cm.output), 2)
            
            # 验证日志内容
            self.assertIn("WARNING", cm.output[0])
            self.assertIn("ERROR", cm.output[1])
            self.assertIn("这是一个WARNING级别的日志", cm.output[0])
            self.assertIn("这是一个ERROR级别的日志", cm.output[1])
    
    @patch('logging_config.RotatingFileHandler')
    def test_logging_file_output(self, mock_rotating_handler):
        """测试日志文件输出配置"""
        # 模拟文件路径
        mock_log_file = "/mock/path/to/logs/app_test.log"
        
        with patch('logging_config.LOG_FILE', mock_log_file):
            setup_logging(logging.INFO)
            
            # 验证文件处理器创建
            mock_rotating_handler.assert_called_once()
            
            # 验证文件处理器参数
            call_args = mock_rotating_handler.call_args
            self.assertEqual(call_args[0][0], mock_log_file)
            self.assertEqual(call_args[1]['maxBytes'], 10 * 1024 * 1024)  # 10MB
            self.assertEqual(call_args[1]['backupCount'], 10)
            self.assertEqual(call_args[1]['encoding'], "utf-8")
    
    def test_logging_format(self):
        """测试日志格式化"""
        setup_logging(logging.INFO)
        
        # 获取根日志器的处理器
        handlers = logging.getLogger().handlers
        
        # 检查格式化器
        for handler in handlers:
            formatter = handler.formatter
            if formatter:
                # 验证格式字符串包含必要的字段
                format_string = formatter._fmt
                self.assertIn("%(asctime)s", format_string)
                self.assertIn("%(name)s", format_string)
                self.assertIn("%(levelname)s", format_string)
                self.assertIn("%(filename)s:%(lineno)d", format_string)
                self.assertIn("%(message)s", format_string)
    
    def test_get_logger(self):
        """测试获取日志器函数"""
        setup_logging(logging.INFO)
        
        # 获取不同名称的日志器
        logger1 = get_logger("test_module")
        logger2 = get_logger("test_module.submodule")
        
        # 验证日志器名称
        self.assertEqual(logger1.name, "test_module")
        self.assertEqual(logger2.name, "test_module.submodule")
        
        # 验证日志器继承关系
        self.assertEqual(logger1.parent, logging.getLogger())
        self.assertEqual(logger2.parent, logger1)
        
        # 验证日志器级别（继承根日志器）
        self.assertEqual(logger1.level, logging.NOTSET)  # 子日志器继承父级别
        self.assertEqual(logger2.level, logging.NOTSET)  # 子日志器继承父级别


if __name__ == '__main__':
    unittest.main()
