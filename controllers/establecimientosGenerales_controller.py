from flask_restful import Resource,request
from config import conexion
from models.establecimiento_model import EstablecimientoModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from dtos.establecimiento_dto import EstablecimientoRequestDto,EstablecimientoResponseDto
from os import path, getcwd,environ
from werkzeug.utils import secure_filename
from uuid import uuid4
from boto3 import Session

AWSSession = Session(aws_access_key_id=environ.get('AWS_ACCESS_KEY'),aws_secret_access_key=environ.get('AWS_SECRET_KEY'),region_name=environ.get('AWS_BUCKET_REGION'))
class EstablecimientosGeneralesController(Resource):
  
  #para listar los establecimentos en la pagina principal, sin iniciar sesion
    
    def get(self):

       resultado = conexion.session.query(EstablecimientoModel).all()
       S3= AWSSession.client('s3') 
       dto = EstablecimientoResponseDto(many=True)
       establecimientos = dto.dump(resultado)

       for establecimiento in establecimientos:
        if establecimiento.get('fotoLogo'):  
          establecimiento['fotoLogo']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':establecimiento.get("fotoLogo")},#ExpiresIn=50
          )
        
        if establecimiento.get('fotoLocal1'):  
          establecimiento['fotoLocal1']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':establecimiento.get("fotoLocal1")},#ExpiresIn=50
          )
        
        if establecimiento.get('fotoLocal2'):  
          establecimiento['fotoLocal2']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':establecimiento.get("fotoLocal2")},#ExpiresIn=50
          )
        
        if establecimiento.get('fotoLocal3'):  
          establecimiento['fotoLocal3']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':establecimiento.get("fotoLocal3")},#ExpiresIn=50
          )
        
        if establecimiento.get('fotoLocal4'):  
          establecimiento['fotoLocal4']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':establecimiento.get("fotoLocal4")},#ExpiresIn=50
          )

        
        # if persona.get('portada'):  
        #   persona['portada']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':persona.get("portada")},ExpiresIn=50)

       return establecimientos
       

