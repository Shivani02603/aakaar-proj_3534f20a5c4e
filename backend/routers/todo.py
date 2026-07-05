from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from database.config import get_db
from database.models import Todo, User
from backend.schemas import TodoCreate, TodoResponse
from backend.routers.auth import get_current_user

router = APIRouter(tags=["Todo"])

@router.get("/todos", response_model=List[TodoResponse])
def get_todos(
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = db.query(Todo).filter(Todo.user_id == user.id)
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    return query.all()

@router.post("/todos", status_code=201, response_model=TodoResponse)
def create_todo(
    data: TodoCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    new_todo = Todo(**data.model_dump(), user_id=user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/todos/{id}", response_model=TodoResponse)
def get_todo(
    id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/todos/{id}", response_model=TodoResponse)
def update_todo(
    id: str,
    data: TodoCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in data.model_dump().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/todos/{id}")
def delete_todo(
    id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"status": "deleted"}

@router.patch("/todos/{id}")
def patch_todo(
    id: str,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if completed is None:
        raise HTTPException(status_code=400, detail="Missing 'completed' field")
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = completed
    db.commit()
    db.refresh(todo)
    return todo