from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uvicorn


engine = create_engine("mysql+mysqlconnector://root:12345@localhost/db", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="posts")


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_users(request: Request, db: SessionLocal = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.post("/users/create")
def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: SessionLocal = Depends(get_db),
):
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.get("/users/edit/{user_id}")
def edit_user(user_id: int, request: Request, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})


@app.post("/users/update/{user_id}")
def update_user(
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    db: SessionLocal = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.email = email
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.get("/users/delete/{user_id}")
def delete_user(user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.get("/posts")
def read_posts(request: Request, db: SessionLocal = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})


@app.post("/posts/create")
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: SessionLocal = Depends(get_db),
):
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    return RedirectResponse("/posts", status_code=303)


@app.get("/posts/edit/{post_id}")
def edit_post(post_id: int, request: Request, db: SessionLocal = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    users = db.query(User).all()
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post, "users": users})


@app.post("/posts/update/{post_id}")
def update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: SessionLocal = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = title
    post.content = content
    post.user_id = user_id
    db.commit()
    return RedirectResponse("/posts", status_code=303)


@app.get("/posts/delete/{post_id}")
def delete_post(post_id: int, db: SessionLocal = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return RedirectResponse("/posts", status_code=303)

if __name__ == "__main__":
    uvicorn.run("web:app", host="127.0.0.1", port=8009, reload=True)