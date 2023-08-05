from flask_restful import Resource,request
from config import conexion
from models.establecimiento_model import EstablecimientoModel
from models.usuario_model import UsuarioModel, TipoUsuario
from flask_jwt_extended import get_jwt_identity, jwt_required
from dtos.establecimiento_dto import EstablecimientoAdminRequestDto
from os import path, getcwd,environ, remove
from werkzeug.utils import secure_filename
from uuid import uuid4
from boto3 import Session

AWSSession = Session(aws_access_key_id=environ.get('AWS_ACCESS_KEY'),aws_secret_access_key=environ.get('AWS_SECRET_KEY'),region_name=environ.get('AWS_BUCKET_REGION'))


  #Para Eeditar y elminar un establecimiento, el ADMIN debe haber iniciado sesion  
   
  

class EstablecimientosAdminController(Resource):
    @jwt_required()
    # /establecimiento-miInformacion/<int:id>
    def put(self, id):

      usuarioId = get_jwt_identity()
      users = UsuarioModel.query.filter_by(id=usuarioId).first()
      if not users or users.tipoUsuario != TipoUsuario.ADMINISTRADOR:
        return {
                'message': 'Solo los administradores pueden crear establecimientos en los establecimientos.'
            }, 403

      data = request.form 
      fotoLogo = request.files.get('fotoLogo')
      fotoLocal1 = request.files.get('fotoLocal1')
      fotoLocal2 = request.files.get('fotoLocal2')
      fotoLocal3 = request.files.get('fotoLocal3')
      fotoLocal4 = request.files.get('fotoLocal4')
      
      dto = EstablecimientoAdminRequestDto()
      dataValidada = dto.load(data)
      directorioActual = getcwd()
      try: 
        
        establecimientoEncontrado = conexion.session.query(EstablecimientoModel).filter_by(id=id).first()
        
        if not establecimientoEncontrado:
           raise Exception('Establecimiento no existe')
        
        S3 = AWSSession.client('s3')
        if establecimientoEncontrado.fotoLogo:
          S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= establecimientoEncontrado.fotoLogo)

        if establecimientoEncontrado.fotoLocal1:
          S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= establecimientoEncontrado.fotoLocal1)
        
        if establecimientoEncontrado.fotoLocal2:
          S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= establecimientoEncontrado.fotoLocal2)
        
        if establecimientoEncontrado.fotoLocal3:
          S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= establecimientoEncontrado.fotoLocal3)
        
        if establecimientoEncontrado.fotoLocal4:
          S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= establecimientoEncontrado.fotoLocal4)
        
        nombreFotoLogo = None
        nombreFotoLocal1 = None
        nombreFotoLocal2 = None
        nombreFotoLocal3 = None
        nombreFotoLocal4 = None
        
        if fotoLogo:
            filename =secure_filename(fotoLogo.filename)
            nombreFotoLogo = f'{uuid4()}-{filename}'
            ruta=path.join(directorioActual,'imagenes',nombreFotoLogo)
            fotoLogo.save(ruta)
            S3.upload_file(ruta,environ.get('AWS_BUCKET_NAME'), nombreFotoLogo)
            remove(ruta)

        if fotoLocal1:
            filename =secure_filename(fotoLocal1.filename)
            nombreFotoLocal1 = f'{uuid4()}-{filename}'
            ruta=path.join(directorioActual,'imagenes',nombreFotoLocal1)
            fotoLocal1.save(ruta)
            S3.upload_file(ruta,environ.get('AWS_BUCKET_NAME'), nombreFotoLocal1)
            remove(ruta)

        if fotoLocal2:
            filename =secure_filename(fotoLocal2.filename)
            nombreFotoLocal2 = f'{uuid4()}-{filename}'
            ruta=path.join(directorioActual,'imagenes',nombreFotoLocal2)
            fotoLocal2.save(ruta)
            S3.upload_file(ruta,environ.get('AWS_BUCKET_NAME'), nombreFotoLocal2)
            remove(ruta)

        if fotoLocal3:
            filename =secure_filename(fotoLocal3.filename)
            nombreFotoLocal3 = f'{uuid4()}-{filename}'
            ruta=path.join(directorioActual,'imagenes',nombreFotoLocal3)
            fotoLocal3.save(ruta)
            S3.upload_file(ruta,environ.get('AWS_BUCKET_NAME'), nombreFotoLocal3)
            remove(ruta)

        if fotoLocal4:
            filename =secure_filename(fotoLocal4.filename)
            nombreFotoLocal4 = f'{uuid4()}-{filename}'
            ruta=path.join(directorioActual,'imagenes',nombreFotoLocal4)
            fotoLocal4.save(ruta)
            S3.upload_file(ruta,environ.get('AWS_BUCKET_NAME'), nombreFotoLocal4)
            remove(ruta)

        dataValidada['fotoLogo']= nombreFotoLogo
        dataValidada['fotoLocal1']= nombreFotoLocal1
        dataValidada['fotoLocal2']= nombreFotoLocal2
        dataValidada['fotoLocal3']= nombreFotoLocal3
        dataValidada['fotoLocal4']= nombreFotoLocal4

        conexion.session.query(EstablecimientoModel).filter_by(id=id).update(dataValidada)      
        
        conexion.session.commit()
        
        return {
            'message': 'Establecimiento actualizado exitosamente',
          
        },201
      except Exception as e:
         return {
            'message': 'Error al actualizar el establecimiento',
            'content': e.args
         }, 400  

    @jwt_required()
    def delete(self,id):
        try:
          usuarioId = get_jwt_identity()
          users = UsuarioModel.query.filter_by(id=usuarioId).first()
          if not users or users.tipoUsuario != TipoUsuario.ADMINISTRADOR:
            return {
                    'message': 'Solo los administradores pueden crear establecimientos en los establecimientos.'
                }, 403
          
          establecimientoEncontrado = conexion.session.query(EstablecimientoModel).filter_by(id=id).first()
          if not establecimientoEncontrado:
            return {
                'message': 'Este establecimiento no existe'
            }
          
          S3 = AWSSession.client('s3')
          if establecimientoEncontrado.fotoLogo:
            S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= establecimientoEncontrado.fotoLogo)
          
          if establecimientoEncontrado.fotoLocal1:
            S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= establecimientoEncontrado.fotoLocal1)
          
          if establecimientoEncontrado.fotoLocal2:
            S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= establecimientoEncontrado.fotoLocal2)
          
          if establecimientoEncontrado.fotoLocal3:
            S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= establecimientoEncontrado.fotoLocal3)
          
          if establecimientoEncontrado.fotoLocal4:
            S3.delete_object(Bucket=environ.get('AWS_BUCKET_NAME'), Key= establecimientoEncontrado.fotoLocal4)
        
          conexion.session.query(EstablecimientoModel).filter_by(id=id).delete()
 
          conexion.session.commit()

          return {
             'message':'El establecimiento se eliminó exitosamente'
          }
       
        except Exception as e:
           return {
              'message':'Error al eliminar el establecimiento',
              'content':e.args
           },400