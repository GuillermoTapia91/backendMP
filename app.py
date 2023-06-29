from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from config import conexion
from models.usuario_model import UsuarioModel
from models.establecimiento_model import EstablecimientoModel
from models.evento_model import EventoModel
from flask_jwt_extended import JWTManager
from controllers.usuario_controller import RegistroController,LoginController,PerfilController
from controllers.establecimiento_controller import EstablecimientosController
from controllers.establecimientosUsuarios_controller import EstablecimientosUsuariosController
from controllers.evento_controller import EventosController
from controllers.eventosUsuarios_controller import EventosUsuariosController
from datetime import timedelta

from os import environ
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app= Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY']=environ.get('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES']= timedelta(weeks=20)

JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI']=environ.get('DATABASE_URL')

conexion.init_app(app)

Migrate(app,conexion)

#Rutas
  #Usuarios
api.add_resource(RegistroController,'/registro-usuario')
api.add_resource(LoginController,'/iniciar-sesion')
api.add_resource(PerfilController,'/perfil')

  #Establecimientos Vista Principal(usuario registrado) 
api.add_resource(EstablecimientosController,'/establecimientos')
  #Establecimientos Vista Mi información(empresario)
api.add_resource(EstablecimientosUsuariosController,'/establecimientos-miInformacion')
  #Eventos Vista Principal(empresario)
api.add_resource(EventosController,'/eventos')
  #Eventos Vista Mi información(empresario)
api.add_resource(EventosUsuariosController,'/eventos-miInformacion')


if __name__ == ('__main__'):
    app.run(debug=True)