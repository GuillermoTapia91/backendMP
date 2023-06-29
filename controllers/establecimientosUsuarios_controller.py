from flask_restful import Resource,request
from config import conexion
from models.establecimiento_model import EstablecimientoModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from dtos.establecimiento_dto import EstablecimientoRequestDto,EstablecimientoResponseDto

# cloudinary.config( 
#   cloud_name = "duwiwltu2", 
#   api_key = "634234552161273", 
#   api_secret = "sUZeOypHEL57k1nQLUDnxzQq5VQ" 
# )

class EstablecimientosUsuariosController(Resource):
  #Para crear un establecimiento, el usuario debe haber iniciado sesion  
    @jwt_required()
    def post(self):
        data = request.json #request.form
        
        usuarioId = get_jwt_identity()
        dto = EstablecimientoRequestDto()
        try:
          dataValidada = dto.load(data)
          nuevoEstablecimiento = EstablecimientoModel(**dataValidada,usuarioId=usuarioId)

          conexion.session.add(nuevoEstablecimiento)
          conexion.session.commit()

          dtoRespuesta = EstablecimientoResponseDto()
          resultado = dtoRespuesta.dump(nuevoEstablecimiento)
          return {
              'message': 'Establecimiento creado exitosamente',
              'content': resultado
          },201
        
        except Exception as e:
           conexion.session.rollback()
           return {
              'message': 'Error al crear establecimiento',
              'content': e.args
           },400

  #para listar los establecimentos creados por el empresario en la vista mi información, luego de iniciar sesion
    @jwt_required()
    def get(self):

       usuarioId = get_jwt_identity() 
       resultado = EstablecimientoModel.query.filter_by(usuarioId=usuarioId).all()
       if not resultado:
          return {
             'message': 'Aun no has resgistrado un establecimiento'
          } 
       dto = EstablecimientoResponseDto(many=True)
       establecimientos = dto.dump(resultado)

       return {
          'content': establecimientos
       }


