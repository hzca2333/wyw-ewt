import requests
import json
import base64
import uuid
import os
import sys
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

def updateLessonSign(homeworkId, lessonId, playTime,clientLessonTime):
    paramVarArgs = [str(clientLessonTime), str(homeworkId), str(lessonId), str(playTime)]

    # 构建拼接字符串
    stringBuilder = "eo^nye1j#!wt2%v)"
    stringBuilder += ''.join(paramVarArgs)
    stringBuilder += "eo^nye1j#!wt2%v)"

    # 计算 MD5 哈希
    md5_hash = hashlib.md5()
    md5_hash.update(stringBuilder.encode())
    return(md5_hash.hexdigest())
def getPassword(paramString1):
    paramString2 = "eo^nye1j#!wt2%v)"
    if paramString1 is not None:
        try:
            key = paramString2.encode('utf-8')
            cipher = AES.new(key, AES.MODE_ECB)
            data = paramString1.encode('utf-8')
            padded_data = pad(data, AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            return base64.b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            print(e)
    return None

def getTaskInfo(homeworkId,lessonId,token):
    payload = {
        "homeworkId": homeworkId,
        "lessonId": lessonId,
    }
    json_payload = json.dumps(payload)
    response_lessonTaskInfo = requests.post(
        "https://gateway.ewt360.com/api/homeworkprod/homework/student/getUserHomeworkLessonTaskInfo", data=json_payload,
        headers={"Content-Type": "application/json; charset=UTF-8", "token": token, "platform": "2",
                 "version": "10.0.1"})
    lessonTaskInfo = response_lessonTaskInfo.json()
    if response_lessonTaskInfo.status_code == 200:
        if lessonTaskInfo['success'] != True:
            print("获取任务信息失败: ",lessonTaskInfo['msg'])
            return 0
        else:
            return lessonTaskInfo['data']['lessonTime']
    else:
        print(lessonTaskInfo)
        return 0

def updateLessonTask(homeworkId,lessonId,playTime,clientLessonTime,token):
    payload = {
        "homeworkId": homeworkId,
        "lessonId": lessonId,
        "playTime": playTime,
        "clientLessonTime": clientLessonTime,
        "sign": updateLessonSign(homeworkId,lessonId,playTime,clientLessonTime)
    }
    json_payload = json.dumps(payload)
    response_updateLessonTask = requests.post(
        "https://gateway.ewt360.com/api/homeworkprod/homework/student/updateUserLessonTaskV2", data=json_payload,
        headers={"Content-Type": "application/json; charset=UTF-8", "token": token, "platform": "2",
                 "version": "10.0.1"})
    updateResult = response_updateLessonTask.json()
    if response_updateLessonTask.status_code == 200:
        if updateResult['success'] != True:
            print("修改课程视频观看时长失败: ",updateResult['msg'])
            return 0
        else:
            return 1
    else:
        print(updateResult)
        return 0
def update_mission(contentId,schoolId,token):
    payload = {
        "sceneId": "0",
        "contentId": contentId,
        "contentType": 3,
        "percent": 1,
        "schoolId": schoolId
    }
    json_payload = json.dumps(payload)
    response_updateMission = requests.post(
        "https://gateway.ewt360.com/api/homeworkprod/homework/student/updateMission", data=json_payload,
        headers={"Content-Type": "application/json; charset=UTF-8", "token": token, "platform": "2",
                 "version": "10.0.1"})
    updateResult = response_updateMission.json()
    if response_updateMission.status_code == 200:
        if updateResult['success'] != True:
            print("修改课程视频观看时长失败: ",updateResult['msg'])
            return 0
        else:
            return 1
    else:
        print(updateResult)
        return 0

file_path = "data/user.json"
host = "https://gateway.ewt360.com"
if not os.path.isfile(file_path):
    print("本地无账号信息，请登录")
    userName = input("用户名:")
    password = input("密码:")

    # 构建请求体数据
    login_payload = {
        "userName": userName,
        "password": getPassword(password),
        "platform": 2,
        "deviceToken": str(uuid.uuid4()),
        "deviceName": "light",
        "isApp": True,
        "appVersion": "10.0.1"
    }

    # 发送POST请求
    response_login = requests.post(host+"/api/authcenter/v2/oauth/login/account", data=json.dumps(login_payload),
                             headers={"Content-Type": "application/json"})
    login_data = response_login.json()
    # 检查响应状态码
    if response_login.status_code == 200:
        # 请求成功
        response_data = response_login.json()
        if (response_data.get("success") != True):
            print(response_data.get("msg"))
            sys.exit()
        else:
            # 获取当前工作目录
            current_directory = os.getcwd()

            # 构建文件夹路径
            folder_path = os.path.join(current_directory, 'data')

            # 创建文件夹（如果不存在）
            os.makedirs(folder_path, exist_ok=True)

            # 构建文件路径
            file_path = os.path.join(folder_path, 'user.json')
            # 将 response_data 保存到本地文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(response_data, file, ensure_ascii=False)
            print("登录成功，账号信息已缓存")
    else:
        # 请求失败
        print("请求失败: ", login_data)
else:
    print("已读取本地账号信息缓存")
# 获取课程列表
with open(file_path, 'r') as file:
    data = json.load(file).get('data')
    userId = data.get('userId')
    token = data.get('token')
    if not token:
        print("读取用户信息时发生错误，请重新登录")
        os.remove('data/user.json')
        print("已清除用户信息缓存")
# 构建请求体数据
payload = {
    "pageIndex": "1",
    "pageSize": "10",
    "status": "2",
    "subject": "",
    "type": ""
}
json_payload = json.dumps(payload)

# 发送POST请求
response_getHomework = requests.post(host+"/api/homeworkprod/homework/student/queryHomeworks", data=json_payload,
                         headers={"Content-Type": "application/json; charset=UTF-8","token": token,"version": "10.0.1","platform": "2"})
homework_data = response_getHomework.json()
if response_getHomework.status_code == 200:
    if homework_data.get("success") != True:
        print("获取作业列表失败：",homework_data.get("msg"))
    else:
        print("共找到",homework_data.get("data").get("totalRecords"),"个作业")
        homework_objects = homework_data['data']['data']
        # 提取每个 JSON 对象的 title 字段的值
        i = 0
        for homework_obj in homework_objects:
            i = i+1
            title = homework_obj['title']
            homeworkId = homework_obj['homeworkId']
            schoolId = homework_obj['schoolId']
            print(i,".",title," id:",homeworkId)
else:
    print(homework_data)
while True:
    try:
        homeworkIndex = int(input("请输入作业序号: "))
        if homeworkIndex <= 0:
            print("输入的必须是正整数，请重新输入")
        else:
            homework = homework_objects[homeworkIndex-1]
            subjects_objects = homework['subjects']
            for subject_obj in subjects_objects:
                text = subject_obj['text']
                code = subject_obj['code']
                print("学科:", text, " id:", code)
            break
    except ValueError:
        print("输入的必须是正整数，请重新输入")
while True:
    subjectId = input("请输入学科ID: ")
    if subjectId == "exit":
        break
    while True:
        try:
            subjectId = int(subjectId)
            if subjectId <= 0:
                print("输入的必须是正整数，请重新输入")
            else:
                break
        except ValueError:
            print("输入的必须是正整数，请重新输入")
    homeworkId = homework['homeworkId']

    #获取用户选择的科目下的任务

    payload = {
        "schoolId": int(schoolId),
        "sceneId": "0",
        "homeworkIds": [int(homeworkId)],
        "pageIndex": 1,
        "pageSize": 100,
        "subjectId": subjectId
    }
    json_payload = json.dumps(payload)
    response_pageHomeworkTasks = requests.post(host+"/api/homeworkprod/homework/student/pageHomeworkTasks", data=json_payload,
                             headers={"Content-Type": "application/json; charset=UTF-8","token": token})
    pageHomeworkTasks_data = response_pageHomeworkTasks.json()
    if response_pageHomeworkTasks.status_code == 200:
        if pageHomeworkTasks_data['success'] != True:
            print("获取课程任务失败: ",pageHomeworkTasks_data['msg'])
        else:
            print("共找到",pageHomeworkTasks_data['data']['totalRecords'],"个课程任务")
            tasks_objects = pageHomeworkTasks_data['data']['data']
            i = 0
            for task_obj in tasks_objects:
                i = i+1
                title = task_obj['title']
                print(i,".",title)
    else:
        print(pageHomeworkTasks_data)
    while True:
        taskIndex = input("请输入课程任务序号(输入0将对应学科的全部视频播放完成度修改至100%): ")
        if taskIndex == "exit":
            break
        elif int(taskIndex) == 0:
            i = 0
            for task_obj in tasks_objects:
                i = i+1
                lessonId = task_obj['contentId']
                contentType = int(task_obj['contentType'])
                if contentType == 1:
                    lessonTime = getTaskInfo(homeworkId,lessonId,token)
                    if updateLessonTask(homeworkId,lessonId,lessonTime,lessonTime,token) == 1:
                        print("修改成功，当前进度 ",i,"/",pageHomeworkTasks_data['data']['totalRecords'])
                    else:
                        print("第",i,"次修改失败，","当前进度 ",i,"/",pageHomeworkTasks_data['data']['totalRecords'])
                elif contentType == 3:
                    if update_mission(task_obj['contentId'],schoolId,token) == 1:
                        print("(FM电台)修改成功，当前进度 ",i,"/",pageHomeworkTasks_data['data']['totalRecords'])
                    else:
                        print("(FM电台)第", i, "次修改失败，", "当前进度 ", i, "/",pageHomeworkTasks_data['data']['totalRecords'])
                else:
                    print("不支持的类型，已跳过")
            print("修改完成")
        elif int(taskIndex) < 0:
            print("课程任务序号必须大于或等于0，请重新输入")
        else:
            task = tasks_objects[int(taskIndex)-1]
            lessonId = task['contentId']
            contentType = int(task['contentType'])
            if contentType == 1:
                lessonTime = getTaskInfo(homeworkId, lessonId, token)
                if updateLessonTask(homeworkId, lessonId, lessonTime, lessonTime, token) == 1:
                    print("修改成功")
                else:
                    print("修改失败")
            elif contentType == 2:
                #根据paperId获取题目列表
                paperId = task['contentId']
                url = "https://web.ewt360.com/customerApi/api/studyprod/app/answer/paper?paperId=",paperId,"&reportId=0&platform=1&bizCode=204&homeworkId=0&token=",token
                response_questions = requests.get(url,
                    headers={"Content-Type": "application/json; charset=UTF-8", "token": token, "platform": "1",
                             "version": "10.0.1"})
                questions_data = response_questions.json()
                if response_questions.status_code == 200:
                    if questions_data['success'] != True:
                        print("获取题目列表失败: ", questions_data['msg'])
                    else:
                        #获取reportId
                        reportId = 0
                        url = "https://web.ewt360.com/customerApi/api/studyprod/app/answer/report?paperId=",paperId,"&reportId=0&platform=1&bizCode=204&homeworkId=0&token=", token
                        response_report = requests.get(url,
                                                       headers={"Content-Type": "application/json; charset=UTF-8", "token": token, "platform": "1",
                                     "version": "10.0.1"})
                        report_data = response_report.json()
                        if response_report.status_code == 200:
                            if report_data['success'] != True:
                                print("获取reportId失败: ", questions_data['msg'])
                            else:
                                reportId = report_data['data']['reportId']
                        else:
                            print(response_report)

                        questions = questions_data['data']['questions']
                        for question_obj in questions:
                            qid = question_obj['qid']
                else:
                    print(questions_data)
            elif contentType == 3:
                if update_mission(task_obj['contentId'], schoolId, token) == 1:
                    print("(FM电台)修改成功")
                else:
                    print("(FM电台)修改失败")
            else:
                print("不支持的类型，已跳过")
