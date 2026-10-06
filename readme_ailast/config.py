# config.py — TÜM ayarlar tek merkezde. Başka dosya os.environ'a dokunmaz.
import os
from dotenv import load_dotenv

# .env dosyasını okuyup ortam değişkenlerine yükler (yoksa .env okunmaz!)
load_dotenv()


class Config:
    """Ortak ayarlar. Anahtar yoksa güvenli varsayılan kullanılır."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'gelistirme-anahtari')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'smartlead.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    DEBUG = False

    # Yapay zekânın kişiliği. KONUYA ÖZEL TEK YER BURASI: kendi işinize göre değiştirin.
    BUSINESS_CONTEXT = os.environ.get('BUSINESS_CONTEXT', (
        "Sen Cafe Mola'nin asistanisin. Menu, fiyat, calisma saatleri ve "
        "rezervasyon sorularini yanitla. Kibar ve samimi ol. Turkce konus. "
        "Yanitlarin kisa olsun. Musteriyi rezervasyon icin isim ve telefon "
        "birakmaya nazikce yonlendir."
    ))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# FLASK_ENV değerine göre sınıf seçmek için sözlük
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
