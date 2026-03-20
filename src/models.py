from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import List

db = SQLAlchemy()

# # Association table for user favorite characters
# user_favorite_characters = Table(
#     "user_favorite_characters",
#     db.metadata,
#     Column("user_id", ForeignKey("user.id"), primary_key=True),
#     Column("character_id", ForeignKey("characters.id"), primary_key=True),
# )

# # (Optional) Association table for user favorite planets if you need many-to-many too
# user_favorite_planets = Table(
#     "user_favorite_planets",
#     db.metadata,
#     Column("user_id", ForeignKey("user.id"), primary_key=True),
#     Column("planet_id", ForeignKey("planets.id"), primary_key=True),
# )

class User(db.Model):
    __tablename__ = "user"
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

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    char_image: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String(555))
    home_planet: Mapped[str]= mapped_column(String(50))
    characters: Mapped[List["Favorite_Character"]] = relationship(back_populates="characters")
    planets: Mapped[List["Favorite_Planet"]] = relationship(back_populates="planets")


class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    terrain: Mapped[str] = mapped_column(String(500))
    planet_image: Mapped[str] = mapped_column(String(500))
    population: Mapped[int] = mapped_column()
    favorite_planet: Mapped[bool] = mapped_column()

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


# class Base(DeclarativeBase):
#     pass
# # note for a Core table, we use the sqlalchemy.Column construct,
# # not sqlalchemy.orm.mapped_column
# association_table = Table(
#     "association_table_one",
#     Base.metadata,
#     Column("user_id", ForeignKey("User.id")),
#     Column("char_fav_id", ForeignKey("Favorite_Charater.id")),
# )

# class Parent(Base):
#     __tablename__ = "User"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     children: Mapped[List[Characters]] = relationship(secondary=association_table)

# class Child(Base):
#     __tablename__ = "char_fav_id"

#     id: Mapped[int] = mapped_column(primary_key=True)
