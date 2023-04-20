import json
import csv
import datetime
from util import get_json_for_one_candidate, csv_transform
from config import REPEAT, CANDIDATE, FILENAME

# 변수 선언
number_of_repeat = REPEAT
number_of_candidates = CANDIDATE
file_name = FILENAME

# 3. 전체 후보자에 대한 api 응답 결과를 list에 담기

# 3-1. 전체 data를 담을 list와 repeact 횟수만큼의 dict를 생성
result_with_opinion_list = []
result_summary_list = []

for i in range(0, number_of_repeat):
    globals()[f"result_with_opinion_{i}"] = {}
    globals()[f"result_summary_{i}"] = {}

# 3-2. 각 후보자에 대한 api 응답 결과를 dict엔 넣기
for i in range(1, number_of_candidates+1):
    id = '{:03d}'.format(i)
    try:  # error가 발생할 수도 있으므로 예외처리
        data = get_json_for_one_candidate(i, number_of_repeat)
        for j in range(0, number_of_repeat):
            globals()[f"result_with_opinion_{j}"][id] = data[0][j]
            globals()[f"result_summary_{j}"][id] = data[1][j]
    except:  # error 발생 시 error 발생한 후보자의 id를 출력
        print(id + " error")

    print(id + " completed")

# 3-3. dict를 list에 넣기
for i in range(0, number_of_repeat):
    result_with_opinion_list.append(globals()[f"result_with_opinion_{i}"])
    result_summary_list.append(globals()[f"result_summary_{i}"])

# 파일명 uniqueness를 위한 시간 변수 생성
current_time = datetime.datetime.now()
time_string = current_time.strftime("%Y%m%d%H%M%S")


# 4. dict 안의 각 list를 json 파일로 변환하기

for i in range(0, number_of_repeat):

    with open(f"result/json/{file_name}_with_opinion_{i+1} 반복_{time_string}.json", "w", encoding="utf-8") as outfile:
        json.dump(result_with_opinion_list[i], outfile,
                  ensure_ascii=False, indent=4)

    with open(f"result/json/{file_name}_summary_{i+1} 반복_{time_string}.json", "w", encoding="utf-8") as outfile:
        json.dump(result_summary_list[i], outfile,
                  ensure_ascii=False, indent=4)

# 5. json 응답 결과를 점수로 변환한 csv 파일 생성
# 5-1 error list를 통한 csv 변경 오류 처리
error_dict = {}

for i in range(0, number_of_repeat):
    with open(f"result/csv/{file_name}_{i+1} 반복_{time_string}.csv", "w", newline='', encoding="utf-8") as f:
        csv_data = csv.writer(f)
        error_list = csv_transform(csv_data, result_summary_list[i])
        error_dict[i+1] = error_list

print("************************ All completed ************************")
# 5. error list 출력
print("************************ Error List ************************")
print(error_dict)
