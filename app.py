from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from config import conexion
from models.usuario_model import UsuarioModel
from models.establecimiento_model import EstablecimientoModel
from models.evento_model import EventoModel
from flask_jwt_extended import JWTManager
from controllers.usuario_controller import RegistroController,LoginController,PerfilController, UsuarioController
from controllers.establecimiento_controller import EstablecimientosController
from controllers.establecimientosUsuarios_controller import EstablecimientosUsuariosController,EstablecimientoUsuariosController
from controllers.establecimientosGenerales_controller import EstablecimientosGeneralesController
from controllers.evento_controller import EventosController
from controllers.eventosUsuarios_controller import EventosUsuariosController,EventoUsuariosController
from controllers.eventosGenerales_controller import EventosGeneralesController
from datetime import timedelta
from flask_cors import CORS
from os import environ
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app= Flask(__name__)
CORS(app)
api = Api(app)
app.config['JWT_SECRET_KEY']=environ.get('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES']= timedelta(weeks=20)

jwt=JWTManager(app)

@jwt.unauthorized_loader
def tokenRequerida(razon):
    return {
        'message':"Se necesita una token para realizar esta acción"
    },401

@jwt.invalid_token_loader
def tokenInvalida(razon):
   
    print(razon)
    message = ''
    if razon == 'Not enough segments':
        message = 'La token tiene que tener 3 segmentos, el header, payload y signature'

    elif razon == "Invalid header string: 'utf-8' codec can't decode byte 0xc7 in position 0: invalid continuation byte":
        message = 'Token invalida'

    elif razon == 'Signature verification failed':
        message = 'Esta token no pertenece a esta API'

    return {
        'message': message
    }, 401

app.config['SQLALCHEMY_DATABASE_URI']=environ.get('DATABASE_URL')

conexion.init_app(app)

Migrate(app,conexion)

#Rutas
  #Usuarios
api.add_resource(RegistroController,'/registro-usuario')
api.add_resource(LoginController,'/iniciar-sesion')
api.add_resource(PerfilController,'/perfil')
api.add_resource(UsuarioController,'/perfil/<int:id>')

  #Establecimientos
  #Establecimientos Vista Principal(usuario registrado) 
api.add_resource(EstablecimientosController,'/establecimientos')
  #Establecimientos Vista Mi información(empresario)
api.add_resource(EstablecimientosUsuariosController,'/establecimientos-miInformacion')
  #Establecimiento Vista mi Información(empresario)
api.add_resource(EstablecimientoUsuariosController,'/establecimiento-miInformacion/<int:id>') 
   #Establecimientos Vista Principal(usuario no registrado)  
api.add_resource(EstablecimientosGeneralesController,'/establecimientos-generales')
  
  # Eventos 
  #Eventos Vista Principal(empresario)
api.add_resource(EventosController,'/eventos')
  #Eventos Vista Mi información(empresario)
api.add_resource(EventosUsuariosController,'/eventos-miInformacion')
  #Eventos Vista Mi información(empresario)
api.add_resource(EventoUsuariosController,'/evento-miInformacion/<int:id>')
   #Eventos Vista Principal(usuario no registrado)  
api.add_resource(EventosGeneralesController,'/eventos-generales')

if __name__ == ('__main__'):
    app.run(debug=True)