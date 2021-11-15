from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import MetaData, Table, Column, Integer,VARCHAR,BigInteger
from sqlalchemy.orm import declarative_base
from dbconn import engineconn
from typing import Optional

import uvicorn


Base = declarative_base()
metadata = MetaData()
engine = engineconn('synthea_1000')
session = engine.sessionmaker()
connect = engine.connection()
app = FastAPI()



#---------- CLASS 선언부 ----------
# DB Class
class Person(Base):

    __tablename__ = 'person'
    person_id = Column(BigInteger,nullable=False,primary_key=True)
    gender_concept_id = Column(Integer,nullable=True)
    race_source_value = Column(VARCHAR(50),nullable=True)
    ethnicity_source_value = Column(VARCHAR(50),nullable=True)
    year_of_birth = Column(Integer,nullable=True)


    def __repr__(self):
        return "<User(person_id='%s', gender_concept_id='%s', race_source_value='%s', " \
               "ethnicity_source_value='%s', year_of_birth='%s')>" % (
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
# POST Class
class Gender(BaseModel):
    gender : str

class Race(BaseModel):
    color : str

class Ethinicity(BaseModel):
    nation : str

class Occurrence(BaseModel):
    visit : str

class Off_limit(BaseModel):
    offset: int
    limit: int

# ------------------------ CLASS ---------------------------------

@app.get('/person/all')
async def person_all():
    table = Table('person', metadata, autoload=True, autoload_with=engine.engine)
    person = session.query(table).all()
    return person

#성별
@app.post('/person/sex')
async def gender(sex : Gender):
    #8507 male 8532 female
    result = session.query(Person.gender_concept_id).filter(Person.gender_concept_id == sex.gender).count()

    return result

#인종
@app.post('/person/race')
async def race_color(race : Race):
    # white, black, asian
    result_color = session.query(Person.race_source_value).filter(Person.race_source_value == race.color).count()

    return result_color

# 민족
@app.post('/person/ethinicity')
async def ethinicity_nation(ethin : Ethinicity):
    result_nation = session.query(Person.ethnicity_source_value).filter(Person.ethnicity_source_value == ethin.nation).count()

    return result_nation

# 사망
@app.get('/person/death')
async def death():
    table = Table('death', metadata, autoload=True, autoload_with=engine.engine)
    death_person = session.query(table).count()
    return death_person

# 환자 유형 (입원, 외래, 응급)
@app.post('/person/visit')
async def visit_occurrence(occurrence : Occurrence):
#9201 02 03
    result_occurrence = session.query(Visit).filter(Visit.visit_concept_id == occurrence.visit).count()

    return result_occurrence

@app.post('/person/visitor/gender')
async def visitor(sex: Gender):
    result_visitor = session.query(Visit, Person).filter(Visit.person_id == Person.person_id,Person.gender_concept_id == sex.gender).count()

    return result_visitor

@app.post('/person/visitor/race')
async def visitor(race: Race):
    # 인종별
    result_visitor_race = session.query(Visit, Person).filter(Visit.person_id == Person.person_id,Person.race_source_value == race.color).count()

    return result_visitor_race

@app.post('/person/visitor/nation')
async def visitor(ethin : Ethinicity):
    result_visitor = session.query(Visit, Person).filter(Visit.person_id == Person.person_id,Person.ethnicity_source_value == ethin.nation).count()

    return result_visitor

@app.get('/person/age/{age}')
async def age_visitor(age: int):
    ten = age+10
    result = session.query(Visit,Person).filter(Visit.person_id == Person.person_id,age<=Person.year_of_birth,ten>=Person.year_of_birth).count()

    return result

@app.post('/concept/{search}')
async def concept(search : str, cnt :Off_limit):
    result_concept = session.query(Concept).filter(Concept.domain_id == search).offset(cnt.offset).limit(cnt.offset).all()

    return result_concept



if __name__ == '__main__':
    uvicorn.run(app)