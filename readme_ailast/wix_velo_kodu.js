// ====== WIX VELO ======
// Wix'te: Dev Mode'u aç. Aşağıdaki API adresini Render adresinle değiştir.
import { fetch } from 'wix-fetch';
const API = 'https://SENIN-UYGULAMAN.onrender.com';

// ---------- 1) KARŞILAMA SAYFASI ----------
// Elementler ID'leri: #mesajInput, #sorBtn, #yanitText, #isimInput, #telefonInput, #kaydetBtn, #durumText
const gecmis = [];

$w.onReady(function () {
  $w('#sorBtn').onClick(async () => {
    const mesaj = $w('#mesajInput').value.trim();
    if (!mesaj) return;
    try {
      const r = await fetch(`${API}/api/sohbet`, {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mesaj, gecmis })
      });
      const d = await r.json();
      if (d.basari) {
        gecmis.push({ role: 'user', content: mesaj }, { role: 'assistant', content: d.cevap });
        $w('#yanitText').text = d.cevap;
      } else {
        $w('#yanitText').text = d.hata;
      }
    } catch (e) { $w('#yanitText').text = 'Baglanti hatasi'; }
  });

  $w('#kaydetBtn').onClick(async () => {
    try {
      const r = await fetch(`${API}/api/leads`, {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          isim: $w('#isimInput').value,
          telefon: $w('#telefonInput').value,
          mesaj: gecmis.filter(m => m.role === 'user').map(m => m.content).join(' | ')
        })
      });
      const d = await r.json();
      $w('#durumText').text = d.basari ? 'Kaydedildi' : d.hata;
    } catch (e) { $w('#durumText').text = 'Baglanti hatasi'; }
  });
});

// ---------- 2) YÖNETİM PANELİ ----------
// Repeater ID: #leadRepeater ; içindeki metinler: #isimText, #telefonText, #tarihText
/*
$w.onReady(async function () {
  const r = await fetch(`${API}/api/leads`, { method: 'get' });
  const d = await r.json();
  if (d.basari) {
    $w('#leadRepeater').data = d.leadler;           // her objede _id var
    $w('#leadRepeater').onItemReady(($item, itemData) => {
      $item('#isimText').text = itemData.isim;       // en önemli kolon solda
      $item('#telefonText').text = itemData.telefon;
      $item('#tarihText').text = itemData.tarih;
    });
  }
});
*/
