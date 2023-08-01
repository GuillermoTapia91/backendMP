from flask_restful import Resource,request
from config import conexion
from models.eventoE_model import EventoEModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from dtos.eventoE_dto import EventoERequestDto,EventoEResponseDto
from os import path, getcwd,environ,remove
from werkzeug.utils import secure_filename
from uuid import uuid4
from boto3 import Session

AWSSession = Session(aws_access_key_id=environ.get('AWS_ACCESS_KEY'),aws_secret_access_key=environ.get('AWS_SECRET_KEY'),region_name=environ.get('AWS_BUCKET_REGION'))

#para crear un evento en la vista Mi información, despues de que el usuario inicie sesion
class EventosEUsuariosController(Resource):
    @jwt_required()
    def post(self):
        data = request.form #request.json
        fotoEvento = request.files.get('fotoEvento')
        # usuarioId = get_jwt_identity()
        directorioActual = getcwd() 
        S3 = AWSSession.client('s3')
        dto = EventoERequestDto()
        try:
          dataValidada = dto.load(data)
          nombreFotoEvento = None

          if fotoEvento:
              filename =secure_filename(fotoEvento.filename)
              nombreFotoEvento = f'{uuid4()}-{filename}'
              ruta=path.join(directorioActual,'imagenes',nombreFotoEvento)
              fotoEvento.save(ruta)
              S3.upload_file(ruta,environ.get('AWS_BUCKET_NAME'), nombreFotoEvento)
              remove(ruta)
          # nuevoEvento = EventoEModel(**dataValidada,usuarioId=usuarioId,fotoEvento=nombreFotoEvento)
          nuevoEvento = EventoEModel(**dataValidada,fotoEvento=nombreFotoEvento)

          conexion.session.add(nuevoEvento)
          conexion.session.commit()

          dtoRespuesta = EventoEResponseDto()
          resultado = dtoRespuesta.dump(nuevoEvento)
          return {
              'message': 'Evento creado exitosamente',
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
      try:
       usuarioId = get_jwt_identity() 
       
       #resultado = conexion.session.query(EventoModel).filter_by(usuarioId=id).all()
       resultado = EventoEModel.query.filter_by(usuarioId=usuarioId).all()

       S3= AWSSession.client('s3') 
       if not resultado:
          return {
             'message': 'Aun no has registrado un evento'
          }
        
       dto = EventoEResponseDto(many=True)
       eventos = dto.dump(resultado)
       
       for evento in eventos:
        if evento.get('fotoEvento'):  
          evento['fotoEvento']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':evento.get("fotoEvento")},
          #ExpiresIn=50
          ) 

       return {
          'content': eventos
       }
      
      except Exception as e:
           return {
              'message':'Error al listar eventos',
              'content':e.args
           },400

class EventoEUsuariosController(Resource):

  @jwt_required()
  # /evento-miInformacion/<int:id>
  def put(self, id):
    data = request.form #request.json
    fotoEvento = request.files.get('fotoEvento')

    usuarioId = get_jwt_identity()
    dto = EventoERequestDto()
    dataValidada = dto.load(data)
    directorioActual = getcwd()
    try: 
      
      eventoEncontrado = conexion.session.query(EventoEModel).filter_by(id=id,usuarioId=usuarioId).first()
      
      if not eventoEncontrado:
          raise Exception('Este evento no existe')
      
      S3 = AWSSession.client('s3')
      if eventoEncontrado.fotoEvento:
        S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= eventoEncontrado.fotoEvento)

      nombreFotoEvento = None

      if fotoEvento:
          filename =secure_filename(fotoEvento.filename)
          nombreFotoEvento = f'{uuid4()}-{filename}'
          ruta=path.join(directorioActual,'imagenes',nombreFotoEvento)
          fotoEvento.save(ruta)
          S3.upload_file(ruta,environ.get('AWS_BUCKET_NAME'), nombreFotoEvento)
          remove(ruta)

      dataValidada['fotoEvento']= nombreFotoEvento  

      conexion.session.query(EventoEModel).filter_by(id=id,usuarioId=usuarioId).update(dataValidada)      
      
      conexion.session.commit()
      # #resultado = EstablecimientoResponseDto().dump(establecimientoEditado)
      
      return {
          'message': 'Evento actualizado exitosamente',
          #'content': resultado
      },201
    except Exception as e:
        return {
          'message': 'Error al actualizar el evento',
          'content': e.args
        }, 400  

  @jwt_required()
  def delete(self,id):
        try:
          usuarioId= get_jwt_identity()
          eventoEncontrado = conexion.session.query(EventoEModel).filter_by(id=id,usuarioId=usuarioId).first()
          if not eventoEncontrado:
            return {
                'message': 'Este evento no existe'
            }

          S3 = AWSSession.client('s3')
          if eventoEncontrado.fotoEvento:
            S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= eventoEncontrado.fotoEvento)   
          
          conexion.session.query(EventoEModel).filter_by(id=id,usuarioId=usuarioId).delete()
 
          conexion.session.commit()

          return {
             'message':'El evento se eliminó exitosamente'
          }
        except Exception as e:
           return {
              'message':'Error al eliminar el evento',
              'content':e.args
           },400       