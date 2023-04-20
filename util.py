import json
import openai

from config import BASE_PROMPT, SUMMARY_PROMPT, OPENAI_API_KEY, SYSTEM_PROMPT, RUBRIC, CONTENT, SCORE, MODEL, TEMPERATURE

# 1. prompt
base_prompt = BASE_PROMPT
system_prompt = SYSTEM_PROMPT
summary_prompt = SUMMARY_PROMPT

# 3. rubric & score data
with open(RUBRIC, 'r', encoding='UTF8') as f:
    rubric_data = json.load(f)
with open(SCORE, 'r', encoding='utf-8') as f:
    score_data = json.load(f)

# 4. 자기소개서 data
with open(CONTENT, 'r', encoding='UTF8') as f:
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
        user_prompt = base_prompt + f"\n\n[Question]\n{question}" + f"\n\n[Rubric]\n{rubric}" + \
            f"\n\n[Content]\n{content}" + "\n\n[Assistant]\nRating is: "

    if question_number == 2:
        category = content_data[candidate_str]["answer"]["q2_category"]
        user_prompt = base_prompt + f"\n\n[Question]\n{question}" + f"\n\n[Rubric]\n{rubric}" + \
            f"\n[Content]\nMy field of interest: {category}.\n{content}" + \
            "\n\n[Assistant]\nRating is: "

    return user_prompt


def openai_chatcompletion(candidate_id: int, question_number: int, repeat: int = 1):
    completion = openai.ChatCompletion.create(model=MODEL, messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": generate_prompt(
            candidate_id, question_number)},
    ], temperature=TEMPERATURE, n=repeat)
    print("openai chatcompletion completed for " +
          str(candidate_id) + " q" + str(question_number))

    return [completion.choices[i]["message"]["content"] for i in range(repeat)]


def openai_summary_chatcompletion(text: str):
    completion = openai.ChatCompletion.create(model=MODEL, messages=[
        {"role": "user", "content": summary_prompt + "\n\n[Text]\n" + text}], temperature=0)
    return completion.choices[0]["message"]["content"]


"""
def get_json_util(candidate_id: int):
    # 한 사람에 대한 result 추출
    result = {}
    result["q1"] = openai_chatcompletion(candidate_id, 1)
    result["q2"] = openai_chatcompletion(candidate_id, 2)
    result["q3"] = openai_chatcompletion(candidate_id, 3)
    result["q4"] = openai_chatcompletion(candidate_id, 4)

    # "001" 형태로 변환
    candidate_str = '{:03d}'.format(candidate_id)

    data = {}
    data["id"] = content_data[candidate_str]["id"]
    data["name"] = content_data[candidate_str]["name"]
    data["result"] = result

    return data
"""


def get_json_for_one_candidate(candidate_id: int, repeat: int = 1):

    # 1. openai API에서 응답받기
    # 여기서 response의 type은 list이다. repeat 횟수만큼의 응답이 담겨있다.
    response1 = openai_chatcompletion(candidate_id, 1, repeat)
    response2 = openai_chatcompletion(candidate_id, 2, repeat)
    response3 = openai_chatcompletion(candidate_id, 3, repeat)
    response4 = openai_chatcompletion(candidate_id, 4, repeat)

    # 원래 아래 코드는 reponse1,2,3,4가 json 하나라고 생각하고 코드를 짰다.
    # 그런데 이제 response1,2,3,4는 json 여러개가 담긴 list이다. 이걸 고려해서 코드를 수정해야 한다.

    # 2. result_with_opinion을 json으로 추출
    result_with_opinion_list = []

    for i in range(1, repeat+1):
        globals()["result_with_opinion_"+str(i)] = {}
        globals()["result_with_opinion_"+str(i)]["q1"] = response1[i-1]
        globals()["result_with_opinion_"+str(i)]["q2"] = response2[i-1]
        globals()["result_with_opinion_"+str(i)]["q3"] = response3[i-1]
        globals()["result_with_opinion_"+str(i)]["q4"] = response4[i-1]

        result_with_opinion_list.append(
            globals()["result_with_opinion_"+str(i)])

    print("result_with_opinion finished", candidate_id)

    # 3. openai API에서 result_summary 응답받기

    result_summary_list = []

    for i in range(1, repeat+1):
        globals()["result_summary_"+str(i)] = {}
        globals()["result_summary_"+str(i)
                  ]["q1"] = openai_summary_chatcompletion(response1[i-1])
        globals()["result_summary_"+str(i)
                  ]["q2"] = openai_summary_chatcompletion(response2[i-1])
        globals()["result_summary_"+str(i)
                  ]["q3"] = openai_summary_chatcompletion(response3[i-1])
        globals()["result_summary_"+str(i)
                  ]["q4"] = openai_summary_chatcompletion(response4[i-1])

        result_summary_list.append(globals()["result_summary_"+str(i)])

    print("result_summary finished", candidate_id)

    # 4. "001" 형태로 변환 및 프로필 데이터 가져오기
    candidate_str = '{:03d}'.format(candidate_id)

    id_number = content_data[candidate_str]["id"]
    name = content_data[candidate_str]["name"]

    # 5. data에 담기

    data_with_opinion_list = []
    data_summary_list = []

    for i in range(1, repeat+1):
        globals()["data_with_opinion_"+str(i)] = {}
        globals()["data_with_opinion_"+str(i)]["id"] = id_number
        globals()["data_with_opinion_"+str(i)]["name"] = name
        globals()["data_with_opinion_"+str(i)
                  ]["result"] = result_with_opinion_list[i-1]

        data_with_opinion_list.append(globals()["data_with_opinion_"+str(i)])

        globals()["data_summary_"+str(i)] = {}
        globals()["data_summary_"+str(i)]["id"] = id_number
        globals()["data_summary_"+str(i)]["name"] = name
        globals()["data_summary_"+str(i)]["result"] = result_summary_list[i-1]

        data_summary_list.append(globals()["data_summary_"+str(i)])

    return data_with_opinion_list, data_summary_list

    """ 20130417에 삭제----------------------------------------------------------------아래부터 원본 코드

    # 2. result_with_opinion을 json으로 추출
    result_with_opinion = {}
    result_with_opinion["q1"] = response1
    result_with_opinion["q2"] = response2
    result_with_opinion["q3"] = response3
    result_with_opinion["q4"] = response4

    print("result_with_opinion finished", candidate_id)

    # 3. openai API에서 result_summary 응답받기
    result_summary = {}
    result_summary["q1"] = openai_summary_chatcompletion(response1)
    result_summary["q2"] = openai_summary_chatcompletion(response2)
    result_summary["q3"] = openai_summary_chatcompletion(response3)
    result_summary["q4"] = openai_summary_chatcompletion(response4)

    print("result_summary finished", candidate_id)

    # 4. "001" 형태로 변환
    candidate_str = '{:03d}'.format(candidate_id)

    # 5. data에 담기
    data_with_opinion = {}
    data_with_opinion["id"] = content_data[candidate_str]["id"]
    data_with_opinion["name"] = content_data[candidate_str]["name"]
    data_with_opinion["result"] = result_with_opinion

    data_summary = {}
    data_summary["id"] = content_data[candidate_str]["id"]
    data_summary["name"] = content_data[candidate_str]["name"]
    data_summary["result"] = result_summary

    return [data_with_opinion, data_summary]
"""


