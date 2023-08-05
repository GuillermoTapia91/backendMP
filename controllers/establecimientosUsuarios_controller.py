from flask_restful import Resource,request
from config import conexion
from models.establecimiento_model import EstablecimientoModel
from models.usuario_model import UsuarioModel, TipoUsuario
from flask_jwt_extended import get_jwt_identity, jwt_required
from dtos.establecimiento_dto import EstablecimientoRequestDto,EstablecimientoResponseDto
from os import path, getcwd,environ, remove
from werkzeug.utils import secure_filename
from uuid import uuid4
from boto3 import Session

AWSSession = Session(aws_access_key_id=environ.get('AWS_ACCESS_KEY'),aws_secret_access_key=environ.get('AWS_SECRET_KEY'),region_name=environ.get('AWS_BUCKET_REGION'))

class EstablecimientosUsuariosController(Resource):
  #Para crear un establecimiento, el usuario debe haber iniciado sesion  
    @jwt_required()
    def post(self):
        
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
        
        directorioActual = getcwd() 
        S3 = AWSSession.client('s3')
        dto = EstablecimientoRequestDto()
        
        try:
          dataValidada = dto.load(data)
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

          nuevoEstablecimiento = EstablecimientoModel(**dataValidada,fotoLogo=nombreFotoLogo,fotoLocal1=nombreFotoLocal1,fotoLocal2=nombreFotoLocal2, fotoLocal3=nombreFotoLocal3,fotoLocal4=nombreFotoLocal4,usuarioId=usuarioId)

          conexion.session.add(nuevoEstablecimiento)
          conexion.session.commit()

          dtoRespuesta = EstablecimientoResponseDto()
          resultado = dtoRespuesta.dump(nuevoEstablecimiento)
          return {
              'message': 'Establecimiento creado exitosamente',
              'content': resultado
          },201
        
        except Exception as e:
           conexion.session.rollback()
           return {
              'message': 'Error al crear establecimiento',
              'content': e.args
           },400

  #para listar los establecimentos creados por el empresario en la vista mi información, luego de iniciar sesion
    @jwt_required()
    def get(self):

       usuarioId = get_jwt_identity() 
       print(usuarioId)
       resultado = EstablecimientoModel.query.filter_by(usuarioId=usuarioId).all()
       try:
        S3= AWSSession.client('s3')
        if not resultado:
            return {
              'message': 'Aun no has resgistrado un establecimiento'
            } 
        dto = EstablecimientoResponseDto(many=True)
        establecimientos = dto.dump(resultado)

        for establecimiento in establecimientos:
          if establecimiento.get('fotoLogo'):  
            establecimiento['fotoLogo']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':establecimiento.get("fotoLogo")},
            #ExpiresIn=50
            )

          if establecimiento.get('fotoLocal1'):  
            establecimiento['fotoLocal1']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':establecimiento.get("fotoLocal1")},
            #ExpiresIn=50
            )

          if establecimiento.get('fotoLocal2'):  
            establecimiento['fotoLocal2']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':establecimiento.get("fotoLocal2")},
            #ExpiresIn=50
            )

          if establecimiento.get('fotoLocal3'):  
            establecimiento['fotoLocal3']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':establecimiento.get("fotoLocal3")},
            #ExpiresIn=50
            )

          if establecimiento.get('fotoLocal4'):  
            establecimiento['fotoLocal4']=S3.generate_presigned_url('get_object',Params={'Bucket':environ.get('AWS_BUCKET_NAME'),'Key':establecimiento.get("fotoLocal4")},
            #ExpiresIn=50
            )

        return establecimientos 
        
       except Exception as e:
         return {
              'message':'Error al listar establecimientos',
              'content':e.args
           },400   

class EstablecimientoUsuariosController(Resource):
    @jwt_required()
    # /establecimiento-miInformacion/<int:id>
    def put(self, id):
      data = request.form 
      fotoLogo = request.files.get('fotoLogo')
      fotoLocal1 = request.files.get('fotoLocal1')
      fotoLocal2 = request.files.get('fotoLocal2')
      fotoLocal3 = request.files.get('fotoLocal3')
      fotoLocal4 = request.files.get('fotoLocal4')
      usuarioId = get_jwt_identity()
      dto = EstablecimientoRequestDto()
      dataValidada = dto.load(data)
      directorioActual = getcwd()
      try: 
        
        establecimientoEncontrado = conexion.session.query(EstablecimientoModel).filter_by(id=id,usuarioId=usuarioId).first()
        
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

        conexion.session.query(EstablecimientoModel).filter_by(id=id,usuarioId=usuarioId).update(dataValidada)      
        
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
          usuarioId= get_jwt_identity()
          establecimientoEncontrado = conexion.session.query(EstablecimientoModel).filter_by(id=id,usuarioId=usuarioId).first()
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
        
          conexion.session.query(EstablecimientoModel).filter_by(id=id,usuarioId=usuarioId).delete()
 
          conexion.session.commit()

          return {
             'message':'El establecimiento se eliminó exitosamente'
          }
       
        except Exception as e:
           return {
              'message':'Error al eliminar el establecimiento',
              'content':e.args
           },400