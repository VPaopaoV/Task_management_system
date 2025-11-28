import sys
import config
import approval
import data_control
from tools import *
from comment import comment
import report

TASK_SYSTEM = data_control.TaskControl()


def menu() -> None:

    print("功能菜单:\n1.项目&任务管理    2.查看任务    3.发表评论    4.报表分析    5.项目信息    \n0.退出")
    while True:
        try:
            mode = int(input("请选择操作 (0-5):\n"))
            if 0 <= mode <= 5:
                break
            else:
                print("错误: 请输入 0-5 之间的数字")
        except ValueError:
            print("错误: 请输入有效的数字")

    if mode == 1:

        if not config.CURRENT_USER_PRIVILEGE in (0, 1, 2):
            print("Error:无操作权限,将返回至功能菜单")
            menu()

        print("1.修改项目信息    2.发表任务    3.删除任务    4.修改任务    5.任务审批    6.查看全部任务列表    \n0.返回上级菜单")
        while True:
            try:
                mode_1 = int(input("请选择操作 (0-6):\n"))
                if 0 <= mode_1 <= 6:
                    break
                else:
                    print("错误: 请输入 0-6 之间的数字")
            except ValueError:
                print("错误: 请输入有效的数字")

        if mode_1 == 1:
            data_control.add_project()
            save_project()
            menu()

        if mode_1 == 2:
            TASK_SYSTEM.data_input()
            save_tasks()
            menu()

        if mode_1 == 3:
            task_title = input("输入任务标题:\n")
            if TASK_SYSTEM.del_task(task_title):
                print("删除成功")
            else:
                print("Error:删除失败,请检查输入")
            save_tasks()
            menu()

        if mode_1 == 4:
            TASK_SYSTEM.change_task()
            save_tasks()
            menu()

        if mode_1 == 5:
            print("1.审批待审核任务    2.完成进行中任务\n0.返回上级菜单")
            while True:
                try:
                    mode_1_5 = int(input("请选择操作 (0-2):\n"))
                    if 0 <= mode_1_5 <= 2:
                        break
                    else:
                        print("错误: 请输入 0-2 之间的数字")
                except ValueError:
                    print("错误: 请输入有效的数字")

            if mode_1_5 == 1:
                approval.task_approval()
                menu()

            if mode_1_5 == 2:
                approval.task_pass()
                menu()

            if mode_1_5 == 0:
                menu()

        if mode_1 == 6:
            TASK_SYSTEM.all_path()
            menu()

        if mode_1 == 0:
            menu()

    if mode == 2:
        TASK_SYSTEM.get_user_task(config.CURRENT_USER)
        menu()

    if mode == 3:
        print("正在唤起评论窗口")
        comment()
        print("评论窗口关闭,即将返回菜单")
        menu()

    if mode == 4:
        print("1.个人工作量统计    2.项目进度    3.查看逾期任务\n0.退出")
        while True:
            try:
                mode_4 = int(input("请选择操作 (0-3):\n"))
                if 0 <= mode_4 <= 3:
                    break
                else:
                    print("错误: 请输入 0-3 之间的数字")
            except ValueError:
                print("错误: 请输入有效的数字")

        if mode_4 == 1:
            name = input("请输入要查询的对象:\n")
            if not name in [user.username for user in config.User_list]:
                print("未查找到此用户")
                menu()
            report.personal_report(name)
            menu()


        if mode_4 == 2:
            report.project_report()
            menu()

        if mode_4 == 3:
            upcoming_tasks = check_task_deadlines()
            if len(upcoming_tasks) == 0:
                print("无逾期任务")
                menu()

            i = 0
            print(f"--------------------以下为将到期任务--------------------")
            for task in upcoming_tasks:
                if not i == 0:
                    print('--------------------------------------------------')
                print(task)
                i += 1
            menu()

        if mode_4 == 0:
            menu()

    if mode == 5:
        print(config.PROJECT_INFO)
        print(f'There are {len(config.User_list)} people in the project')
        menu()

    if mode == 0:
        print("退出中")
        sys.exit()


if __name__ == '__main__':
    menu()