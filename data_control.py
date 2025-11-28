import config
import re
from data_model import Task, Project
from typing import List
from datetime import datetime
from tools import date_check

class TaskControl:

    def __init__(self) -> None:
        self.TaskData = config.Task_list
        self.People = [user.username for user in config.User_list]

    def data_input(self) -> None:
        print('标题,描述,优先级,负责人,截止日期:\n(空格为分隔符，时间格式\'yyyy-mm-dd\')')

        while True:
            task_input = input().split(' ')

            if len(task_input)!=5:
                print("Error:输入缺失或盈余!")
                continue

            if task_input[0] in [task.title for task in self.TaskData]:
                print("Error:任务标题重复!")
                continue

            if task_input[3] not in self.People:
                print("Error:未查找到此用户")
                continue

            if not date_check(task_input[4]):
                print("Error:时间格式有误")
                continue

            if datetime.strptime(task_input[4], '%Y-%m-%d') > datetime.strptime(config.PROJECT_INFO.end_date, '%Y-%m-%d'):
                print("Error:超出项目截止日期")
                continue

            config.TASK_MAX_ID += 1
            task = Task(
                id=config.TASK_MAX_ID,
                title=task_input[0].strip(),
                description=task_input[1],
                priority=int(task_input[2]),
                status='PENDING',
                responsible_person=task_input[3],
                deadline=task_input[4].strip(),
            )

            self.TaskData.append(task)
            break

        self.task_sort()

    def task_sort(self) -> None:
        self.TaskData.sort(key=lambda x: x.id)
        config.Task_list = self.TaskData

    def get_user_task(self, name: str) -> None:
        task_list = []

        for task in self.TaskData:
            if task.responsible_person == name:
                task_list.append(task)

        task_list.sort(key=lambda x: x.priority)

        i = 0
        for task in task_list:
            if i != task.priority:
                i = task.priority
                print(f"--------------------以下为{i}级任务--------------------")
            else:
                print('--------------------------------------------------')

            print(task)

    def all_path(self) -> None:
        task_list = config.Task_list
        task_list.sort(key=lambda x: (x.priority, x.responsible_person, x.deadline))

        i = 0
        for task in task_list:
            if i != task.priority:
                i = task.priority
                print(f"--------------------以下为{i}级任务--------------------")
            else:
                print('--------------------------------------------------')

            print(task)

    def del_task(self, title: str) -> bool:

        for task in self.TaskData:
            if task.title == title:
                config.Task_list.remove(task)
                self.TaskData = config.Task_list
                self.task_sort()
                return True

        print("Error:未发现此任务")
        return False

    def change_task(self) -> None:
        task_title = input("输入任务标题:\n")
        if self.del_task(task_title):
            self.data_input()

def add_project() -> None:
    print('标题,描述,开始日期,截止日期(空格作为分割符):')

    while True:
        info_input = input().split(' ')

        if len(info_input) != 4:
            print("Error:输入缺失或盈余!")
            continue

        if not date_check(info_input[2]):
            print("Error:开始时间格式有误!")
            continue

        if not date_check(info_input[3]):
            print("Error:截止时间格式有误!")
            continue

        project = Project(
            title=info_input[0].strip(),
            description=info_input[1].strip(),
            start_date=info_input[2].strip(),
            end_date=info_input[3].strip()
        )

        config.PROJECT_INFO = project
        break

# class ProjectControl:
#
#     def __init__(self) -> None:
#         self.ProjectList=[]
#
#     def add_new_project(self):
#         s=input("项目名称、描述、开始日期、结束日期(空格分隔):").strip(" ")
#         proj=TaskControl()
#         proj.data_input()
#         s.append(proj)
#         self.ProjectList.append(s)
#         return 0


if __name__ == '__main__':
    app = TaskControl()
    app.data_input()