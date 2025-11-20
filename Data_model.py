class Task:
    def __init__(self, title: str, description: str, priority: int, leader: str, deadline: str) -> None:
        self.title = title
        self.description = description
        self.priority = priority
        self.leader = leader
        self.deadline = deadline
        self.status = "PENDING"     #or 'PROGRESSING' 'COMPLETED'
        self.id = -1

    def __str__(self) -> str:
        return f'Task "{self.title}" is leaded by {self.leader} and ended on {self.deadline} \nDescription: \n{self.description}'

    def __repr__(self) -> str:
        return f'title{self.title}, priority{self.priority}, leader{self.leader}, deadline{self.deadline}, status{self.status}, id{self.id}\ndescription\n{self.description}'

    def status_change(self, status: str) -> None:
        self.status = status

    def id_change(self, id: int) -> None:
        self.id = id

class Project:
    def __init__(self, title: str, description: str, start_date: str, end_date: str) -> None:
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.include_tasks = []

    def __str__(self) -> str:
        return f'Project "{self.title}" started on {self.start_date} until {self.end_date} \nDescription: \n{self.description}'

    def __repr__(self) -> str:
        return f'title{self.title}, start_date{self.start_date}, end_date{self.end_date}, include_tasks{self.include_tasks}'

    def add_task(self, task: int) -> None:
        self.include_tasks.append(task)

class User:
    def __init__(self, username: str, role: str, privilege: int) -> None:
        self.username = username
        self.role = role    #admin or manager or regular_member     管理员能做任何事；项目经理可以发布任务，更改项目截止时间和描述，添加或删除其他人的评论；普通成员可以发布任务，添加评论
        self.privilege = privilege  #0 is admin; 1 is manager; 2 is regular_member

    def __str__(self) -> str:
        return f'User "{self.username}" is role "{self.role}"'

    def __repr__(self) -> str:
        return f'username{self.username}, role{self.role}, privilege{self.privilege}'

#this is a git test in another file