from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.establecimiento_model import EstablecimientoModel, TipoEstablecimiento
from marshmallow_enum import EnumField

#para Crear establecimiento(post)
class EstablecimientoRequestDto(SQLAlchemyAutoSchema):
    class Meta:
        model = EstablecimientoModel

#Para listar establecimientos(get)
class EstablecimientoResponseDto(SQLAlchemyAutoSchema):
    tipoEstablecimiento = EnumField(enum=TipoEstablecimiento,by_value=True)
    class Meta:
        model = EstablecimientoModel