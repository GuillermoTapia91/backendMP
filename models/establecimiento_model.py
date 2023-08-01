from config import conexion
from sqlalchemy import Column, types, ForeignKey
from enum import Enum


class TipoEstablecimiento(Enum):
    DISCOTECA = 'DISCOTECA'
    BAR = 'BAR'
    

class EstablecimientoModel(conexion.Model):
    id = Column(type_=types.Integer,primary_key= True, autoincrement=True)
    tipoEstablecimiento = Column(type_=types.Enum(TipoEstablecimiento), nullable=False, name='tipo_establecimiento')
    nombre = Column(type_=types.Text, nullable=False)
    distrito = Column(type_=types.Text, nullable=False)
    direccion = Column(type_=types.Text, nullable=False)
    horarioLunes = Column(type_=types.Text, name='horario_lunes',default='Por definir' )
    horarioMartes = Column(type_=types.Text, name='horario_martes',default='Por definir')
    horarioMiercoles = Column(type_=types.Text, name='horario_miercoles', default='Por definir')
    horarioJueves = Column(type_=types.Text, name='horario_jueves',default='Por definir')
    horarioViernes = Column(type_=types.Text, name='horario_viernes',default='Por definir')
    horarioSabado = Column(type_=types.Text, name='horario_sabado',default='Por definir')
    horarioDomingo = Column(type_=types.Text, name='horario_domingo',default='Por definir')
    fotoLogo = Column(type_=types.Text, name= 'foto_logo',nullable=False) #verificar
    fotoLocal1 = Column(type_=types.Text, name= 'foto_local_1')#verificar
    fotoLocal2 = Column(type_=types.Text, name= 'foto_local_2')#verificar
    fotoLocal3 = Column(type_=types.Text, name= 'foto_local_3')#verificar
    fotoLocal4 = Column(type_=types.Text, name= 'foto_local_4')#verificar
    paginaWeb = Column(type_=types.Text, name='pagina_web')
    usuarioId = Column(ForeignKey(column='usuarios.id'),type_=types.Integer, nullable=False, name='usuario_id')

    __tablename__ = "establecimientos"