import json
import csv

from util import get_json_for_one_candidate, csv_transform
from config import BASE_PROMPT_FILENAME

# 1. repeat 횟수에 따라 반복됨
number_of_repeat = 3

# 2. 파일명은 Prompt 텍스트 파일 명에에 따라 달라짐
file_name = BASE_PROMPT_FILENAME.split(".")[0]

# 3. 전체 후보자에 대한 api 응답 결과를 json 파일로 생성
for repeat in range(number_of_repeat):
    print(f"************************ Repeat {repeat+1} started")

    result_dict = {}

    for i in range(1, 85):
        id = '{:03d}'.format(i)
        data = get_json_for_one_candidate(i)

        result_dict[id] = data

        print(id + " completed")

    with open(f"result/json/{file_name}_{repeat+1}.json", "w", encoding="utf-8") as outfile:
        json.dump(result_dict, outfile, ensure_ascii=False, indent=4)

# 4. json 응답 결과를 점수로 변환한 csv 파일 생성

    with open(f"result/csv/{file_name}_{repeat+1}.csv", "w", newline='', encoding="utf-8") as f:
        csv_data = csv.writer(f)
        csv_transform(csv_data, result_dict)
