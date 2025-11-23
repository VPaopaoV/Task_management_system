import time

class TaskControl:
    '''用于管理每个项目下的所有任务'''
    '''所有的输入和输出之后会改成形参和返回值，目前是没加形参是方便测试状况，之后调用代码时再改'''
    '''最终完成后要在合适的位置跑一下ErrorCheck,检测当前数据有无出现问题,感觉还是再你们调用的时候检测比较好'''
    def __init__(self):
        self.TaskData=[]
        self.People=[]
    def DataInput(self):
        '''临时输入数据作为测试'''
        n=int(input("任务数量："))
        while(n):
            s=input('任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):').split(' ')
            #Id可以考虑自动生成的以后再做，日期当作一个纯数字年月日时分之间不要空格，位不足要补零,优先级理解为先做小的全做完才可以做下一个,假设每个任务只有一个人做，状态分未完成/已完成
            if(len(s)!=7):
                print("Error:输入缺失或盈余！")
                continue
            s[3]=int(s[3])
            s[6]=int(s[6])
            self.TaskData.append(s)
            if s[5] not in self.People:
                self.People.append(s[5])
            n-=1
            #print(s)
        self.TaskSort()
        return 0
    def TaskSort(self):
        '''对任务进行排序'''
        #先以人物排序,再以优先级排序,后截止日期排序
        self.TaskData.sort(key=lambda x:(x[5],x[3],x[6]))
        #但是对个人可能出现优先级高但截止日期晚的情况，所以要重新更新截止日期
        for i in range(len(self.TaskData)-1,0,-1):
            if(self.TaskData[i][5]!=self.TaskData[i-1][5]):continue
            if(self.TaskData[i][6]<self.TaskData[i-1][6]):self.TaskData[i-1][6]=self.TaskData[i][6]
        #print(self.TaskData)
    def CheckPersonalTask(self,Name_):
        '''查询个人任务顺序
        Name_:名字
        return 包含所有任务的列表'''
        #name=input("输入查询的名字：")
        name=Name_
        ans=[]
        for l in self.TaskData:
            if(l[5]==name):
                ans.append(l)
                #print(l)
        print("end")
        return ans
    def IdCheck(self,id__):
        '''查询前后要做的任务
        id__ 任务Id
        return None无此Id
        return [],[] 前置任务与后置任务 没有则为空'''
        #id_=input("输入ID：")
        id_=id__
        rank_=0
        for l in self.TaskData:
            if(l[0]==id_):
                rank_=l[3]
                break
        if(rank_==0):
            print("目标不存在")
            return None
        tl=[];tr=[]
        for l in self.TaskData:
            if(l[3]==rank_-1):
                tl.append(l)
            elif(l[3]==rank_+1):
                tr.append(l)
        # if(tl):
        #     print("前置任务：")
        #     for l in tl:
        #         print(tl)
        # else:
        #     print("无前置任务")
        # if(tr):
        #     print("后置任务：")
        #     for l in tr:
        #         print(l)
        # else:
        #     print("无后置任务")
        return tl,tr
    def PersonalPath(self,name_):
        '''查询个人的工作路径
        name_名字
        return 个人任务有序列表'''
        #name=input("输入名字：")
        name=name_
        ans=[]
        #print("个人任务内容、优先级及截止时间注意")
        for l in self.TaskData:
            if(l[5]!=name):continue
            #print(l)
            ans.append(l)
        return ans
    def AllPath(self):
        '''输出整体的工作路径
        return 整体工作路径列表'''
        NewList=self.TaskData
        NewList.sort(key=lambda x:(x[3],x[5],x[6])) #先以优先级排序,再按人物，再按时间
        place=0
        # 如有需要，输出直接删掉，重写输出
        for i in range(len(NewList)):
            if(place!=NewList[i][3]):
                place=NewList[i][3]
                print(f"第{place}级任务：")
            print(NewList[i])
        return NewList
    def ErrorCheck(self):
        '''检查不符合优先级顺序完成、超时未完成、任务重复
        正常返回1
        不正常返回0'''
        #不符合优先级顺序完成
        NewList=self.TaskData
        NewList.sort(key=lambda x:(x[3],x[4])) #先以优先级排序，再以完成状态排序
        rank_=0;mark=len(NewList)
        ans=1
        for l in NewList:
            if(l[3]>rank_):
                rank_=l[3]
            if(mark):
                if(l[4]=="已完成" and mark<rank_):
                    ans=0
                    print("Error:出现优先级问题")
                    print(f"优先级{l[3]}任务越级完成")
                    #return 0   不break了，可能有多个出问题的任务
            else:
                if(l[4]=="未完成"):
                    mark=rank_
        #超时未完成
        def new_time():#当前时间
            now=time.localtime()
            t=str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+str(now.tm_hour)+str(now.tm_min)
            return int(t)
        now_time=new_time()
        NewList.sort(key=lambda x:x[6])
        for l in NewList:
            if(l[6]<now_time):
                if(l[4]=="未完成"):
                    ans=0
                    print("Error:出现超时问题")
                    print(f"{l[5]}负责的{l[0]}超时仍未完成")
            else:
                break
        #任务重复
        NewList.sort(key=lambda x:x[1])
        for i in range(0,len(NewList)-1):
            if NewList[i][1]==NewList[i+1][1]:
                ans=0
                print(f"Error:{NewList[i][0]}与{NewList[i+1][0]}重复")
        return ans
    def ChangeData(self):
        '''对任务内容的重新修改'''
        n=int(input("输入修改次数:"))
        while(n):
            id_=input("ID:")
            for i in range(len(self.TaskData)):
                if(self.TaskData[i][0]==id_):
                    s=input('任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):').split(' ')
                    while(len(s)!=7):
                        print("Error:输入缺失或盈余！")
                        s=input('任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):').split(' ')
                    s[3]=int(s[3])
                    s[6]=int(s[6])
                    self.TaskData[i]=s
                    break
            n-=1
        self.TaskSort()
        return 1
    def ChangeOneData(self,id,NewTask):
        '''替换单个任务
        失败返回0
        成功返回1'''
        if len(NewTask)!=7:
            print("Error:输入缺失或盈余！")
            return 0
        for i in range(len(self.TaskData)):
            if(self.TaskData[i][0]==id):
                NewTask[3]=int(NewTask[3])
                NewTask[6]=int(NewTask[6])
                self.TaskData[i]=NewTask
                self.TaskSort()
                return 1
    def AddData(self):
        '''对任务内容进行添加'''
        n=int(input("输入添加次数:"))
        while(n):
            s=input('任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):').split(' ')
            if(len(s)!=7):
                print("Error:输入缺失或盈余！")
                continue
            s[3]=int(s[3])
            s[6]=int(s[6])
            self.TaskData.append(s)
            n-=1
        self.TaskSort()
        return 1
    def AddOneData(self,NewTask):
        '''添加单个任务
        失败返回0
        成功返回1'''
        if len(NewTask)!=7:
            print("Error:输入缺失或盈余！")
            return 0
        NewTask[3]=int(NewTask[3])
        NewTask[6]=int(NewTask[6])
        self.TaskData.append(NewTask)
        self.TaskSort()
        return 1
    def DelData(self):
        '''对任务内容进行删除'''
        n=int(input("输入删除次数:"))
        while(n):
            id_=input("输入Id:")
            for i in range(len(self.TaskData)):
                if(self.TaskData[i][0]==id_):
                    self.TaskData.pop(i)
                    break
            n-=1
        self.TaskSort()
        return 1
    def DelOneTask(self,id):
        '''只删除一个任务
        失败返回0
        成功返回1'''
        for i in range(len(self.TaskData)):
            if(self.TaskData[i][0]==id):
                self.TaskData.pop(i)
                self.TaskSort()
                return 1
        return 0


