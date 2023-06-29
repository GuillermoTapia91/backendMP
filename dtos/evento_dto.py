from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.evento_model import EventoModel

#para Crear evento(post)
class EventoRequestDto(SQLAlchemyAutoSchema):
    class Meta:
        model = EventoModel

#para listar eventos(get)
class EventoResponseDto(SQLAlchemyAutoSchema):
    class Meta:
        model = EventoModel
