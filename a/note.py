import aiohttp
import asyncio

async def make_request(session, url, headers, data, current_attempt, total_attempts):
    async with session.post(url, headers=headers, json=data) as response:
        result = await response.json()
        print(f"Attempt {current_attempt}/{total_attempts} - Response Code: {response.status}, Result: {result}")
        return result

async def run_requests(url, headers, data, total_attempts, interval, batch_size, pause_duration):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for current_attempt in range(1, total_attempts + 1):
            task = make_request(session, url, headers, data, current_attempt, total_attempts)
            tasks.append(task)

            if current_attempt % batch_size == 0:
                await asyncio.sleep(pause_duration)

        results = await asyncio.gather(*tasks)
        return results

if __name__ == '__main__':
    url = "https://gateway.ewt360.com/api/studynoteprod/student/batchAddStudyNotes"
    headers = {'token': '142312096-1-77bc49ce527f8bf7'}
    data = {
        "day": 1706889600000,
        "homeworkId": 10271071,
        "filePathList": ["http://speedtest.zju.edu.cn/10G"],
        "subjectId": 1,
        "schoolId": 0
    }

    total_attempts = int(input("Enter the number of attempts: "))
    interval = 0.01  # 每次请求之间的间隔时间（秒）
    batch_size = 5   # 每5次请求后停顿
    pause_duration = 1  # 每次停顿的时间（秒）

    results = asyncio.run(run_requests(url, headers, data, total_attempts, interval, batch_size, pause_duration))

    # 输出所有请求的结果
    print("All results:", results)
