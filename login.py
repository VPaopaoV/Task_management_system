import config


def sign_in():

    while True:
        password = str(input("请输入密码:\n"))

        if password == get_password():
            print("登录成功")
            break
        else:
            print("密码错误!")

def register():

    while True:
        password = str(input("请输入密码:\n"))
        psw_confirm = str(input("请确认密码:\n"))

        if password == psw_confirm:
            with open(config.USER_PATH, 'a', encoding='utf-8') as file:
                file.write(f'\nname: {config.CURRENT_USER} role: regular_member privilege: 2 password: {password}')
            print(f"用户{config.CURRENT_USER}添加成功")
            break

def get_password():

    for user in config.User_list:
        if user.username == config.CURRENT_USER:
            return user.password

    return None


def login():
    config.CURRENT_USER = str(input("请输入用户名:\n"))
    if not config.CURRENT_USER in [user.username for user in config.User_list]:
        print("用户不存在,将进行注册操作")
        register()
    else:
        privilege = 2
        for user in config.User_list:
            if user.username == config.CURRENT_USER:
                privilege = user.privilege

        config.CURRENT_USER_PRIVILEGE = privilege
        sign_in()