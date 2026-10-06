# app/database.py — SQL YALNIZCA bu dosyada.
import sqlite3
from flask import current_app


def get_db():
    """Veritabanına bağlanır. row_factory sayesinde satırlara sütun adıyla erişilir."""
    conn = sqlite3.connect(current_app.config['DATABASE_URL'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db(app):
    """'leads' tablosunu yoksa oluşturur."""
    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                isim    TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj   TEXT,
                tarih   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()


def lead_ekle(isim, telefon, mesaj=''):
    """Yeni lead ekler. '?' yer tutucusu SQL Injection'ı engeller:
    değerler SQL metnine eklenmez, sürücü tarafından ayrıca (veri olarak) gönderilir."""
    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
            (isim, telefon, mesaj),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def tum_leadler():
    """Tüm lead'leri en yeniden eskiye döndürür (sözlük listesi olarak)."""
    conn = get_db()
    try:
        satirlar = conn.execute(
            "SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY id DESC"
        ).fetchall()
        # sqlite3.Row -> dict: JSON'a çevrilebilsin diye
        return [dict(s) for s in satirlar]
    finally:
        conn.close()
