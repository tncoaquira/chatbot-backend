from src.application.autentificacion.models.index import Usuario
from src.database.chatbotDB import db
from src.common.utils.bcrypt import getHashPassword

def seeds_users():
    password=getHashPassword("12345678")
    usuario = Usuario(
        usuario="upb-admin",
        contrasenia=password,
        correo="tncoaquiralt@gmail",
        nombres="Ricardo Ernesto",
        apellidos="Beltran Sanabria",
        ci="12345678",
    )
    db.add(usuario)
    db.commit()
    db.close()
