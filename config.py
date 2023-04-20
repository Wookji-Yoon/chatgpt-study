import os

# 조작변인 1. Temperature ([0.5, 1.0, 0.5])
TEMPERATURE = 1.0
# 조작변인 2. Grade
# A, B, C
# High, Average, Low
# Excellent, Great, Need Improvement

RUBRIC = "src/Rubric_Good.json"
SCORE = "src/Score_High.json"

# 반복횟수 설정
REPEAT = 3
# 후보자수 설정 (전체 후보자 수를 넣고 싶으면 84로 입력할 것)
CANDIDATE = 84
# 파일명 설정
FILENAME = "GOOD_1.0"

# OPENAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-3.5-turbo-0301"

# 자기소개서
CONTENT = "src/Content.json"

# PROMPT
SYSTEM_PROMPT = "You are a helpful assistant that helps HR Personnel for the cover letter evaluation."

BASE_PROMPT = 'Context: The HRM/HRD training program called "Next Generation HR Academy" is recruiting candidates. HR personnel will evaluate the cover letters submitted by the candidates.\n\
Info: "Next Generation HR Academy" or "Next Generation" or "HR Academy" are proper noun.\n\
Provide: cover-letter question, cover-letter content, rubric(criteria w/ rating grades),\n\
Assistant Need to do: Provide ratings for each criteria in accordance with the rubric, and include a rationale for each rating.'

SUMMARY_PROMPT = "Summarize below text in follow format:\n\
C1: {GRADE}, C2: {GRADE}, C3: {GRADE}, C4: {GRADE}, ... \n\n\
(only answer in this format, no extra word, don't use word 'Grade')"
