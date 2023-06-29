from flask_restful import Resource,request
from config import conexion
from models.evento_model import EventoModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from dtos.evento_dto import EventoRequestDto,EventoResponseDto

#para crear un evento en la vista Mi información, despues de que el usuario inicie sesion
class EventosUsuariosController(Resource):
    @jwt_required()
    def post(self):
        data = request.json #request.form
        usuarioId = get_jwt_identity()
        dto = EventoRequestDto()
        try:
          dataValidada = dto.load(data)
          nuevoEvento = EventoModel(**dataValidada,usuarioId=usuarioId)

          conexion.session.add(nuevoEvento)
          conexion.session.commit()

          dtoRespuesta = EventoResponseDto()
          resultado = dtoRespuesta.dump(nuevoEvento)
          return {
              'message': 'Establecimiento creado exitosamente',
              'content': resultado
          },201


        except Exception as e:
           conexion.session.rollback()
           return {
              'message': 'Error al crear el evento',
              'content': e.args
           },400

  #para listar los eventos creados pr el empresario en la vista mi información, luego de iniciar sesion
    @jwt_required()
    def get(self):
       usuarioId = get_jwt_identity() 
       print(id)
       #resultado = conexion.session.query(EventoModel).filter_by(usuarioId=id).all()
       resultado = EventoModel.query.filter_by(usuarioId=usuarioId).all()

       if not resultado:
          return {
             'message': 'Aun no has registrado un evento'
          }
        
       print(resultado)
       dto = EventoResponseDto(many=True)
       eventos = dto.dump(resultado)

       return {
          'content': eventos
       }
   