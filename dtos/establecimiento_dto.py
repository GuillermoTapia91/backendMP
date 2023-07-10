from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.establecimiento_model import EstablecimientoModel, TipoEstablecimiento
from marshmallow import Schema, fields
from marshmallow_enum import EnumField

#para Crear establecimiento(post)
# class EstablecimientoRequestDto(SQLAlchemyAutoSchema):
#     class Meta:
#         model = EstablecimientoModel

#Para listar establecimientos(get)
class EstablecimientoResponseDto(SQLAlchemyAutoSchema):
    tipoEstablecimiento = EnumField(enum=TipoEstablecimiento,by_value=True)
    class Meta:
        model = EstablecimientoModel

class EstablecimientoRequestDto(Schema):
    tipoEstablecimiento = EnumField(enum=TipoEstablecimiento,by_value=True)
    nombre = fields.Str(required=True)
    distrito = fields.Str(required=True)
    direccion = fields.Str(required=True)
    horarioLunes = fields.Str(required=True)
    horarioMartes = fields.Str(required=True)
    horarioMiercoles = fields.Str(required=True)
    horarioJueves = fields.Str(required=True)
    horarioViernes = fields.Str(required=True)
    horarioSabado = fields.Str(required=True)
    horarioDomingo = fields.Str(required=True)
    paginaWeb = fields.Str(required=True)