class ProjectControl:
    '''需要整一个权限功能'''
    '''taskcontrol中有errorcheck功能,记得每次操作后调用一下检验是否出现资源冲突'''
    def __init__(self,title=0,description=0,priority=0,leader=0,deadline=0):
        self.ProjectList=[]

        # self.title=title
        # self.description=description
        # self.priority=priority
        # self.leader=leader
        # self.deadline=deadline
        # self.status="PENDING"     #or 'PROGRESSING' 'COMPLETED'
        # self.id=-1
    def AddNewProject(self):
        '''发布项目'''
        s=input("项目名称、描述、开始日期、结束日期(空格分隔):").strip(" ")
        proj=TaskControl()
        proj.DataInput()
        s.append(proj)
        self.ProjectList.append(s)
        return 0
    


#-----------下面是在测试--------------

# a=ProjectControl()
# a.AddNewProject()

b=TaskControl()
b.DataInput()

# 要注意Id是一个字符串，不是数字，调用的时候要注意
# 调试的时候才发现checkpersonaltask和personalpath的写法是一样的（

print(b.CheckPersonalTask("我"),'\n----------------------------\n')
print(b.IdCheck('2'),'\n----------------------------\n')
print(b.PersonalPath("我"),'\n----------------------------\n')
print(b.AllPath(),'\n----------------------------\n')
print(b.ErrorCheck(),'\n----------------------------\n')
print(b.ChangeData(),'\n----------------------------\n')
print(b.AddData(),'\n----------------------------\n')
print(b.DelData(),'\n----------------------------\n')
print(b.CheckPersonalTask("我"),'\n----------------------------\n')
print(b.IdCheck('2'),'\n----------------------------\n')
print(b.PersonalPath("我"),'\n----------------------------\n')
print(b.AllPath(),'\n----------------------------\n')
print(b.ErrorCheck(),'\n----------------------------\n')



