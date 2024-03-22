# fastapi_neon/main.py
from typing import Optional
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel, create_engine, Session
from pydantic import BaseModel

db_url = 'postgresql://ToDoApp_owner:GtjNO8uyxwv5@ep-divine-cell-a5w6ewc5.us-east-2.aws.neon.tech/ToDoApp?sslmode=require'

class ToDos(SQLModel, table = True):  # making the table in Neon
    id: Optional[int] = Field(default=None, primary_key=True)
    content : str
    is_complete: bool = Field(default = False)

class User_Data(BaseModel):
    content : str = Field(nullable = False)
    is_complete: bool = False

engine = create_engine(db_url, echo = True) # echo true to see database query run on terminal

def create_table():  # funciton to create table in sql database
   SQLModel.metadata.create_all(engine)


def insert_table_data(content:str):  
    with Session(engine) as session:   #used to automatically close the session within body to avoid forgeting close 
        data:ToDos = ToDos(content = content)
        session.add(data)
        session.commit()
        session.close()  # no need to close session inside with


app = FastAPI(title="Hello World API", 
    version="0.0.1",
    servers=[
        {
            "url": "http://0.0.0.0:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ToDos")
def add_todos_route(user_todos:User_Data):
    if user_todos.content.strip():
        insert_table_data(user_todos.content)
        return {"Message": "ToDos added successfully"}
    else:
        raise HTTPException(status_code = 404, detail = "no todos found")