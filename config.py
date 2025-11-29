import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Configuración RDS
    DB_ENGINE = os.environ.get('DB_ENGINE', 'mysql')
    DB_HOST = os.environ.get('DB_HOST', 'database-1.c9kaeqiwud9r.us-east-1.rds.amazonaws.com')
    DB_NAME = os.environ.get('DB_NAME', 'formulario')
    DB_USER = os.environ.get('DB_USER', 'admin')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '12345678')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    
    @property
    def DATABASE_URI(self):
        if self.DB_ENGINE == 'mysql':
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}