"""     if IS_SUMMARY_NEED == False:
        return get_json_util(candidate_id)
    if IS_SUMMARY_NEED == True:
        response1 = openai_chatcompletion(candidate_id, 1)
        response2 = openai_chatcompletion(candidate_id, 2)
        response3 = openai_chatcompletion(candidate_id, 3)
        response4 = openai_chatcompletion(candidate_id, 4)

        result = {}
        result["q1"] = openai_summary_chatcompletion(response1)
        print("q1 summary completed")
        result["q2"] = openai_summary_chatcompletion(response2)
        print("q2 summary completed")
        result["q3"] = openai_summary_chatcompletion(response3)
        print("q3 summary completed")
        result["q4"] = openai_summary_chatcompletion(response4)
        print("q4 summary completed")

        # "001" 형태로 변환
        candidate_str = '{:03d}'.format(candidate_id)

        data = {}
        data["id"] = content_data[candidate_str]["id"]
        data["name"] = content_data[candidate_str]["name"]
        data["result"] = result

        return data """


def csv_transform(csv_data, json_data):
    # 1. csv 파일에 header 쓰기
    cols = ["id", "name", "q1", "q2", "q3", "q4"]
    for i in range(1, 5):
        for j in range(1, 6):
            cols.append(f"q{i}c{j}")
            cols.append(f"score_q{i}c{j}")

    csv_data.writerow(cols)

    # 2. 사람 별로 row 쓰기

    error_list = []

    for candidate_id in json_data:
        print(candidate_id, " csv transformed")
        row = []

        # id, name 쓰기
        row.append(json_data[candidate_id]["id"])
        row.append(json_data[candidate_id]["name"])

        # total score array 미리 생성
        total_score_array = []

        # 질문 별로 data 클렌징해서 쓰기
        for i in range(1, 5):
            result = json_data[candidate_id]["result"][f'q{i}']
            result = result.replace(".", "").replace(
                '"', "").replace("'", "").replace("\n", "")

            c1 = result.split(', ')[0].split(': ')[1]
            c2 = result.split(', ')[1].split(': ')[1]
            c3 = result.split(', ')[2].split(': ')[1]
            c4 = result.split(', ')[3].split(': ')[1]

            if c1 in score_data[f'q{i}']["c1"]:
                score1 = score_data[f'q{i}']["c1"][c1]
            else:
                c1 = "error"
                score1 = 0

            if c2 in score_data[f'q{i}']["c2"]:
                score2 = score_data[f'q{i}']["c2"][c2]
            else:
                c2 = "error"
                score2 = 0

            if c3 in score_data[f'q{i}']["c3"]:
                score3 = score_data[f'q{i}']["c3"][c3]
            else:
                c3 = "error"
                score3 = 0

            if c4 in score_data[f'q{i}']["c4"]:
                score4 = score_data[f'q{i}']["c4"][c4]
            else:
                c4 = "error"
                score4 = 0

            try:
                c5 = result.split(', ')[4].split(': ')[1]
                if c5 in score_data[f'q{i}']["c5"]:
                    score5 = score_data[f'q{i}']["c5"][c5]
                else:
                    c5 = "error"
                    score5 = 0
            except:
                c5 = ' '
                score5 = 0

            total_score_array.append(score1+score2+score3+score4+score5)
            row.extend([c1, score1, c2, score2, c3,
                       score3, c4, score4, c5, score5])
            if c1 == "error" or c2 == "error" or c3 == "error" or c4 == "error" or c5 == "error":
                error_list.append(candidate_id+"_q"+str(i))

        # total score 기본 row에 update하기
        row[2:2] = total_score_array
        csv_data.writerow(row)

    return error_list
