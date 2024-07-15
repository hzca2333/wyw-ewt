import requests
import time

def make_request(url, headers, data, current_attempt, total_attempts):
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    print(f"Attempt {current_attempt}/{total_attempts} - Response Code: {response.status_code}, Result: {result}")
    return result

def run_requests(url, headers, data, total_attempts):
    results = []
    for current_attempt in range(1, total_attempts + 1):
        result = make_request(url, headers, data, current_attempt, total_attempts)
        results.append(result)

    return results

if __name__ == '__main__':
    url = "https://gateway.ewt360.com/api/studynoteprod/student/batchAddStudyNotes"
    headers = {'token': '142312096-1-fe856686b142ff7a'}
    data = {
        "day": 1707062400000,
        "homeworkId": 10271071,
        "filePathList": ["1"],
        "subjectId": 2,
        "schoolId": 0
    }

    total_attempts = int(input("Enter the number of attempts: "))

    results = run_requests(url, headers, data, total_attempts)