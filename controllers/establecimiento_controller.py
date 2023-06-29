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

class EstablecimientosController(Resource):
  
  #para listar los establecimentos en la pagina principal, luego de iniciar sesion
    @jwt_required()
    def get(self):

       resultado = conexion.session.query(EstablecimientoModel).all()

       dto = EstablecimientoResponseDto(many=True)
       establecimientos = dto.dump(resultado)

       return {
          'content': establecimientos
       }


