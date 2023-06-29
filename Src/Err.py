"""定义异常模块"""


class LoginErr(Exception):
    """定义登录失效的异常"""

    def __init__(self, msg):
        super().__init__(msg)


class TimeErr(Exception):
    """定义非选课时间段的异常"""

    def __init__(self, msg):
        super().__init__(msg)
