"""服务器交互模块"""
import requests
from Err import LoginErr, TimeErr


def get_course_list(server: int, cookies: str, course_type: list) -> list:
    """返回对应类型的课程列表"""
    course_list = []
    for i in course_type:
        url = f"http://xk{server}.cqupt.edu.cn/data/json-data.php?type={i}"
        headers = {
            "Host": f"xk{server}.cqupt.edu.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Referer": f"http://xk{server}.cqupt.edu.cn/xuanke.php",
            "Cookie": cookies
        }
        response = requests.get(url, headers=headers)

        # 登录失效
        if '失效' in response.json()['info']:
            raise LoginErr('登录失效，需要更新cookies！')
        # 不在时间段
        if '时间' in response.json()['info']:
            raise TimeErr('不在选课时间段！')
        # 获取课程列表出现的的其他错误
        if response.json()['code'] != 0:
            raise Exception(response.json()['info'])

        courses = response.json()['data']
        if i == 'cx':   # 重修返回的是列表，需要特别处理
            for course in courses:
                course_list.append(course)
        else:
            for course in courses.values():
                course_list.append(course)
    return course_list


def post(server: int, cookies: str, course: dict) -> dict:
    """提交选课申请，返回选课结果"""
    url = f"http://xk{server}.cqupt.edu.cn/xkPost.php"
    headers = {
        "Host": f"xk{server}.cqupt.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": f"http://xk{server}.cqupt.edu.cn",
        "Connection": "keep-alive",
        "Referer": f"http://xk{server}.cqupt.edu.cn/xuanke.php",
        "Cookie": cookies
    }

    response = requests.post(url, headers=headers, data=course)

    # 登录失效
    if '失效' in response.json()['info']:
        raise LoginErr('登录失效，需要更新cookies！')
    # 不在时间段
    if '时间' in response.json()['info']:
        raise TimeErr('不在选课时间段！')

    return response.json()
