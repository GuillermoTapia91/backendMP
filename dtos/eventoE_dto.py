from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.eventoE_model import EventoEModel
from marshmallow import Schema, fields

#para listar eventos(get)
class EventoEResponseDto(SQLAlchemyAutoSchema):
    class Meta:
        model = EventoEModel

#para Crear evento(post)
class EventoERequestDto(Schema):

  descripcion = fields.Str(required=True)
  paginaWeb = fields.Str(required=True)
  establecimientoId = fields.Str(required=True)