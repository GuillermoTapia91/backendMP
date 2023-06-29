from flask_restful import Resource, request
from models.usuario_model import UsuarioModel
from config import conexion
from dtos.usuario_dto import RegistroUsuarioRequestDto,IniciarSesionRequestDto,UsuarioResponseDto
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
          print(hashString)

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