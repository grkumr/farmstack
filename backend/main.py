from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import Todo



app = FastAPI()

from database import(
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)


origins = ['http://localhost:3000',]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods =  ["*"],
    allow_headers = ["*"],
)

@app.get("/")
def read_root():
    return {"PING"}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo{title}", response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"NO TO ITEM WITH THIS TITLE {title}")

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.__dict__)
    if response:
        return response
    raise HTTPException(400, "SOMETHING WENT WRONG")

@app.put("/api/todo{title}", response_model=Todo)
async def put_todo(title, desc):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"NO TO ITEM WITH THIS TITLE {title}")


@app.delete("/api/todo{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "SUCCESSFULLY DELETED TODO ITEM"
    raise HTTPException(404, f"NO TO ITEM WITH THIS TITLE {title}")
 
