import json
import openai

from config import BASE_PROMPT_FILENAME, OPENAI_API_KEY, SYSTEM_PROMPT

# 1. base_prompt
with open("prompt/"+BASE_PROMPT_FILENAME, 'r', encoding='UTF8') as f:
    base_prompt = f.read()

# 2. system_prompt
system_prompt = SYSTEM_PROMPT

# 3. rubric data
with open("src/Rubric.json", 'r', encoding='UTF8') as f:
    rubric_data = json.load(f)

# 4. 자기소개서 data
with open("src/Content.json", 'r', encoding='UTF8') as f:
    content_data = json.load(f)

# 5. openai api key
openai.api_key = OPENAI_API_KEY


def generate_prompt(candidate_id: int, question_number: int):
    # "001" 형태로 변환
    candidate_str = '{:03d}'.format(candidate_id)
    # "q1" 형태로 변환
    question_str = "q"+str(question_number)

    # text 데이터 세팅
    question = rubric_data[question_str]["question"]
    rubric = rubric_data[question_str]["rubric"]
    content = content_data[candidate_str]["answer"][question_str]

    # base prompt로부터 prompt 생성, 단 2번 문항일 경우 category 추가
    if question_number != 2:
        user_prompt = base_prompt + f"\n[Question]\n{question}" + f"\n[Rubric]\n{rubric}" + \
            f"\n[Content]\n{content}" + "\n[Assistant]\nRating is: "

    if question_number == 2:
        category = content_data[candidate_str]["answer"]["q2_category"]
        user_prompt = base_prompt + f"\n[Question]\n{question}" + f"\n[Rubric]\n{rubric}" + \
            f"\n[Content]\n제가 관심있는 분야는 {category}입니다.\n{content}" + \
            "\n[Assistant]\nRating is: "

    return user_prompt


def openai_chatcompletion(candidate_id: int, question_number: int):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": generate_prompt(
            candidate_id, question_number)}
    ], temperature=0.3)
    return completion


def get_json_for_one_candidate(candidate_id: int):
    # 한 사람에 대한 result 추출
    result = {}
    result["q1"] = openai_chatcompletion(
        candidate_id, 1).choices[0]["message"]["content"]
    result["q2"] = openai_chatcompletion(
        candidate_id, 2).choices[0]["message"]["content"]
    result["q3"] = openai_chatcompletion(
        candidate_id, 3).choices[0]["message"]["content"]
    result["q4"] = openai_chatcompletion(
        candidate_id, 4).choices[0]["message"]["content"]

    # "001" 형태로 변환
    candidate_str = '{:03d}'.format(candidate_id)

    data = {}
    data["id"] = content_data[candidate_str]["id"]
    data["name"] = content_data[candidate_str]["name"]
    data["result"] = result

    return data


def csv_transform(csv_data, json_data):
    # 1. score data 불러오기
    with open("src/Score.json", 'r', encoding='utf-8') as f:
        score_data = json.load(f)

    # 2. 열 이름 쓰기
    cols = ["id", "name", "q1", "q2", "q3", "q4"]
    for i in range(1, 5):
        for j in range(1, 6):
            cols.append(f"q{i}c{j}")
            cols.append(f"score_q{i}c{j}")

    csv_data.writerow(cols)

    # 3. 사람 별로 row 쓰기
    for candidate_id in json_data:
        row = []

        # id, name 쓰기
        row.append(json_data[candidate_id]["id"])
        row.append(json_data[candidate_id]["name"])

        # total score array 미리 생성
        total_score_array = []

        # 질문 별로 data 클렌징해서 쓰기
        for i in range(1, 5):
            print(candidate_id, i)
            result = json_data[candidate_id]["result"][f'q{i}']
            result = result.replace('A.', 'A').replace('B.', 'B').replace(
                'C.', 'C').replace("Yes.", "Yes").replace("No.", "No")
            c1 = result.split(', ')[0].split(': ')[1]
            c2 = result.split(', ')[1].split(': ')[1]
            c3 = result.split(', ')[2].split(': ')[1]
            c4 = result.split(', ')[3].split(': ')[1]
            score1 = score_data[f'q{i}']["c1"][c1]
            score2 = score_data[f'q{i}']["c2"][c2]
            score3 = score_data[f'q{i}']["c3"][c3]
            score4 = score_data[f'q{i}']["c4"][c4]
            try:
                c5 = result.split(', ')[4].split(': ')[1]
                score5 = score_data[f'q{i}']["c5"][c5]
            except:
                c5 = ' '
                score5 = 0

            total_score_array.append(score1+score2+score3+score4+score5)
            row.extend([c1, score1, c2, score2, c3,
                       score3, c4, score4, c5, score5])

        # total score 기본 row에 update하기
        row[2:2] = total_score_array
        csv_data.writerow(row)
