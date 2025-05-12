from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):

    __tablename__='users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str]=mapped_column(unique=True, nullable =False)
    lastname:Mapped[str]=mapped_column(unique=True, nullable =False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String,nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

   

    favoritos:Mapped[list["Favoritos"]] = relationship(back_populates="user")
   
    def serialize(self):

        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "favoritos":[favorito.id for favorito in self.favoritos] if self.favoritos else []
        }


class Favoritos(db.Model):

    __tablename__='favoritos'
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
    people_id:Mapped[int]=mapped_column(ForeignKey('peoples.id'))
    planeta_id:Mapped[int]=mapped_column(ForeignKey('planetas.id'))
   
    user:Mapped["User"]=relationship(back_populates="favoritos")
    people:Mapped["People"]=relationship(back_populates="favoritos")
    planeta:Mapped["Planeta"]=relationship(back_populates="favoritos")

    def serialize(self):
        return {
            "user_id": self.user_id,
            "people_id":self.people_id,
            "planeta_id":self.planeta_id
            
        }
    



class People(db.Model):
   
   __tablename__='peoples'
   id:Mapped[int]=mapped_column(primary_key=True)
   name: Mapped[str] = mapped_column(String(100))
   raza: Mapped[str] = mapped_column(String(100))

   favoritos: Mapped[list["Favoritos"]] = relationship(back_populates="people")


def serialize(self):
        return {
           "id": self.id,
           "name": self.name,
                 
        }

class Planeta(db.Model):
   
   __tablename__='planetas'
   id:Mapped[int]=mapped_column(primary_key=True)
   name: Mapped[str] = mapped_column(String(100))
   size: Mapped[int]=mapped_column(nullable =False)

   favoritos: Mapped[list["Favoritos"]] = relationship(back_populates="planeta")


def serialize(self):
        return {
           "id": self.id,
           "name": self.name,
           "size":self.size
                 
        }