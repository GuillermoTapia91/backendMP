from flask_restful import Resource, request, reqparse
from models.usuario_model import UsuarioModel
from config import conexion
from dtos.usuario_dto import RegistroUsuarioRequestDto,IniciarSesionRequestDto,UsuarioResponseDto, PerfilRequestDto
from bcrypt import gensalt, hashpw, checkpw
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from datetime import datetime
from correo import enviarCorreo

class RegistroController(Resource):
    def post(self):
        data = request.json 
        dto = RegistroUsuarioRequestDto()

        try:
            dataValidada = dto.load(data)
            parser = reqparse.RequestParser()
            parser.add_argument('fechaNacimiento', type=str, required=True, help='Fecha de nacimiento requerida (formato: yyyy-mm-dd)')

            data = parser.parse_args()
            fecha_nacimiento_str = data['fechaNacimiento']
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d")

            edad_minima = 18
            hoy = datetime.today().date()
            edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

            if edad < edad_minima:
               return {
                  'message': 'Debes tener al menos {} años para registrarte.'.format(edad_minima)
               }, 400
            password = bytes(dataValidada.get('password'),'utf-8')
            salt =gensalt()

            hash= hashpw(password,salt)
            hashString = hash.decode('utf-8')

            dataValidada['password'] = hashString
            
            nuevoUsuario = UsuarioModel(**dataValidada)
            conexion.session.add(nuevoUsuario)
            conexion.session.commit()
            print(dataValidada)
            enviarCorreo([dataValidada['correo']])
            
            return {
               'message': 'Usuario creado exitosamente'
            },201
        
        except Exception as e:
           conexion.session.rollback()
           return{
              'message' : 'Error al crear usuario',
              'content':e.args
           }, 400
   
class LoginController(Resource):
   def post(self):
      
      data = request.json
      dto = IniciarSesionRequestDto()
      try:
         
        dataValidada = dto.load(data)
        usuarioEncontrado = conexion.session.query(UsuarioModel).filter_by(correo = dataValidada.get('correo')).first()
        print(usuarioEncontrado)

        if usuarioEncontrado is None:
           raise Exception('Usuario con correo {} no existe'.format(dataValidada.get('correo')))
        password = bytes(dataValidada.get('password'),'utf-8')
        passwordHashed = bytes(usuarioEncontrado.password,'utf-8')

        resultado = checkpw(password, passwordHashed)
        print(resultado)

        if resultado:
           token = create_access_token(identity=usuarioEncontrado.id)
           return {
              'message': 'Bienvenido',
              'content': token
           }
        else:
           raise Exception('Contraseña incorrecta')
       
      except Exception as e:
        return {
          'message': 'Error al iniciar Sesion',
          'content': e.args
        },400
      
class UsuariosController(Resource):
   def get(self):
      resultado= conexion.session.query(UsuarioModel).all()
      dto= UsuarioResponseDto(many=True)
      data=dto.dump(resultado)
      return{
         "message":"Lista de usuarios",
         "content":data
      }
class PerfilController(Resource):
   @jwt_required()
   def get(self):
      identificador = get_jwt_identity()
      print(identificador)
      usuarioEncontrado = conexion.session.query(UsuarioModel).filter_by(id=identificador).first()
      dto = UsuarioResponseDto()
      resultado = dto.dump(usuarioEncontrado)
      return {
         'content': resultado
      }     
   
class UsuarioController(Resource):
   @jwt_required()  
   def delete(self, id):
      try:
         usuarioId= get_jwt_identity()
         usuarioEliminado=conexion.session.query(UsuarioModel).filter_by(id=id).delete()
         if  usuarioEliminado == 0 :
            raise Exception ("No se encontro el usuario")
         if id != usuarioId:
            raise Exception("Tú no puedes borrar este usuario")

         conexion.session.commit()
         return{
                  "message":"Usuario eliminado exitosamente"
               },201

      except Exception as e:
            return{
                "message":"Error al eliminar al usuario",
                "content": e.args
            },400
   
   @jwt_required()
   def put(self, id):
      try:
            usuarioId = get_jwt_identity()
            print(usuarioId)
            usuario = conexion.session.query(UsuarioModel).filter_by(id=id).first()
            if not usuario:
                raise Exception("Este usuario no existe")
            if id != usuarioId:
                raise Exception("Tú no puedes modificar este usuario")
            dto=PerfilRequestDto()
            dataValidada =dto.load(request.json)

            conexion.session.query(UsuarioModel).filter_by(id = id).update(dataValidada)

            conexion.session.commit()
            resultado = PerfilRequestDto().dump(usuario)

            return{
                    "message" :"Usuario actualizado exitosamente",
                    "content" : resultado
            }, 201
      except Exception as e:
            return{
                "message":"error al intentar actualizar",
                "content": e.args
            }, 400
      
   