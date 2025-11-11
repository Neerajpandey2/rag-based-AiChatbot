from flask import Flask
from app.routes.embed_routes import api_bp
from app.routes.qdrant_routes import qdrant_bp
from app.routes.askGemini import ask_bp
from app.routes.getPdfFromFrontend import upload_bp
from flasgger import Swagger
from flask_cors import CORS 

def create_app():
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'TechFeature Expert API',
        'uiversion': 3
    }

    Swagger(app)
    CORS(app)

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(qdrant_bp, url_prefix='/qdrantapi')
    app.register_blueprint(ask_bp, url_prefix='/ask')
    app.register_blueprint(upload_bp, url_prefix='/upload')
    return app