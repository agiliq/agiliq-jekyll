---
layout: post
comments: true
title:  "Getting started with FastAPI by re building the Django Polls Tutorial"
description: ""
keywords: "FastAPI, Python, SQLAlchemy, Pydantic"
date: 2020-05-14
categories: [FastAPI, Python, SQLAlchemy, Pydantic]
author: Manjunath Hugar
---

In this blog post we are going to rebuild Django Polls tutorial API using FastAPI.

### What is FastAPI?
FastAPI is a web framework for building APIs. As per its official page, `FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

It is easy to learn, fast and said to be high performance, on par with `NodeJS` and `Go`.`

### Installation
Open your terminal and run
```
pip install fastapi
```

also need to install ASGI server
```
pip install uvicorn
```

thats all, now lets quicky create some endpoints, create a file `main.py` and add the following
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome to the world of FastAPI!"}

@app.get("/items/{item}")
def read_item(item: str, q: str = None):
    return {"item": item, "q": q}
```

now run the server 
```
uvicorn main:app
```
open your browser and visit `http://127.0.0.1:8000/`
you should see the following response:
```json
{"message":"Welcome to the world of FastAPI!"}
```
visit `http://127.0.0.1:8000/items/apple?q=delicious`
you should see the below response:
```json
{"item":"apple","q":"delicious"}
```
that's great, we have already created an API having two endpoints:

- `http://127.0.0.1:8000/` doesn't take any parameters and it simply returns a JSON response.
- `http://127.0.0.1:8000/items/{item}"`takes a parameter `item` of type `str` and optional `str` query parameter `q`. 

another good feature of FastAPI is that it provides an interactive API documentation, simply visit `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`.

Now let's go ahead and rebuild our polls tutorial API.
The endpoints we created above are static, they don't interact with the database. In the next section you will learn how we can use [SQLAlchemy](https://www.sqlalchemy.org/) for ORM and [Pydantic](https://pydantic-docs.helpmanual.io/) to create models/schemas to make our APIs dynamic.

This post assumes that you're familiar with `SQLAlchemy`, you can refer this [docs](https://www.sqlalchemy.org/) for more details.

We will create the following endpoints
 - An API to create poll question
 - API to list all poll questions
 - API to get question detail
 - API to edit poll question
 - API to delete poll question
 - API to create choice for a particular poll question
 - API to update votes for a particular question
 
Our project structure would look like this
```json
└───pollsapi
   │--- crud.py
   │--- database.py
   │--- main.py
   │--- models.py
   │--- schemas.py
```

Now let's add the following code to `pollsapi/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/DATABASE_NAME"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

after that, add the following code to `pollsapi/models.py`
```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Question(Base):
	__tablename__ = "question"
	id = Column(Integer, primary_key=True)
	question_text = Column(String)
	pub_date = Column(DateTime)

	choices = relationship('Choice', back_populates="question")


class Choice(Base):
	__tablename__ = "choice"
	id = Column(Integer, primary_key=True)
	question_id = Column(Integer, ForeignKey('question.id'))
	choice_text = Column(String())
	votes = Column(Integer, default=0)

	question = relationship("Question", back_populates="choices")
```

we have created `relationship` provided by SQLAlchemy ORM, with this we can simply access attribute like `question.choices` to get all the choices for that particular question. Similarly the we can refer `choice.question` to get question object related to that choice.

Ok, so far so good, we will now create schemas using the `pydantic` library.
Go ahead and add the following code to `pollsapi/schemas.py`
```python
from datetime import datetime

from pydantic import BaseModel
from typing import List


# Choice schema

class ChoiceBase(BaseModel):
	choice_text: str
	votes: int = 0

class ChoiceCreate(ChoiceBase):
	pass

class ChoiceList(ChoiceBase):
	id: int

	class Config:
		orm_mode = True


# Question schema

class QuestionBase(BaseModel):
	question_text: str
	pub_date: datetime

class QuestionCreate(QuestionBase):
	pass

class Question(QuestionBase):
	id: int

	class Config:
		orm_mode = True

class QuestionInfo(Question):
	choices: List[ChoiceList] = []
```

defining attributes in SQLAlchemy is different as compared with Pydantic, in SQLAlchemy arributes are defined using `=` and the type is passed as a parameter to `Column` like this
```
question_text = Column(String)
```
whereas the Pydantic style declares the type using `:` like this
```
question_text: str
```

Pyndatic models/schemas will be mapped to the incoming data (request data in POST, PUT) and to the response data returned from the API.

We have created base classes `QuestionBase` and `ChoiceBase` that extends pydantic `BaseModel` to hold attributes which are common for creating or reading data and created other classes that inherit from these base classes, the reason being we want specific attributes for creation and reading.

like for example - for creating a choice we need `choice_text` and `votes` (if not passed, it defaults to **0**)  so we will use `ChoiceCreate` and for reading the choice, we want to return `id`, `choice_text` and `votes` and in this case we will use `ChoiceList`.

Another important thing to understand is the use of `orm_mode = True`, notice we have added a `class Config` and have set `orm_mode = True`, this is because by default Pydantic model could read the data from `dict` and it can't read the data if the data is an ORM model so with the `orm_mode = True` added to our class, Pydantic model can also read the data from the object something like `data.question_text`.

Ok, we will now create `pollsapi/crud.py` which will contain all the functions to perform CRUD (**C**reate, **R**etrieve, **U**pdate and **D**elete) operations.

