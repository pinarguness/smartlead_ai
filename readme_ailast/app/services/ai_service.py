# app/services/ai_service.py — AI çağrıları YALNIZCA burada.
# Bu dosya Flask/HTTP/veritabanı bilmez; sadece yapay zekâ ile konuşur.
import requests
from config import Config

GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'
GROQ_MODEL = 'llama-3.1-8b-instant'


class AIServiceError(Exception):
    """AI servisine özel hata: rotalar bunu yakalayıp 503 döner."""


class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.provider = Config.AI_PROVIDER

    def _sistem_talimati(self):
        """AI'ın kişiliğini config'den okur."""
        return Config.BUSINESS_CONTEXT

    def _mesajlari_hazirla(self, mesaj, gecmis):
        """Sıra: sistem talimatı -> geçmiş -> yeni kullanıcı mesajı."""
        mesajlar = [{'role': 'system', 'content': self._sistem_talimati()}]
        for m in (gecmis or []):
            # Güvenlik: yalnızca beklenen rol ve metin biçimini kabul et
            if isinstance(m, dict) and m.get('role') in ('user', 'assistant') \
                    and isinstance(m.get('content'), str):
                mesajlar.append({'role': m['role'], 'content': m['content']})
        mesajlar.append({'role': 'user', 'content': mesaj})
        return mesajlar

    def _groq_istegi(self, mesajlar):
        """Groq API'ye istek atar. Ağ/HTTP hatalarını AIServiceError'a çevirir."""
        try:
            r = requests.post(
                GROQ_URL,
                headers={'Authorization': f'Bearer {self.api_key}',
                         'Content-Type': 'application/json'},
                json={'model': GROQ_MODEL, 'messages': mesajlar,
                      'temperature': 0.6, 'max_tokens': 400},
                timeout=20,
            )
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content'].strip()
        except (requests.RequestException, KeyError, IndexError, ValueError) as e:
            raise AIServiceError(f'Yapay zeka servisine ulasilamadi: {e}')

    def yanit_uret(self, mesaj, gecmis=None):
        """Dışarıya açılan tek metot."""
        # Anahtar yoksa çökmek yerine demo modu
        if not self.api_key:
            return '[Demo modu] GROQ_API_KEY tanimli degil. Mesajiniz alindi: ' + mesaj
        return self._groq_istegi(self._mesajlari_hazirla(mesaj, gecmis))


# Tek örnek: her yerde `from app.services.ai_service import ai_service`
ai_service = AIService()
