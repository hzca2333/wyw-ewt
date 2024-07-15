import requests
import json
import base64
import uuid
import os
import sys
import hashlib
import time
from datetime import datetime
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

#生成修改课程观看时长所需签名

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

#生成登录密码

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

#获取课程视频时长

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

#修改课程视频观看时长
    
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
    
#修改电台观看状态
    
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
    
#获取schoolId 
    
def getSchoolUserInfo(token):
    response_schoolUserInfo = requests.get(
        "https://gateway.ewt360.com/api/eteacherproduct/school/getSchoolUserInfo",
        headers={"Content-Type": "application/json; charset=UTF-8", "token": token, "platform": "2",
                 "version": "10.0.1"})
    userInfo = response_schoolUserInfo.json()
    if response_schoolUserInfo.status_code == 200:
        if userInfo['success'] != True:
            return 0
        else:
            schoolId = userInfo['data']['schoolId']
            return schoolId
    else:
        print(userInfo)
        return 0
    
if __name__ == "__main__":
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
    with open(file_path, 'r') as file:
        data = json.load(file).get('data')
        userId = data.get('userId')
        token = data.get('token')
        if not token:
            print("读取用户信息时发生错误，请重新登录")
            os.remove('data/user.json')
            print("已清除用户信息缓存")

    headers = {"Content-Type": "application/json; charset=UTF-8", "token": token, "platform": "2",
                    "version": "10.0.1"}
    # 获取schoolId
            
    schoolId = getSchoolUserInfo(token)

    # 获取假期任务ID homeworkId
    timestamp = int(round(time.time() * 1000))
    response_getHomework = requests.get("https://gateway.ewt360.com/api/homeworkprod/homework/student/holiday/getHomeworkSummaryInfo?schoolId="+str(schoolId)+"&timestamp="+ str(timestamp) +"&sceneId=136",headers=headers)
    homework_data = response_getHomework.json()
    if response_getHomework.status_code == 200:
        if homework_data.get("success") != True:
            print("获取假期计划失败：",homework_data.get("msg"))
        else:
            homework_data = homework_data['data']
            # 提取每个 JSON 对象的 title 字段的值
            title = homework_data['homeworkTitle']
            homeworkId = homework_data['homeworkIds'][0]
            print(title," id:",homeworkId)
    else:
        print(homework_data)

    # 获取days
        
    days = []
    days_body = {"homeworkIds":[int(homeworkId)],"isSelfTask":False,"userOptionTaskId":None,"schoolId":21669,"sceneId":"136"}
    response_getDays = requests.post("https://gateway.ewt360.com/api/homeworkprod/homework/student/holiday/getHomeworkDistribution",data = json.dumps(days_body),headers=headers)
    days_resp = response_getDays.json()
    if response_getDays.status_code == 200:
        if days_resp.get("success") != True:
            print("获取days失败：",days_resp.get("msg"))
        else:
            days_data = days_resp["data"]["days"]
            i = 0
            print("0 .","全部")
            for days_obj in days_data:
                i += 1
                timestamp_day = days_obj['day']/1000.0
                date_time_obj = datetime.fromtimestamp(timestamp_day)
                formatted_date = date_time_obj.strftime('%Y-%m-%d')
                print(i,". ",formatted_date,"dayId:",days_obj['dayId'][0])
                days.append(days_obj['dayId'][0])
    else:
        print(days_resp)

    while True:
        dayIds = []
        dayId = input("请输入day序号: ")
        if dayId == "exit":
            break
        elif dayId == "0":
            dayIds = days
        else:
            dayIds.append(days[int(dayId)-1])

        # 获取作业任务
        tasks_body = {"dayId":dayIds,
                    "day":1706889600000,"status":0,
                    "homeworkIds":[10271071],
                    "isSelfTask":False,
                    "userOptionTaskId":None,
                    "pageIndex":1,
                    "pageSize":1145,
                    "missionType":0,
                    "schoolId":schoolId,
                    "sceneId":"136"}
        response_getTasks = requests.post(host+"/api/homeworkprod/homework/student/holiday/pageHomeworkTasks",data = json.dumps(tasks_body),headers=headers)
        tasks_resp = response_getTasks.json()
        if response_getTasks.status_code == 200:
            if tasks_resp.get("success") != True:
                print("获取作业任务失败：",tasks_resp.get("msg"))
            else:
                tasks_objects = tasks_resp['data']['data']
                i= 0
                for task_obj in tasks_objects:
                    i = i+1
                    lessonId = task_obj['contentId']
                    contentType = int(task_obj['contentType'])
                    if contentType == 1:
                        lessonTime = getTaskInfo(homeworkId,lessonId,token)
                        if updateLessonTask(homeworkId,lessonId,lessonTime,lessonTime,token) == 1:
                            print("修改成功，当前进度 ",i,"/",tasks_resp['data']['totalRecords'])
                        else:
                            print("第",i,"次修改失败，","当前进度 ",i,"/",tasks_resp['data']['totalRecords'])
                    elif contentType == 3:
                        if update_mission(task_obj['contentId'],schoolId,token) == 1:
                            print("(FM电台)修改成功，当前进度 ",i,"/",tasks_resp['data']['totalRecords'])
                        else:
                            print("(FM电台)第", i, "次修改失败，", "当前进度 ", i, "/",tasks_resp['data']['totalRecords'])
                    else:
                        print("不支持的类型，已跳过")
                print("修改完成")
        else:
            print(tasks_resp)
