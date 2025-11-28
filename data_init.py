import os
from pathlib import Path


def initialize_data_directory():
    base_dir = Path("Data")

    # 定义需要创建的文件及其初始内容
    files_config = {
        "user.txt": """#user.txt
name: Admin role: admin privilege: 0 password: admin
name: Bob role: manager privilege: 1 password: 123
""",

        "task.txt": """#task.txt
--------------------------------------------------
$id: 1    $title: 示例任务    $priority: 1    $status: PENDING    $responsible_person: Admin    $deadline: 2024-12-31
$description:
'''
这是一个示例任务描述
'''
""",

        "project.txt": """#project.txt
--------------------------------------------------
$title: 示例项目    $start_date: 2024-01-01    $end_date: 2024-12-31
$description:
'''
这是一个示例项目描述
'''
""",

        "comment.txt": """#comment.txt
--------------------------------------------------
$id: 1    $task_id: 0    $author: Admin    $time: 2024-01-01 10:00
$content:
这是一个示例评论
"""
    }

    # 创建 Data 目录（如果不存在）
    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {base_dir}")

    # 创建或检查各个文件
    for filename, initial_content in files_config.items():
        file_path = base_dir / filename

        if not file_path.exists():
            # 文件不存在，创建并写入初始内容
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(initial_content)
                print(f"创建文件: {file_path}")
            except Exception as e:
                print(f"创建文件失败 {file_path}: {e}")
        else:
            # 文件已存在
            print(f"文件已存在: {file_path}")


def check_data_files_exist():
    base_dir = Path("Data")

    if not base_dir.exists():
        return False

    required_files = ["user.txt", "task.txt", "project.txt", "comment.txt"]

    for filename in required_files:
        file_path = base_dir / filename
        if not file_path.exists():
            return False

    return True

def setup_environment():
    if not check_data_files_exist():
        print("初始化数据文件...")
        initialize_data_directory()

# 主程序入口
if __name__ == "__main__":
    print("正在检查数据目录...")

    # 检查数据文件是否存在
    if check_data_files_exist():
        print("所有数据文件已存在，无需初始化")
    else:
        print("数据文件不完整，开始初始化...")
        initialize_data_directory()
        print("数据目录初始化完成")