# SmartLead AI
AI ile sohbet edip ziyaretçilerden iletişim bilgisi (lead) toplayan Flask uygulaması.
Mimari: config -> database (SQL) -> services/ai_service (AI) -> routes (yönlendirme) -> create_app.

## Çalıştırma
    python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env      # GROQ_API_KEY'i yaz
    python run.py             # http://localhost:5000

## Uç noktalar
GET /health · POST /api/sohbet {mesaj, gecmis} · POST /api/leads {isim, telefon, mesaj} · GET /api/leads

## Yayın
Render: Build `pip install -r requirements.txt`, Start `gunicorn run:app`; env: GROQ_API_KEY, SECRET_KEY, FLASK_ENV=production.
