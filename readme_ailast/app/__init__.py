# app/__init__.py — Uygulama fabrikası: tüm parçaları birleştirir.
from flask import Flask, jsonify
from flask_cors import CORS

from config import config_by_name
from app.database import init_db
from app.routes import pages_bp, api_bp


def create_app(config_name='development'):
    app = Flask(__name__)

    # 1) Ayarları yükle
    app.config.from_object(config_by_name.get(config_name, config_by_name['development']))

    # 2) CORS: Wix gibi başka bir alan adından gelen isteklere izin verir
    origins = app.config['CORS_ORIGINS']
    CORS(app, resources={r"/api/*": {"origins": origins if origins == '*' else origins.split(',')}})

    # 3) Veritabanını hazırla (app context gerekir: g ve config buna bağlı)
    with app.app_context():
        init_db(app)

    # 4) Blueprint'leri kaydet (API'ye /api öneki)
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # Canlılık kontrolü (Render buraya bakar)
    @app.route('/health')
    def health():
        return jsonify({'basari': True, 'durum': 'aktif'})

    return app
