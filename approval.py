import config
import menu
from tools import *


def task_approval() -> None:
    print(f"即将显示待审核的任务")
    config.PENDING_TASKS = get_status_tasks('PENDING')

    if len(config.PENDING_TASKS ) == 0:
        print("无待审核任务!")
        return

    i = 0
    for task in config.PENDING_TASKS:
        if i != task.priority:
            i = task.priority
            print(f"--------------------以下为{i}级任务--------------------")
        else:
            print('--------------------------------------------------')

        print(task)

    print("1.通过任务    2.删除任务\n0.退出")
    while True:
        try:
            mode = int(input("请选择操作 (0-2):\n"))
            if 0 <= mode <= 2:
                break
            else:
                print("错误: 请输入 0-2 之间的数字")
        except ValueError:
            print("错误: 请输入有效的数字")

    if mode == 1:
        i = 0
        print("请输入要通过的任务标题:\n(支持多选,空格分隔)")
        task_name = input().split(' ')
        for task in config.PENDING_TASKS:
            if task.title in task_name:
                task.status_change('PROCESSING')
                i += 1
        if i :
            print(f'成功通过{i}个任务')
            save_tasks()
            config.PENDING_TASKS = get_status_tasks('PENDING')
            task_approval()

        else:
            print("Error:操作失败,请检查输入")
            task_approval()

    if mode == 2:
        i = 0
        print("请输入要通过的任务标题:\n(支持多选,空格分隔)")
        task_name = input().split(' ')
        for task in config.PENDING_TASKS:
            if task.title in task_name:
                menu.TASK_SYSTEM.del_task(task.title)
                i += 1

        if i :
            print(f'成功删除{i}个任务')
            save_tasks()
            config.PENDING_TASKS = get_status_tasks('PENDING')
            task_approval()

        else:
            print("Error:操作失败,请检查输入")
            task_approval()

    if mode == 0:
        return

def task_pass() -> None:
    print(f"即将显示进行中的任务")
    config.PROCESSING_TASKS = get_status_tasks('PROCESSING')

    if len(config.PROCESSING_TASKS) == 0:
        print("无进行中任务!")
        return

    i = 0
    for task in config.PROCESSING_TASKS:
        if i != task.priority:
            i = task.priority
            print(f"--------------------以下为{i}级任务--------------------")
        else:
            print('--------------------------------------------------')

        print(task)

    print("1.完成任务\n0.退出")
    while True:
        try:
            mode = int(input("请选择操作 (0-1):\n"))
            if 0 <= mode <= 1:
                break
            else:
                print("错误: 请输入 0-1 之间的数字")
        except ValueError:
            print("错误: 请输入有效的数字")

    if mode == 1:
        i = 0
        print("请输入要完成的任务标题:\n(支持多选,空格分隔)")
        task_name = input().split(' ')
        for task in config.PROCESSING_TASKS:
            if task.title in task_name:
                task.status_change('COMPLETED')
                i += 1
        if i:
            print(f'成功完成{i}个任务')
            save_tasks()
            config.PENDING_TASKS = get_status_tasks('PROCESSING')
            task_pass()

        else:
            print("Error:操作失败,请检查输入")
            task_pass()

    if mode == 0:
        return

if __name__ == '__main__':
    task_approval()