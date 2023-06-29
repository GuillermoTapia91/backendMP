from flask_restful import Resource,request
from config import conexion
from models.evento_model import EventoModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from dtos.evento_dto import EventoRequestDto,EventoResponseDto


class EventosController(Resource):

  #para listar los eventos en la pagina principal, luego de iniciar sesion
    @jwt_required()
    def get(self):
       
       print(id)
       resultado = conexion.session.query(EventoModel).all()
       
       dto = EventoResponseDto(many=True)
       eventos = dto.dump(resultado)

       return {
          'content': eventos
       }
   