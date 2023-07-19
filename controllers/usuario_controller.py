from flask_restful import Resource, request
from models.usuario_model import UsuarioModel
from config import conexion
from dtos.usuario_dto import RegistroUsuarioRequestDto,IniciarSesionRequestDto,UsuarioResponseDto, PerfilRequestDto
from bcrypt import gensalt, hashpw, checkpw
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity

class RegistroController(Resource):
    def post(self):
        data = request.json 
        dto = RegistroUsuarioRequestDto()
        try:
          dataValidada = dto.load(data)
          password = bytes(dataValidada.get('password'),'utf-8')

          salt =gensalt()

          hash= hashpw(password,salt)
          hashString = hash.decode('utf-8')

          dataValidada['password'] = hashString

          nuevoUsuario = UsuarioModel(**dataValidada)
          conexion.session.add(nuevoUsuario)
          conexion.session.commit()

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
      
   @jwt_required()  
   def get(self):
      resultado= conexion.session.query(UsuarioModel).all()
      dto= UsuarioResponseDto(many=True)
      data=dto.dump(resultado)
      return{
         "message":"Aqui esta la lista de usuarios",
         "content":data
      }
   
class PerfilController(Resource):
   @jwt_required()
   def get(self):
      identificador = get_jwt_identity()
      print(identificador)
      usuarioEncontrado = conexion.session.query(UsuarioModel).all()
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
            raise Exception ("no se encontro el usuario")
         if id != usuarioId:
            raise Exception("Tu no puedes borrar este perfil")

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
                #condici para comprar id con usuarioID , si no son iguales 
                raise Exception("Perfil no existe")
            if id != usuarioId:
                raise Exception("Tu no puedes modificar este perfil")
            dto=PerfilRequestDto()
            dataValidada =dto.load(request.json)

            conexion.session.query(UsuarioModel).filter_by(id = id).update(dataValidada)

            conexion.session.commit()
            resultado = PerfilRequestDto().dump(usuario)

            return{
                    "message" :"Publicacion actualizada exitosamente",
                    "content" : resultado
            }, 201
      except Exception as e:
            return{
                "message":"error al intentar actualizar",
                "content": e.args
            }, 400