Add the following code to `pollsapi/crud.py`
```python
from sqlalchemy.orm import Session

from models import Base, Question, Choice
import schema

# Question

def create_question(db: Session, question: schema.QuestionCreate):
	obj = Question(**question.dict())
	db.add(obj)
	db.commit()
	return obj

def get_all_questions(db: Session):
	return db.query(Question).all()

def get_question(db:Session, qid):
	return db.query(Question).filter(Question.id == qid).first()

def edit_question(db: Session, qid, question: schema.QuestionInfo):
	obj = db.query(Question).filter(Question.id == qid).first()
	obj.question_text = question.question_text
	obj.pub_date = question.pub_date
	db.commit()
	return obj

def delete_question(db: Session, qid):
	db.query(Question).filter(Question.id == qid).delete()
	db.commit()

# Choice

def create_choice(db:Session, qid: int, choice: schema.ChoiceCreate):
	obj = Choice(**choice.dict(), question_id=qid)
	db.add(obj)
	db.commit()
	return obj

def update_vote(choice_id: int, db:Session):
	obj = db.query(Choice).filter(Choice.id == choice_id).first()
	obj.votes += 1
	db.commit()
	return obj
```

we have created all the utility functions which will be used in API functions.

Now comes the real file `pollsapi/main.py`, which will make use of all the files we created above.

### Create a poll question
Add the following lines to `pollsapi/main.py`
```python
from fastapi import FastAPI, HTTPException, Response, Depends
import schema
from typing import List

from sqlalchemy.orm import Session

import crud
from database import SessionLocal, engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


## Question

@app.post("/questions/", response_model=schema.QuestionInfo)
def create_question(question: schema.QuestionCreate, db: Session = Depends(get_db)):
	return crud.create_question(db=db, question=question)
```

- This line `Base.metadata.create_all(bind=engine)` creates database tables by using the SQLAlchemy models we defined in `pollsapi/models.py`.
- function `create_question`is decorated using the `app` object created above which is an instance of `FastAPI`, it takes two arguments `path` and `response_model`. `response_model` returns the schema `QuestionInfo` so the endpoint will return the fields `id`, `question_text` and `pub_date`.`
- We have created a function `create_question`, first argument receives the request data and maps it to the schema `QuestionCreate` which has the fields `question_text` and `pub_date` and the second argument creates a session/request and then it gets closed after the request is completed.

now visit `http://127.0.0.1:8000/docs` and you should see section to POST `/questions/` something like this

![](/assets/images/fastapi/fastapidocs.png) 

click on that section and it will expand, now click on `Try it out` to test your API. 

### List all poll questions
We will now create an endpoint to get all our poll questions, for this we will use `@app.get`, add another function in `pollsapi/main.py`
```python
@app.get("/questions/", response_model=List[schema.Question])
def get_questions(db: Session = Depends(get_db)):
	return crud.get_all_questions(db=db)
```
notice the use of `List` in `response_model`, `crud.get_all_questions` returns a list of objects and not just an object so we should let our framework know that. Try removing the `List` and our application will throw an error.

at this point when you visit `http://127.0.0.1:8000/docs`, you should see two sections - `POST /questions/` and `GET /questions/`, click on GET section and Try it out and you should a response something like below
```json
[
  {
    "question_text": "What is fastAPI?",
    "pub_date": "2020-05-14T12:58:05.043000",
    "id": 1
  }
]
```
### Retrieve, Edit and Delete a poll question
```python
@app.get("/questions/{qid}", response_model=schema.QuestionInfo)
def get_question(qid: int, db: Session = Depends(get_db)):
	q = crud.get_question(db=db, qid=qid)
	if not q:
		raise HTTPException(status_code=404, detail="Question not found")
	return crud.get_question(db=db, qid=qid)

@app.put("/questions/{qid}", response_model=schema.QuestionInfo)
def edit_question(qid: int, question: schema.QuestionCreate, db: Session = Depends(get_db)):
	q = crud.get_question(db=db, qid=qid)
	if not q:
		raise HTTPException(status_code=404, detail="Question not found")
	obj = crud.edit_question(db=db, qid=qid, question=question)
	return obj

@app.delete("/questions/{qid}", response_model=schema.QuestionInfo)
def delete_question(qid: int, db: Session = Depends(get_db)):
	q = crud.get_question(db=db, qid=qid)
	if not q:
		raise HTTPException(status_code=404, detail="Question not found")
	crud.delete_question(db=db, qid=qid)
	return q
```
We have used different response_model for `get_questions` and `get_question`, this is because we wanted to show `choices` in the API response only in case of Question detail API and not for Question list API.

### API to create choice for a particular poll question
```python
@app.post("/questions/{qid}/choice", response_model=schema.ChoiceList)
def create_choice(qid: int, choice: schema.ChoiceCreate, db: Session = Depends(get_db)):
	question = crud.get_question(db=db, qid=qid)
	if not question:
		raise HTTPException(status_code=404, detail="Question not found")
	return crud.create_choice(db=db, qid=qid, choice=choice)
```

and finally 
### API to update votes for a particular question
```python
@app.put("/choices/{choice_id}/vote", response_model=schema.ChoiceList)
def update_vote(choice_id: int, db: Session = Depends(get_db)):
	return crud.update_vote(choice_id=choice_id, db=db)
```

the following are the endpoints for Question and Choice
- Create question - `POST http://127.0.0.1:8000/questions/`
- List all questions - `GET http://127.0.0.1:8000/questions/`
- Retrieve a particular question - `GET http://127.0.0.1:8000/questions/{qid}`
- Edit a particular question - `PUT http://127.0.0.1:8000/questions/{qid}`
- Delete a particular question - `DELETE http://127.0.0.1:8000/questions/{qid}`
- Create choice for a particular poll question - `POST http://127.0.0.1:8000/questions/{qid}/choice`
- Update votes for a particular question - `PUT http://127.0.0.1:8000/choices/{choice_id}/vote`

You can find a source code [here](https://github.com/manjunath24/Polls-API)