#附上最后一次测试结果，目前未发现BUG
'''
任务数量：5
任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):1 吃饭 用嘴吃 3 未完成 我 202511231100
任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):2 做饭 在厨房 2 未完成 你 202511231000
任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):3 买菜 去市场 2 未完成 我 202511230930
任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):4 上课 在教室 1 未完成 我 202511230830
任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):5 睡觉 在家 1 未完成 你 202511230630
end
[['4', '上课', '在教室', 1, '未完成', '我', 202511230830], ['3', '买菜', '去市场', 2, '未完成', '我', 202511230930], ['1', '吃饭', '用嘴吃', 3, '未完成', '我', 202511231100]] 
----------------------------

([['5', '睡觉', '在家', 1, '未完成', '你', 202511230630], ['4', '上课', '在教室', 1, '未完成', '我', 202511230830]], [['1', '吃饭', '用嘴吃', 3, '未完成', '我', 202511231100]]) 
----------------------------

[['4', '上课', '在教室', 1, '未完成', '我', 202511230830], ['3', '买菜', '去市场', 2, '未完成', '我', 202511230930], ['1', '吃饭', '用嘴吃', 3, '未完成', '我', 202511231100]] 
----------------------------

第1级任务：
['5', '睡觉', '在家', 1, '未完成', '你', 202511230630]
['4', '上课', '在教室', 1, '未完成', '我', 202511230830]
第2级任务：
['2', '做饭', '在厨房', 2, '未完成', '你', 202511231000]
['3', '买菜', '去市场', 2, '未完成', '我', 202511230930]
第3级任务：
['1', '吃饭', '用嘴吃', 3, '未完成', '我', 202511231100]
[['5', '睡觉', '在家', 1, '未完成', '你', 202511230630], ['4', '上课', '在教室', 1, '未完成', '我', 202511230830], ['2', '做饭', '在厨房', 2, '未完成', '你', 202511231000], ['3', '买菜', '去市场', 2, '未完成', '我', 202511230930], ['1', '吃饭', '用嘴吃', 3, '未完成', '我', 202511231100]]
----------------------------

Error:出现超时问题
你负责的5超时仍未完成
Error:出现超时问题
我负责的4超时仍未完成
Error:出现超时问题
我负责的3超时仍未完成
Error:出现超时问题
你负责的2超时仍未完成
Error:出现超时问题
我负责的1超时仍未完成
0
----------------------------

输入修改次数:1
ID:1
任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):1 吃饭 用嘴吃 3 未完成 我 202511231300
0
----------------------------

输入添加次数:1
任务ID、标题、描述、优先级、状态、负责人、截止日期(空格作为分割符):6 打游戏 玩Mc 4 未完成 我 202511231430
0
----------------------------

输入添加次数:1
输入Id:2
0 
----------------------------

end
[['4', '上课', '在教室', 1, '未完成', '我', 202511230830], ['3', '买菜', '去市场', 2, '未完成', '我', 202511230930], ['1', '吃饭', '用嘴吃', 3, '未完成', '我', 202511231300], ['6', '打游戏', '玩Mc', 4, '未完 成', '我', 202511231430]]
----------------------------

目标不存在
None
----------------------------

[['4', '上课', '在教室', 1, '未完成', '我', 202511230830], ['3', '买菜', '去市场', 2, '未完成', '我', 202511230930], ['1', '吃饭', '用嘴吃', 3, '未完成', '我', 202511231300], ['6', '打游戏', '玩Mc', 4, '未完 成', '我', 202511231430]]
----------------------------

第1级任务：
['5', '睡觉', '在家', 1, '未完成', '你', 202511230630]
['4', '上课', '在教室', 1, '未完成', '我', 202511230830]
第2级任务：
['3', '买菜', '去市场', 2, '未完成', '我', 202511230930]
第3级任务：
['1', '吃饭', '用嘴吃', 3, '未完成', '我', 202511231300]
第4级任务：
['6', '打游戏', '玩Mc', 4, '未完成', '我', 202511231430]
[['5', '睡觉', '在家', 1, '未完成', '你', 202511230630], ['4', '上课', '在教室', 1, '未完成', '我', 202511230830], ['3', '买菜', '去市场', 2, '未完成', '我', 202511230930], ['1', '吃饭', '用嘴吃', 3, '未完成', '我', 202511231300], ['6', '打游戏', '玩Mc', 4, '未完成', '我', 202511231430]]
----------------------------

Error:出现超时问题
你负责的5超时仍未完成
Error:出现超时问题
我负责的4超时仍未完成
Error:出现超时问题
我负责的3超时仍未完成
0
----------------------------
'''
