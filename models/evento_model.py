from config import conexion
from sqlalchemy import Column, types,ForeignKey

class EventoModel(conexion.Model):
    id = Column(type_=types.Integer,primary_key= True, autoincrement=True)
    descripcion = Column(type_=types.Text, nullable=False)
    fotoEvento = Column(type_=types.Text, name= 'foto_evento',nullable=False) #verificar
    paginaWeb = Column(type_=types.Text, name='pagina_web')
    usuarioId = Column(ForeignKey(column='usuarios.id'),type_=types.Integer, nullable=False, name='usuario_id')

    __tablename__ = "eventos"