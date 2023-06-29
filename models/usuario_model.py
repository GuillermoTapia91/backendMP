from config import conexion
from sqlalchemy import Column, types
from enum import Enum

class TipoUsuario(Enum):
    ADMINISTRADOR = 'ADMINISTRADOR'
    ESPECTADOR = 'ESPECTADOR'
    EMPRESARIO = 'EMPRESARIO'

class UsuarioModel(conexion.Model):
    id = Column(type_=types.Integer,primary_key= True, autoincrement=True)
    nombre = Column(type_=types.Text, nullable=False)
    apellido = Column(type_=types.Text, nullable=False)
    tipoUsuario = Column(type_=types.Enum(TipoUsuario),nullable=False , name= 'tipo_usuario')
    correo = Column(type_=types.Text,unique=True, nullable=False)
    password = Column(type_=types.Text, nullable=False)
    fechaNacimiento = Column(type_=types.Date, nullable=False, name= 'fecha_nacimiento')

    __tablename__ = "usuarios"
