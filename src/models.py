from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    character_fav: Mapped[List["Characters"]] = relationship(back_populates="Favorite_Character")
    planet_fav: Mapped[List["Planets"]] = relationship(back_populates="Favorite_Planet")
    characters: Mapped[List["Favorite_Character"]] = relationship(back_populates="characters")
    planets: Mapped[List["Favorite_Planet"]] = relationship(back_populates="planets")
    fav_planet_id: Mapped[int] = mapped_column(ForeignKey("Favorite_Planet.id"))
    fav_character_id: Mapped[int] = mapped_column(ForeignKey("Favorite_Character.id"))

    # author: Mapped[List["Post"]] = relationship(back_populates="author")
    # likes: Mapped[List["Like"]] = relationship(back_populates="like_author")
    # comments: Mapped[List["Comment"]] = relationship(back_populates="comment_author")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    char_image: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String(555))
    home_planet: Mapped[str]= mapped_column(String(50))
    characters: Mapped[List["Favorite_Character"]] = relationship(back_populates="characters")
    planets: Mapped[List["Favorite_Planet"]] = relationship(back_populates="planets")

    # user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # author: Mapped["User"] = relationship(back_populates="posts")
    # likes: Mapped[List["Like"]] = relationship()
    # comments: Mapped[List["Comment"]] = relationship(back_populates="commented_on")
    # media: Mapped["Media"] = relationship(back_populates="media_url")

class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    terrain: Mapped[str] = mapped_column(String(500))
    planet_image: Mapped[str] = mapped_column(String(500))
    population: Mapped[int] = mapped_column()
    favorite_planet: Mapped[bool] = mapped_column()

    # comment_author: Mapped["User"] = relationship(back_populates="comments")
    # user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    # commented_on: Mapped["Post"] = relationship(back_populates="comments")

class Favorite_Character(db.Model):
    __tablename__ = "Favorite_Character"
    id: Mapped[int] = mapped_column(primary_key=True)
    characters_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    character_fav: Mapped[List["Characters"]] = relationship(back_populates="Favorite_Character")

class Favorite_Planet(db.Model):
    __tablename__ = "Favorite_Planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    planets_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    planet_fav: Mapped[List["Planets"]] = relationship(back_populates="Favorite_Planet")

    # post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    # user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # single_post: Mapped["Post"] = relationship(back_populates="likes")
    # like_author: Mapped["Post"] = relationship(back_populates="likes")

# class Media(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     type: Mapped[str] = mapped_column(String(120), nullable = False)
#     media_url: Mapped[str] = mapped_column(String(500))
#     post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

