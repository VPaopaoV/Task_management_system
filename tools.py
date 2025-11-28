import re
import config
import sys
from typing import List, Dict, Any
from datetime import datetime, timedelta
from data_model import User, Task, Project

def date_check(date_string):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, date_string):
        try:
            # 验证日期是否有效
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    return False

def load_users() -> List[User]:
    users = []

    try:
        with open(config.USER_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue

                # 使用正则表达式提取字段
                name_match = re.search(r'name:\s*(\S+)', line)
                role_match = re.search(r'role:\s*(\S+)', line)
                privilege_match = re.search(r'privilege:\s*(\d+)', line)
                password_match = re.search(r'password:\s*(\S+)', line)

                # 检查必需字段是否存在
                if not all([name_match, role_match, privilege_match, password_match]):
                    print(f"警告: 行格式不正确: {line}")
                    continue

                try:
                    # 提取字段值
                    username = name_match.group(1)
                    role = role_match.group(1)
                    privilege = int(privilege_match.group(1))
                    password = password_match.group(1)

                    # 创建User实例并添加到列表
                    user = User(username, role, privilege, password)
                    users.append(user)

                except Exception as e:
                    print(f"解析行时发生错误: {e}")
                    continue

        # print(f"成功加载 {len(users)} 个用户")
        return users

    except FileNotFoundError:
        print(f"错误: 用户文件 {config.USER_PATH} 不存在")
        return []
    except Exception as e:
        print(f"读取用户文件时发生错误: {e}")
        return []

def load_tasks() -> List[Task]:
    tasks = []

    try:
        with open(config.TASK_PATH, 'r', encoding='utf-8') as file:
            content = file.read()

        # 分割任务块
        task_blocks = re.split(r'-{50,}', content)

        for block in task_blocks:
            block = block.strip()
            if not block or block.startswith('#'):
                continue

            # 提取基本信息
            info_match = re.search(
                r'\$id:\s*(\d+).*?\$title:\s*([^$]+?)\$priority:\s*(\d+).*?\$status:\s*(\w+).*?\$responsible_person:\s*([^$]+?)\$deadline:\s*([^\n]+)\$',
                block.replace('\n', ' ')
            )

            if not info_match:
                continue

            # 提取描述
            desc_match = re.search(r"\$description:\s*'''\s*\n(.*?)'''", block, re.DOTALL)
            description = desc_match.group(1).strip() if desc_match else "无描述"

            # 创建任务
            task = Task(
                id=int(info_match.group(1)),
                title=info_match.group(2).strip(),
                description=description,
                priority=int(info_match.group(3)),
                status=info_match.group(4).strip(),
                responsible_person=info_match.group(5).strip(),
                deadline=info_match.group(6).strip()
            )

            tasks.append(task)

        return tasks

    except Exception as e:
        print(f"加载任务失败: {e}")
        return []

def load_projects() -> Project:

    try:
        with open(config.PROJECT_PATH, 'r', encoding='utf-8') as file:
            content = file.read()

        # 分割项目块
        project_blocks = re.split(r'-{50,}', content)

        for block in project_blocks:
            block = block.strip()
            if not block or block.startswith('#'):
                continue

            # 提取基本信息
            info_match = re.search(
                r'\$title:\s*([^$]+?)\$start_date:\s*([^$]+?)\$end_date:\s*([^\n]+)\$',
                block.replace('\n', ' ')
            )

            if not info_match:
                continue

            # 提取描述
            desc_match = re.search(r"\$description:\s*'''\s*\n(.*?)'''", block, re.DOTALL)
            description = desc_match.group(1).strip() if desc_match else "无描述"

            # 创建项目
            project = Project(
                title=info_match.group(1).strip(),
                description=description,
                start_date=info_match.group(2).strip(),
                end_date=info_match.group(3).strip(),
            )

        return project

    except FileNotFoundError:
        print(f"错误: 项目文件 {config.PROJECT_PATH} 不存在")
        sys.exit()
    except Exception as e:
        print(f"读取项目文件时发生错误: {e}")
        sys.exit()

def get_task_max_id() -> int:
    max_id = 0

    for task in config.Task_list:
        if task.id > max_id:
            max_id = task.id

    return max_id

def save_user() -> None:
    try:
        with open(config.USER_PATH, 'w', encoding='utf-8') as file:

            for user in config.User_list:
                # 写入用户信息
                file.write(
                    f"name: {user.username} role: {user.role} privilege: {user.privilege} password: {user.password}\n")

        print(f"保存成功")

    except Exception as e:
        print(f"保存用户到文件时发生错误: {e}")

def save_tasks() -> None:

    try:
        with open(config.TASK_PATH, 'w', encoding='utf-8') as file:

            for task in config.Task_list:
                # 写入分隔线
                file.write("-" * 50 + "\n")

                # 写入任务基本信息
                file.write(
                    f"$id: {task.id}    $title: {task.title}    $priority: {task.priority}    $status: {task.status}    $responsible_person: {task.responsible_person}    $deadline: {task.deadline}\n")

                # 写入描述
                file.write("$description:\n")
                file.write("'''\n")
                file.write(f"{task.description}\n")
                file.write("'''\n")

        print("保存成功")

    except Exception as e:
        print(f"保存任务到文件时发生错误: {e}")

def save_project() -> None:

    try:
        with open(config.PROJECT_PATH, 'w', encoding='utf-8') as file:

            # 写入分隔线
            file.write("-" * 50 + "\n")

            # 写入任务基本信息
            file.write(
                f"$title: {config.PROJECT_INFO.title}    $start_date: {config.PROJECT_INFO.start_date}    $end_date: {config.PROJECT_INFO.end_date}\n")

            # 写入描述
            file.write("$description:\n")
            file.write("'''\n")
            file.write(f"{config.PROJECT_INFO.description}\n")
            file.write("'''\n")

        print("保存成功")

    except Exception as e:
        print(f"保存任务到文件时发生错误: {e}")

def get_status_tasks(status: str) -> List[Task]:
    tasks = []

    for task in config.Task_list:
        if task.status == status:
            tasks.append(task)

    return tasks

def save_comments(comments: List[Dict[str, Any]]):
    try:
        with open(config.COMMENT_PATH, 'w', encoding='utf-8') as file:

            for comment in comments:
                # 写入分隔线
                file.write("-" * 50 + "\n")

                # 写入评论基本信息
                file.write(
                    f"$id: {comment['id']}    $task_id: {comment['task_id']}    $author: {comment['author']}    $time: {comment['time']}\n")

                # 写入内容
                file.write("$content:\n")
                file.write(f"{comment['content']}\n")

    except Exception as e:
        print(f"保存评论到文件时发生错误: {e}")

def load_comments() -> List[Dict[str, Any]]:
    comments = []

    try:
        with open(config.COMMENT_PATH, 'r', encoding='utf-8') as file:
            content = file.read()

        # 分割评论块
        comment_blocks = re.split(r'-{50,}', content)

        for block in comment_blocks:
            block = block.strip()
            if not block or block.startswith('#'):
                continue

            # 提取基本信息
            info_match = re.search(
                r'\$id:\s*(\d+).*?\$task_id:\s*(\d+).*?\$author:\s*([^$]+?)\$time:\s*([^\n]+)',
                block.replace('\n', ' ')
            )

            if not info_match:
                continue

            # 提取内容部分
            # 查找 $content: 后的所有内容，直到下一个分隔符或文件结束
            content_match = re.search(r'\$content:\s*\n(.*?)(?=\n-|\Z)', block, re.DOTALL)
            content_text = content_match.group(1).strip() if content_match else ""

            # 创建评论字典
            comment = {
                'id': int(info_match.group(1)),
                'task_id': int(info_match.group(2)),
                'author': info_match.group(3).strip(),
                'time': info_match.group(4).strip(),
                'content': content_text
            }

            comments.append(comment)

        return comments

    except FileNotFoundError:
        print(f"错误: 评论文件 {config.COMMENT_PATH} 不存在")
        return []
    except Exception as e:
        print(f"读取评论文件时发生错误: {e}")
        return []

def check_task_deadlines() -> List[Task]:
    upcoming_tasks = []
    today = datetime.now()

    for task in config.Task_list:
        # 跳过已完成的任务
        if task.status == "COMPLETED":
            continue

        # 解析截止日期
        deadline = datetime.strptime(task.deadline, "%Y-%m-%d")

        # 计算时间差
        time_delta = deadline - today

        # 如果时间差在3天内(包括今天)
        if timedelta(days=0) <= time_delta <= timedelta(days=3):
            upcoming_tasks.append(task)

    return upcoming_tasks