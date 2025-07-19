from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


# Model to define the structure of a Todo item
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False


# Temporary storage simulating a database
todos_db = []


# Create operation - Add a new Todo item
@app.post("/todos/", response_model=TodoItem)
def create_todo_item(todo: TodoItem):
    todos_db.append(todo)
    return todo


# Read operation - Get all Todo items
@app.get("/todos/", response_model=List[TodoItem])
def read_todo_items():
    return todos_db


# Read operation - Get a single Todo item by ID
@app.get("/todos/{todo_id}", response_model=TodoItem)
def read_todo_item(todo_id: int):
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo item not found")


# Update operation - Update a Todo item by ID
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo_item(todo_id: int, todo: TodoItem):
    for index, existing_todo in enumerate(todos_db):
        if existing_todo.id == todo_id:
            todos_db[index] = todo
            return todo
    raise HTTPException(status_code=404, detail="Todo item not found")


# Delete operation - Delete a Todo item by ID
@app.delete("/todos/{todo_id}", response_model=TodoItem)
def delete_todo_item(todo_id: int):
    for index, todo in enumerate(todos_db):
        if todo.id == todo_id:
            deleted_todo = todos_db.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail="Todo item not found")