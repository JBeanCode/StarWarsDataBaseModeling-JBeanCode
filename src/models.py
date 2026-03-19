from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    author: Mapped[List["Post"]] = relationship(back_populates="author")
    likes: Mapped[List["Like"]] = relationship(back_populates="like_author")
    comments: Mapped[List["Comment"]] = relationship(back_populates="comment_author")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(555))
    image: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    likes: Mapped[List["Like"]] = relationship()
    comments: Mapped[List["Comment"]] = relationship(back_populates="commented_on")
    media: Mapped["Media"] = relationship(back_populates="media_url")

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500))
    comment_author: Mapped["User"] = relationship(back_populates="comments")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    commented_on: Mapped["Post"] = relationship(back_populates="comments")

class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    single_post: Mapped["Post"] = relationship(back_populates="likes")
    like_author: Mapped["Post"] = relationship(back_populates="likes")

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    media_url: Mapped[str] = mapped_column()
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

