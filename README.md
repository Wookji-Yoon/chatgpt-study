# config.py

- api를 요청하기 위한 prompt를 configuration할 수 있는 파일

# main.py

- 전체 후보자(84명)/전체문항에 대한 chatGPT 채점 결과를 json, csv 파일로 저장하는 코드
- 반복해서 실행할 수 있음 (default: 3회)

# test_rand_5.py

- 테스트용 코드
- 랜덤으로 5명 후보자/전체문항에 대한 chatGPT 채점 결과를 json, csv 파일로 저장하는 코드

# result

- python 코드 시행결과가 저장되는 directory

# prompt

- prompt를 text 파일로 저장한 directory

---

## 아래는 참고

# raw_data

- 자기소개서 원본, 평가표, 평가결과 등의 원본 data

# src

- raw_data를 코드에 사용하기 위해 가공해 놓은 data

# util.py

- 코드 정리용
