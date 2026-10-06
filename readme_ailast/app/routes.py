# app/routes.py — Sadece isteği karşılar, doğrular, doğru katmana yönlendirir.
# Bu dosyada SQL veya AI API kodu YOKTUR.
from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

pages_bp = Blueprint('pages', __name__)   # HTML sayfaları
api_bp = Blueprint('api', __name__)       # JSON API (/api öneki __init__'te verilir)


@pages_bp.route('/')
def index():
    return render_template('index.html')


@pages_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    veri = request.get_json(silent=True) or {}
    mesaj = (veri.get('mesaj') or '').strip()
    if not mesaj:
        return jsonify({'basari': False, 'hata': 'mesaj alani zorunlu'}), 400
    try:
        cevap = ai_service.yanit_uret(mesaj, veri.get('gecmis'))
        return jsonify({'basari': True, 'cevap': cevap})
    except AIServiceError:
        return jsonify({'basari': False,
                        'hata': 'Asistan su an yanit veremiyor, lutfen tekrar deneyin.'}), 503


@api_bp.route('/leads', methods=['POST'])
def lead_kaydet():
    veri = request.get_json(silent=True) or {}
    isim = (veri.get('isim') or '').strip()
    telefon = (veri.get('telefon') or '').strip()
    mesaj = (veri.get('mesaj') or '').strip()
    if not isim or not telefon:
        return jsonify({'basari': False, 'hata': 'isim ve telefon zorunlu'}), 400
    try:
        yeni_id = lead_ekle(isim, telefon, mesaj)
        return jsonify({'basari': True, 'id': yeni_id}), 201
    except Exception:
        # İç hata detayını kullanıcıya sızdırmıyoruz
        return jsonify({'basari': False, 'hata': 'Kayit sirasinda bir hata olustu'}), 500


@api_bp.route('/leads', methods=['GET'])
def lead_listele():
    try:
        leadler = tum_leadler()
        # Wix Repeater her objede _id ister; backend bunu hazır verir
        for l in leadler:
            l['_id'] = str(l['id'])
        return jsonify({'basari': True, 'leadler': leadler})
    except Exception:
        return jsonify({'basari': False, 'hata': 'Liste alinamadi'}), 500
