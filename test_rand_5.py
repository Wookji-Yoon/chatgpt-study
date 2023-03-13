import json
import csv
import random

from util import get_json_for_one_candidate, csv_transform
from config import BASE_PROMPT_FILENAME


# 1. 파일명은 Prompt 텍스트 파일 명에에 따라 달라짐
file_name = BASE_PROMPT_FILENAME.split(".")[0]


# 2. 1부터 84까지의 숫자 중에서 5개를 선택하여 리스트에 저장
selected_numbers = random.sample(range(1, 85), 5)
print("***********************test start")


# 3. 다섯 명의 random 후보자에 대한 api 응답 결과를 json 파일로 생성
result_dict = {}

for i in selected_numbers:
    id = '{:03d}'.format(i)
    data = get_json_for_one_candidate(i)

    result_dict[id] = data

    print(id + " completed")

with open(f"result/json/{file_name}_test.json", "w", encoding="utf-8") as outfile:
    json.dump(result_dict, outfile, ensure_ascii=False, indent=4)

# 4. json 응답 결과를 점수로 변환한 csv 파일 생성

with open(f"result/csv/{file_name}_test.csv", "w", newline='', encoding="utf-8") as f:
    csv_data = csv.writer(f)
    csv_transform(csv_data, result_dict)
