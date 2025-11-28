import config
from login import login
from menu import menu

def main():
    print("欢迎使用任务管理系统，请先登录或注册")
    login()
    menu()



if __name__ == "__main__":
    main()