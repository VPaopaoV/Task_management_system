from tools import *
from data_init import setup_environment

setup_environment()

CURRENT_USER = "visitor"
CURRENT_USER_PRIVILEGE = 2
USER_PATH = "Data/user.txt"
TASK_PATH = "Data/task.txt"
PROJECT_PATH = "Data/project.txt"
COMMENT_PATH = "Data/comment.txt"

User_list = load_users()
Task_list = load_tasks()
TASK_MAX_ID = get_task_max_id()
PROJECT_INFO = load_projects()
COMMENTS = load_comments()

PENDING_TASKS = get_status_tasks('PENDING')
PROCESSING_TASKS = get_status_tasks('PROCESSING')
COMPLETED_TASKS = get_status_tasks('COMPLETED')

