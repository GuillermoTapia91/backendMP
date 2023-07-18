from flask_restful import Resource,request
from config import conexion
from models.evento_model import EventoModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from dtos.evento_dto import EventoRequestDto,EventoResponseDto
from os import path, getcwd,environ
from werkzeug.utils import secure_filename
from uuid import uuid4
from boto3 import Session

AWSSession = Session(aws_access_key_id=environ.get('AWS_ACCESS_KEY'),aws_secret_access_key=environ.get('AWS_SECRET_KEY'),region_name=environ.get('AWS_BUCKET_REGION'))

class EventosController(Resource):

  #para listar los eventos en la pagina principal, luego de iniciar sesion
    @jwt_required()
    def get(self):
      try: 
        resultado = conexion.session.query(EventoModel).all()
        S3= AWSSession.client('s3') 
        dto = EventoResponseDto(many=True)
        eventos = dto.dump(resultado)

        for evento in eventos:
          if evento.get('fotoEvento'):  
            evento['fotoEvento']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':evento.get("fotoEvento")},#ExpiresIn=50
            )

        return {
            'content': eventos
        }
     
      except Exception as e:
           return {
              'message':'Error al listar eventos',
              'content':e.args
           },400