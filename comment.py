import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import json
import config
from tools import *

class CommentSystem:
    def __init__(self):
        self.comments = config.COMMENTS
        self.next_id = 1
        self.tasks = {}
        for task in config.COMPLETED_TASKS:
            self.tasks[task.id] = task.title
        # self.tasks = {
        #     1: "开发登录功能",
        #     2: "设计数据库",
        #     3: "编写测试用例",
        #     4: "test"
        # }

    def add_comment(self, task_id, author, content):
        if not content.strip():
            return False

        comment = {
            'id': self.next_id,
            'task_id': task_id,
            'author': author,
            'content': content.strip(),
            'time': datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.comments.append(comment)
        config.COMMENTS = self.comments
        save_comments(config.COMMENTS)
        self.next_id += 1
        return True

    def get_task_comments(self, task_id):
        return [c for c in self.comments if c['task_id'] == task_id]


class CommentApp:
    def __init__(self, root):
        self.root = root
        self.system = CommentSystem()
        self.current_user = config.CURRENT_USER
        self.setup_ui()
        # print("界面初始化完成")  # 调试信息

    def setup_ui(self):
        self.root.title("任务评论系统")
        self.root.geometry("600x500")

        # 确保窗口显示在屏幕中央
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 600) // 2
        y = (self.root.winfo_screenheight() - 500) // 2
        self.root.geometry(f"600x500+{x}+{y}")

        # 主框架
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 顶部 - 任务选择
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)

        ttk.Label(top_frame, text="任务:").pack(side=tk.LEFT)
        self.task_var = tk.StringVar()
        task_combo = ttk.Combobox(top_frame, textvariable=self.task_var, state="readonly", width=30)
        task_combo['values'] = [f"{tid}: {title}" for tid, title in self.system.tasks.items()]
        if task_combo['values']:
            task_combo.current(0)
        task_combo.pack(side=tk.LEFT, padx=5)

        ttk.Label(top_frame, text=f"用户: {self.current_user}").pack(side=tk.RIGHT)

        # 中部 - 评论输入
        mid_frame = ttk.Frame(main_frame)
        mid_frame.pack(fill=tk.X, pady=5)

        ttk.Label(mid_frame, text="评论内容:").pack(anchor=tk.W)
        self.comment_text = scrolledtext.ScrolledText(mid_frame, height=4, width=50)
        self.comment_text.pack(fill=tk.X, pady=5)

        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="发表评论", command=self.post_comment).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="查看评论", command=self.view_comments).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="历史记录", command=self.show_history).pack(side=tk.LEFT, padx=2)
        # ttk.Button(btn_frame, text="清空", command=self.clear_input).pack(side=tk.LEFT, padx=2)

        # 底部 - 评论显示
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(bottom_frame, text="评论列表:").pack(anchor=tk.W)
        self.display_area = scrolledtext.ScrolledText(bottom_frame, height=15)
        self.display_area.pack(fill=tk.BOTH, expand=True)

        # print("所有UI组件创建完成")  # 调试信息

    def get_task_id(self):
        text = self.task_var.get()
        return int(text.split(':')[0]) if ':' in text else None

    def post_comment(self):
        task_id = self.get_task_id()
        content = self.comment_text.get("1.0", tk.END).strip()

        if not content:
            messagebox.showwarning("提示", "请输入评论内容")
            return

        if self.system.add_comment(task_id, self.current_user, content):
            messagebox.showinfo("成功", "评论发表成功")
            self.clear_input()
            self.view_comments()

    def view_comments(self):
        task_id = self.get_task_id()
        comments = self.system.get_task_comments(task_id)

        self.display_area.delete("1.0", tk.END)

        task_title = self.system.tasks.get(task_id, "未知任务")
        self.display_area.insert(tk.END, f"任务: {task_title} (ID: {task_id})\n")
        self.display_area.insert(tk.END, "=" * 40 + "\n\n")

        if not comments:
            self.display_area.insert(tk.END, "暂无评论\n")
            return

        for comment in comments:
            self.display_area.insert(tk.END,
                                     f"[{comment['time']}] {comment['author']} (评论ID:{comment['id']}):\n")
            self.display_area.insert(tk.END, f"  {comment['content']}\n")
            self.display_area.insert(tk.END, "-" * 30 + "\n")

    def show_history(self):
        history_win = tk.Toplevel(self.root)
        history_win.title("所有评论历史")
        history_win.geometry("500x400")

        text_area = scrolledtext.ScrolledText(history_win, height=20)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if not self.system.comments:
            text_area.insert(tk.END, "暂无评论记录")
        else:
            for comment in self.system.comments:
                task_title = self.system.tasks.get(comment['task_id'], "未知任务")
                text_area.insert(tk.END,
                                 f"任务{comment['task_id']}: {task_title}\n")
                text_area.insert(tk.END,
                                 f"评论{comment['id']} - {comment['author']} [{comment['time']}]:\n")
                text_area.insert(tk.END, f"  {comment['content']}\n")
                text_area.insert(tk.END, "=" * 40 + "\n")

        text_area.config(state=tk.DISABLED)

    def clear_input(self):
        self.comment_text.delete("1.0", tk.END)


# 运行程序
# if __name__ == "__main__":

def comment() -> None:
    config.COMMENTS = load_comments()
    try:
        root = tk.Tk()
        # print("Tk根窗口创建成功")  # 调试信息
        app = CommentApp(root)
        # print("开始主循环")  # 调试信息
        root.mainloop()
        # print("主循环结束")  # 调试信息
    except Exception as e:
        print(f"程序出错: {e}")