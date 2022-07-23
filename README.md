# Pratice API

### API 연결 법

##### 1. db_auth.py 파일 생성 후 아래와 같은 형식의 코드 입력

>
>
>app =
>{
>
>        'name' : '데이터베이스(mysql, postgresql)',
>        
>        'user' : '유저이름',
>        
>        'password': '비밀번호',
>        
>        'host': '주소',
>        
>        'db': '데이터베이스 이름',
>       
>        'port': '포트'}



### 2. 파일을 내려받는다.

### 3. rest_api를 실행 시킨다.(localhost 기준)

### 4. 127.0.0.1:8000/docs or insomnia를 이용해 API를 호출한다.(insomnia.json 참조)

1.  GET 127.0.0.1:8000/person/all => 전체 수 호출




2.  POST 127.0.0.1:8000/person/gender => 성별에 따라 호출
      
      body = { "gender":"8507" male 또는 "gender":"8532" female}
    
    
    
3.  POST 127.0.0.1:8000/person/race => 인종에 따라 호출 
      
      body = { "color":"black" 또는 "color":"white" 또는 "color":"asian"}
    
    
    
4.  POST 127.0.0.1:8000/person/ethinicity => 민족에 따라 호출 
      
      body = { "nation":"hispanic" 또는 "nation":"nonhispanic"}



5.  GET 127.0.0.1:8000/person/death => 사망 수 호출




6.  POST 127.0.0.1:8000/person/visit => 유형에 따라 호출
      
      body = { "visit":"9201" 또는 "visit":"9202" 또는 "visit":"9203"}
    
    
    
7.  POST 127.0.0.1:8000/person/visit/gender => 성별에 따라 방문 수 호출
      
      body = { "gender":"8507" male 또는 "gender":"8532" female}
      
      
      
8.  POST 127.0.0.1:8000/person/visit/race => 인종에 따라 방문 수 호출
      
      body = { "color":"black" 또는 "color":"white" 또는 "color":"asian"}
      
      
      
9.  POST 127.0.0.1:8000/person/visit/nation => 민족에 따라 방문 수 호출
      
      body = { "nation":"hispanic" 또는 "nation":"nonhispanic"}



10. GET  127.0.0.1:8000/person/age/{age} => 태어난 년도(10년 기준) 따라 방문 수 호출
      
      Ex:) {age} =>1990 => 1990 ~ 2000년 , 1900 => 1900 ~ 1910년
      
      
      
11. POST 127.0.0.1:8000/concept/{search} => concept_id 호출, offset/limit를 이용해 Pagination 구현
      
      Ex:) {search} => Drug, Condition, Visit, Observation
      body = { "offset":"숫자","offset":"숫자"}
      
      
      
12. POST 127.0.0.1:8000/row/{table} => 각 테이블 row 호출, 특정 키워드 검색 기능은 추가 예정

      EX:) {table} => Drug, Condition, Visit, Person
      body = { "offset":"숫자","offset":"숫자"}





## 추가 예정 

### 특정 키워드 검색 기능

현재 테이블 별로 데이터 불러오는 것 까진 구현 완료 
여기에 조금 더 추가를 해서 유저들이 직접 컬럼 속 데이터를 집어넣어 요청했을 때 동작하는 기능을 만들어야됨 

각 테이블의 column들이 모두 다 다르기 때문에 일일히 하나씩 
분기점을 나누기에는 리소스가 너무 많이 소모됨 그래서 생각한 방법

파라미터(?example=0&data=0)를 이용해서 구현하려고 했으나 아직 파라미터를 이용해 
데이터를 호출하는 것 까진 구현을 해보지 못함

파라미터로 데이터 값을 직접 집어 넣어 처리를 할 때 만약 쿼리에서 해당 테이블이 아닌 내용이 들어왔을 경우 
다시 입력하도록 리턴 해주고 정상적인 데이터가 들어와 작동을 한다면 처리된 결과값을 리턴해 주는 코드를 만들 예정
