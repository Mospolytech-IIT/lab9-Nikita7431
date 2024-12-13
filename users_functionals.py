from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_my import  User, Post  

engine = create_engine("mysql+mysqlconnector://root:12345@localhost/db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def add_users():
    users = [
        User(username="Nikita", email="nik@example.com", password="password123"),
        User(username="Maks", email="mak@e.com", password="secure456"),
        User(username="Alyona", email="a@e.com", password="pass789")
    ]
    session.add_all(users)
    session.commit()
    print("Пользователи добавлены.")

def add_posts():
    posts = [
        Post(title="Первый пост", content="Это содержимое первого поста.", user_id=1),
        Post(title="Второй пост", content="Это содержимое второго поста.", user_id=2),
        Post(title="Третий пост", content="Это содержимое третьего поста.", user_id=1)
    ]
    session.add_all(posts)
    session.commit()
    print("Посты добавлены.")


def get_all_users():
    users = session.query(User).all()
    for user in users:
        print(user.id, user.username, user.email)

def get_all_posts_with_users():
    posts = session.query(Post).all()
    for post in posts:
        print(post.id, post.title, post.author.username)

def get_posts_by_user(username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        for post in user.posts:
            print(post.id, post.title)
    else:
        print(f"Пользователь {username} не найден.")


def update_user_email(user_id, new_email):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.email = new_email
        session.commit()
        print("Email обновлен.")
    else:
        print("Пользователь не найден.")

def update_post_content(post_id, new_content):
    post = session.query(Post).filter_by(id=post_id).first()
    if post:
        post.content = new_content
        session.commit()
        print("Содержимое поста обновлено.")
    else:
        print("Пост не найден.")


def delete_post(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    if post:
        session.delete(post)
        session.commit()
        print("Пост удален.")
    else:
        print("Пост не найден.")

def delete_user_and_posts(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.query(Post).filter_by(user_id=user_id).delete()
        session.delete(user)
        session.commit()
        print("Пользователь и все его посты удалены.")
    else:
        print("Пользователь не найден.")

# if __name__ == "__main__":
#     add_users()
#     add_posts()
#     print("\nВсе пользователи:")
#     get_all_users()
#     print("\nВсе посты с информацией о пользователях:")
#     get_all_posts_with_users()
#     print("\nПосты, созданные пользователем Nikita:")
#     get_posts_by_user("Nikita")
#     print("\nОбновление email пользователя с ID=1:")
#     update_user_email(1, "nik@example.com")
#     print("\nОбновление содержимого поста с ID=1:")
#     update_post_content(1, "Обновленное содержимое первого поста.")
#     print("\nУдаление поста с ID=2:")
#     delete_post(2)
#     print("\nУдаление пользователя с ID=1 и всех его постов:")
#     delete_user_and_posts(1)
