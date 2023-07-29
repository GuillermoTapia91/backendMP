from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.usuario_model import UsuarioModel, TipoUsuario
from marshmallow import Schema, fields
from marshmallow_enum import EnumField

#(post)
class RegistroUsuarioRequestDto(SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModel

#Perfil(get)
class UsuarioResponseDto(SQLAlchemyAutoSchema):
    tipoUsuario = EnumField(enum=TipoUsuario, by_value=True)
    password = auto_field(load_only=True)
    class Meta:
        model = UsuarioModel

#(post)
class IniciarSesionRequestDto(Schema):
    correo = fields.Email(required = True)
    password = fields.String(required=True)

#(put)
class PerfilRequestDto(Schema):
    nombre = fields.String()
    apellido = fields.String()
