from fastapi import FastAPI
from sqlalchemy import MetaData, Table, Column, Integer, Sequence, String,VARCHAR,BigInteger
from sqlalchemy.orm import declarative_base
from dbconn import engineconn

import uvicorn


Base = declarative_base()
metadata = MetaData()
engine = engineconn('synthea_1000')
session = engine.sessionmaker()
connect = engine.connection()
app = FastAPI()

#---------- CLASS 선언부 ----------
# Person Class
class Person(Base):

    __tablename__ = 'person'
    person_id = Column(BigInteger,nullable=False,primary_key=True)
    gender_concept_id = Column(Integer,nullable=True)
    race_source_value = Column(VARCHAR(50),nullable=True)
    ethnicity_source_value = Column(VARCHAR(50),nullable=True)
    year_of_birth = Column(Integer,nullable=True)


    def __repr__(self):
        return "<User(person_id='%s', gender_concept_id='%s', race_source_value='%s', ethnicity_source_value='%s', year_of_birth='%s')>" % (
            self.person_id,self.gender_concept_id, self.race_source_value, self.ethnicity_source_value, self.year_of_birth)

class Visit(Base):

    __tablename__ = 'visit_occurrence'
    visit_occurrence_id = Column(BigInteger,nullable=False,primary_key=True)
    person_id = Column(BigInteger,nullable=True)
    visit_concept_id = Column(Integer,nullable=True)


    def __repr__(self):
        return "<User(visit_occurrence_id='%s', person_id='%s', visit_concept_id='%s')>" % (
            self.visit_occurrence_id,self.person_id, self.visit_concept_id)

class Concept(Base):

    __tablename__ = 'concept'
    concept_id = Column(BigInteger,nullable=False,primary_key=True)
    concept_name = Column(VARCHAR(255),nullable=True)
    domain_id = Column(VARCHAR(20),nullable=True)

    def __repr__(self):
        return "<User(concept_id='%s', concept_name='%s', domain_id='%s')>" % (
            self.concept_id,self.concept_name, self.domain_id)

# ------------------------ CLASS ---------------------------------

@app.get('/person/all')
async def person_all():
    table = Table('person', metadata, autoload=True, autoload_with=engine.engine)
    person = session.query(table).all()
    return person

#성별
@app.get('/person/sex/{gender}')
async def gender(gender : str):

    if gender == 'm':
        result = session.query(Person.gender_concept_id).filter(Person.gender_concept_id == "8507").count()

    elif gender == 'f':
        result = session.query(Person.gender_concept_id).filter(Person.gender_concept_id == "8532").count()

    return result

#인종
@app.get('/person/race/{color}')
async def race_color(color : str):
    if color == 'white':
        result_color = session.query(Person.race_source_value).filter(Person.race_source_value == "white").count()

    elif color == 'asian':
        result_color = session.query(Person.race_source_value).filter(Person.race_source_value == "asian").count()

    elif color == 'black':
        result_color = session.query(Person.race_source_value).filter(Person.race_source_value == "black").count()

    return result_color

# 민족
@app.get('/person/ethinicity/{nation}')
async def ethinicity_nation(nation : str):

    if nation == 'hispanic':
        result_nation = session.query(Person.ethnicity_source_value).filter(
            Person.ethnicity_source_value == "hispanic").count()

    elif nation == 'nonhispanic':
        result_nation = session.query(Person.ethnicity_source_value).filter(
            Person.ethnicity_source_value == "nonhispanic").count()

    return result_nation

# 사망
@app.get('/person/death')
async def death():
    table = Table('death', metadata, autoload=True, autoload_with=engine.engine)
    death_person = session.query(table).count()
    return death_person

# 환자 유형 (입원, 외래, 응급)
@app.get('/person/occurrence/{occurrence}')
async def visit_occurrence(occurrence : str):

    if occurrence == 'inpatient':
        result_occurrence = session.query(Visit.visit_concept_id).filter(Visit.visit_concept_id == "9201").count()

    elif occurrence == 'outpatient':
        result_occurrence = session.query(Visit.visit_concept_id).filter(Visit.visit_concept_id == "9202").count()

    elif occurrence == 'emergency':
        result_occurrence = session.query(Visit.visit_concept_id).filter(Visit.visit_concept_id == "9203").count()

    return result_occurrence

@app.get('/person/visitor/{visitor}')
async def visitor(visitor: str):

    # 성별 방문자 수
    if visitor == 'male':
        result_visitor = session.query(Visit,Person).filter(Visit.person_id == Person.person_id).filter(
            Person.gender_concept_id == '8507').count()

    elif visitor == 'female':
        result_visitor = session.query(Visit, Person).filter(Visit.person_id == Person.person_id).filter(
            Person.gender_concept_id == '8532').count()

    # 인종별
    elif visitor == 'white':
        result_visitor = session.query(Visit, Person).filter(Visit.person_id == Person.person_id).filter(
            Person.race_source_value == 'white').count()

    elif visitor == 'asian':
        result_visitor = session.query(Visit, Person).filter(Visit.person_id == Person.person_id).filter(
            Person.race_source_value == 'asian').count()

    elif visitor == 'balck':
        result_visitor = session.query(Visit, Person).filter(Visit.person_id == Person.person_id).filter(
            Person.race_source_value == 'balck').count()

    # 민족별
    elif visitor == 'hispanic':
        result_visitor = session.query(Visit, Person).filter(Visit.person_id == Person.person_id).filter(
            Person.ethnicity_source_value == 'hispanic').count()

    elif visitor == 'nonhispanic':
        result_visitor = session.query(Visit, Person).filter(Visit.person_id == Person.person_id).filter(
            Person.ethnicity_source_value == 'nonhispanic').count()

    return result_visitor

@app.get('/person/age/{age}')
async def age_visitor(age: int):
    ten = age+10
    result = session.query(Visit,Person).filter(Visit.person_id == Person.person_id).filter(age<=Person.year_of_birth).filter(ten>=Person.year_of_birth).count()

    return result

@app.get('/concept')
async def concept():
    # table = Table('concept', metadata, autoload=True, autoload_with=engine.engine)
    # death_person = session.query(table)
    return

@app.get("/")
async def main():
    main = "fastapi 메인페이지 입니다."
    return main


if __name__ == '__main__':
    uvicorn.run(app)