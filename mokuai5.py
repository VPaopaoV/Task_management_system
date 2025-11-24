from datetime import datetime
tasks=[
    {"ID":"001","title":"报表分析","assignee":"张三","status":"进行中","deadline":"2025-11-26"},
    {"ID":"002","title":"写作通信","assignee":"李四","status":"已完成","deadline":"2025-11-26"},
]
contribution={}
for i in tasks:
    person = i["assignee"]
    contribution[person]=contribution.get(person,[])+[i["title"]]
status_fenbu = {"待处理":[],"进行中":[],"已完成":[]}
for j in tasks:
    status_fenbu[j["status"]].append(j["name"])
import datetime
now =datetime.datetime.now()
near_days={}
for k in tasks:
    due = datetime.datetime.strftime(k["deadline"], "%Y-%m-%d")
    if 0<=(due-now)<3:
        near_days.append(f"{k['title']}({k['assignee']},{k['deadline']}")
print("每人任务贡献")
for p, ts in contribution.items():
    print(f"{p}: {', '.join(ts)}")
print("\n任务状态分布")
for s, ts in status_fenbu.items():
    print(f"{s}: {', '.join(ts)}")
print("\n快过期任务")
print("\n".join(near_days) if near_days else "无")