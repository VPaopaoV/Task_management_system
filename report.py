import config




def personal_report(name: str) -> None:
    progressing_task = 0
    completed_task = 0

    for task in config.Task_list:
        if task.responsible_person == name and task.status == 'PROGRESSING':
            progressing_task += 1

        if task.responsible_person == name and task.status == 'COMPLETED':
            completed_task += 1

    print(f"任务总数: {progressing_task + completed_task}    进行中: {progressing_task}    已完成: {completed_task}")
    if completed_task == 0:
        print("完成度: 0%")
    else:
        print(f"完成度: {completed_task / (completed_task + progressing_task) * 100}%")

def project_report() -> None:
    progressing_task = 0
    completed_task = 0
    for task in config.Task_list:
        if task.status == 'PROGRESSING':
            progressing_task += 1
        if task.status == 'COMPLETED':
            completed_task += 1

    print(f"任务总数: {progressing_task + completed_task}    进行中: {progressing_task}    已完成: {completed_task}")
    if completed_task == 0:
        print("完成度: 0%")
    else:
        print(f"完成度: {completed_task / (completed_task + progressing_task) * 100}%")
