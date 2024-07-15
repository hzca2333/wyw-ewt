import main

token = input("token:")
token = "142312096-1-77bc49ce527f8bf7"
homeworkId = input("homeworkId:")
homeworkId = "10271071"
lessonId = input("lessonId:")
playTime = input("playTime:")

lessonTime = main.getTaskInfo(homeworkId,lessonId,token)

if main.updateLessonTask(homeworkId,lessonId,playTime,playTime,token) == 1:
    print("成功")
else:
    print("失败")