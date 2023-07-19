from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.evento_model import EventoModel
from marshmallow import Schema, fields



#para listar eventos(get)
class EventoResponseDto(SQLAlchemyAutoSchema):
    class Meta:
        model = EventoModel

#para Crear evento(post)
class EventoRequestDto(Schema):

  descripcion = fields.Str(required=True)
  paginaWeb = fields.Str(required=True)