
from datetime import  datetime
from typing import List,Dict,Optional
from enum import Enum

# 枚举定义
class TaskStatus(Enum):
    PENDING = "待处理"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"

class UserRole(Enum):
    ADMIN = "管理员"
    PROJECT_MANAGER = "项目经理"
    MEMBER = "普通成员"

# 数据模型
class User:
    def __init__(self, username: str, role: UserRole, permissions: List[str]):
        self.username = username
        self.role = role
        self.permissions = permissions

class Project:
    def __init__(self, name: str, description: str, start_date: datetime, end_date: datetime):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

class Task:
    def __init__(self, task_id: int, title: str, description: str, priority: int, 
                 status: TaskStatus, assignee: User, due_date: datetime):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.assignee = assignee
        self.due_date = due_date
        self.comments = []
        self.attachments = []
        self.change_log = []
# 模块C：协作通信系统
class CollaborationSystem:
    def __init__(self):
        self.tasks = {}
        self.notifications = []

    def add_comment(self, task_id: int, user: User, content: str) -> bool:
        """添加任务评论"""
        if task_id not in self.tasks:
            return False

        comment = {
            'user': user.username,
            'content': content,
            'timestamp': datetime.now(),
            'type': 'comment'
        }

        self.tasks[task_id].comments.append(comment)
        self._notify_task_update(task_id, f"用户 {user.username} 添加了评论")
        return True

    def add_attachment(self, task_id: int, user: User, file_name: str, file_data: bytes) -> bool:
        """添加文件附件"""
        if task_id not in self.tasks:
            return False

        attachment = {
            'user': user.username,
            'file_name': file_name,
            'file_data': file_data,
            'timestamp': datetime.now(),
            'type': 'attachment'
        }

        self.tasks[task_id].attachments.append(attachment)
        self._notify_task_update(task_id, f"用户 {user.username} 添加了附件: {file_name}")
        return True

    def get_task_comments(self, task_id: int) -> List[Dict]:
        """获取任务的所有评论"""
        if task_id not in self.tasks:
            return []
        return self.tasks[task_id].comments

    def get_task_attachments(self, task_id: int) -> List[Dict]:
        """获取任务的所有附件"""
        if task_id not in self.tasks:
            return []
        return self.tasks[task_id].attachments

    def _notify_task_update(self, task_id: int, message: str):
        """发送变更通知"""
        notification = {
            'task_id': task_id,
            'message': message,
            'timestamp': datetime.now()
        }
        self.notifications.append(notification)

        # 在实际应用中，这里可以集成邮件、消息推送等通知方式
        print(f"通知: 任务 {task_id} - {message}")

    def get_user_notifications(self, username: str, limit: int = 10) -> List[Dict]:
        """获取用户相关的通知（简化版）"""
        user_tasks = [task_id for task_id, task in self.tasks.items()
                     if task.assignee.username == username]

        user_notifications = []
        for notification in reversed(self.notifications):
            if notification['task_id'] in user_tasks:
                user_notifications.append(notification)
            if len(user_notifications) >= limit:
                break

        return user_notifications

    def log_task_change(self, task_id: int, user: User, change_description: str):
        """记录任务变更日志"""
        if task_id not in self.tasks:
            return

        change_log = {
            'user': user.username,
            'change_description': change_description,
            'timestamp': datetime.now()
        }

        self.tasks[task_id].change_log.append(change_log)
        self._notify_task_update(task_id, f"用户 {user.username} {change_description}")


# 其他模块的简化实现（用于演示）
class TaskScheduler:
    """模块A：任务调度引擎（简化）"""
    pass


class WorkflowManager:
    """模块B：工作流管理系统（简化）"""
    pass


class ReportSystem:
    """模块D：报表分析系统（简化）"""
    pass


# 权限控制类
class PermissionManager:
    def __init__(self):
        self.role_permissions = {
            UserRole.ADMIN: ['create_task', 'delete_task', 'assign_task', 'view_all'],
            UserRole.PROJECT_MANAGER: ['create_task', 'assign_task', 'view_project'],
            UserRole.MEMBER: ['view_assigned', 'update_status']
        }

    def has_permission(self, user: User, permission: str) -> bool:
        return permission in self.role_permissions.get(user.role, [])


# 主系统类
class TaskManagementSystem:
    def __init__(self):
        self.collaboration_system = CollaborationSystem()
        self.permission_manager = PermissionManager()
        self.users = {}
        self.projects = {}
        self.next_task_id = 1

    def create_task(self, title: str, description: str, priority: int,
                    assignee: User, due_date: datetime) -> Optional[Task]:
        """创建任务"""
        task = Task(
            task_id=self.next_task_id,
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.PENDING,
            assignee=assignee,
            due_date=due_date
        )

        self.collaboration_system.tasks[self.next_task_id] = task
        self.next_task_id += 1

        self.collaboration_system._notify_task_update(
            task.task_id, f"任务已创建，负责人: {assignee.username}")

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """获取任务信息"""
        return self.collaboration_system.tasks.get(task_id)


# 使用示例
if __name__ == "__main__":
    # 创建系统实例
    system = TaskManagementSystem()

    # 创建用户
    admin_user = User("admin", UserRole.ADMIN, [])
    member_user = User("zhangsan", UserRole.MEMBER, [])

    # 创建任务
    task = system.create_task(
        title="实现协作通信系统",
        description="开发任务评论和文件附件功能",
        priority=1,
        assignee=member_user,
        due_date=datetime(2024, 1, 31)
    )

    # 使用协作通信功能
    if task:
        # 添加评论
        system.collaboration_system.add_comment(
            task.task_id, admin_user, "请尽快完成这个功能")

        system.collaboration_system.add_comment(
            task.task_id, member_user, "正在开发中，预计明天完成")

        # 模拟添加附件
        system.collaboration_system.add_attachment(
            task.task_id, member_user, "design_document.pdf", b"fake_file_data")

        # 获取评论
        comments = system.collaboration_system.get_task_comments(task.task_id)
        print(f"\n任务评论:")
        for comment in comments:
            print(f"- {comment['user']}: {comment['content']} ({comment['timestamp']})")

        # 获取附件
        attachments = system.collaboration_system.get_task_attachments(task.task_id)
        print(f"\n任务附件:")
        for attachment in attachments:
            print(f"- {attachment['file_name']} (由 {attachment['user']} 上传)")

        # 获取用户通知
        notifications = system.collaboration_system.get_user_notifications(member_user.username)
        print(f"\n用户通知:")
        for notification in notifications:
            print(f"- {notification['message']} ({notification['timestamp']})")

