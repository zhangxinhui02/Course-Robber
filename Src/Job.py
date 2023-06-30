"""任务执行类模块"""
import random
import time
from Err import TimeErr
from ServerIO import get_course_list, post


class Job:
    """任务执行对象"""
    def __init__(self,
                 required_course_teacher: dict,
                 required_course_type: list,
                 cookies: str,
                 server: int,
                 prefer_sleep_range: tuple,
                 sleep_range: tuple):
        """初始化对象参数"""
        self.required_course_teacher = required_course_teacher
        self.required_course_type = required_course_type
        self.server = server
        self.cookies = cookies
        self.prefer_sleep_range = prefer_sleep_range
        self.sleep_range = sleep_range

        self.post_list = []
        self.prefer_list = []

    def __foreach_post(self, post_list, prefer=False):
        """遍历给定的列表课程并提交选课，可选是否采用低延时"""
        for course in post_list:
            resp = post(self.server, self.cookies, course)
            if resp["code"] == 0:
                print(f'选择课程 {course["kcmc"]}-{course["teacher"]} 成功！')
                post_list.remove(course)
            elif '重复' in resp['info']:
                print(f'已经存在课程 {course["kcmc"]} ，无法重复选择同一课程！')
            else:
                print(f'选择课程 {course["kcmc"]}-{course["teacher"]} 失败！\n\t{resp["info"]}')
            if prefer:
                timeout = random.uniform(self.prefer_sleep_range[0], self.prefer_sleep_range[1])
            else:
                timeout = random.uniform(self.sleep_range[0], self.sleep_range[1])
            print(f'休眠{timeout}秒。')
            print()
            time.sleep(timeout)

    def run(self):
        """开始执行自动选课任务"""
        print('开始自动选课。')
        print()

        # 按名称获取待选课程列表
        print('按名称获取待选课程列表……')
        while True:
            try:
                courses = get_course_list(self.server,
                                          self.cookies,
                                          self.required_course_type)
                for course in courses:
                    if course['kcmc'] in self.required_course_teacher.keys():
                        self.post_list.append(course)
                print('待选课程列表获取成功：')
                for course in self.post_list:
                    print(f'\t{course["teacher"]}\t{course["kcbh"]}\t{course["kcmc"]}')
                print()
                break
            except TimeErr:
                timeout = random.uniform(self.sleep_range[0], self.sleep_range[1])
                print(f'不在选课时间段，继续等待。休眠{timeout}秒。')
                time.sleep(timeout)

        # 按老师筛选课程列表
        print('按老师筛选课程列表……')
        is_set = False  # 标识是否有筛选操作
        for k, v in self.required_course_teacher.items():
            teachers = v.split()
            if len(teachers) != 0:
                is_set = True
            force = []
            prefer = []
            for teacher in teachers:
                if '*' in teacher:
                    prefer.append(teacher.replace('*', ''))
                else:
                    force.append(teacher)
            if len(force) != 0:
                for course in self.post_list:
                    if k == course['kcmc']:
                        if course['teacher'] not in force:
                            self.post_list.remove(course)
            else:
                for course in self.post_list:
                    if k == course['kcmc']:
                        if course['teacher'] in prefer:
                            self.prefer_list.append(course)
            if is_set:
                print('优先选择课程列表：')
                for course in self.prefer_list:
                    print(f'\t{course["teacher"]}\t{course["kcbh"]}\t{course["kcmc"]}')
                print()
                print('筛选后课程列表：')
                for course in self.post_list:
                    print(f'\t{course["teacher"]}\t{course["kcbh"]}\t{course["kcmc"]}')
                print()
            else:
                print('未设置按教师筛选条件，跳过。')
                print()

        # 优先预选
        if len(self.prefer_list) != 0:
            print('选择优先课程：')
            self.__foreach_post(self.prefer_list, prefer=True)
            print()

        # 预选
        print('选择课程：')
        self.__foreach_post(self.post_list, prefer=True)
        print()

        print(f'预选完成，有{len(self.post_list)}个课程选择失败{"：" if len(self.post_list) != 0 else "。"}')
        for course in self.post_list:
            print(f'\t{course["teacher"]}\t{course["kcbh"]}\t{course["kcmc"]}')
        print()

        # 候补选课
        print('开始循环候补选课：')
        while True:
            self.__foreach_post(self.post_list)
            if len(self.post_list) == 0:
                break
        print('候补选课完成。')
        print()

        print('选课流程全部结束！')
