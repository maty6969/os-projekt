#!/usr/bin/env python
"""
Skript pro kontrolu obsahu databáze guestbook
Zobrazí obsah tabulek Users a Messages
"""

import sqlite3
from pathlib import Path

# Cesta k databázi
db_path = Path(__file__).parent / 'instance' / 'guestbook.db'

print("=" * 70)
print("📊 KONTROLA DATABÁZE - Kniha návštěv")
print("=" * 70)
print(f"\n📍 Databáze: {db_path}")
print(f"✅ Databáze existuje: {db_path.exists()}")

if not db_path.exists():
    print("\n❌ Databáze neexistuje! Nejdřív spusťte aplikaci: python run.py")
    exit(1)

# Připojení k databázi
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "=" * 70)
print("📋 TABULKA: USERS (Autoři)")
print("=" * 70)

try:
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    if users:
        print(f"\n✅ Počet uživatelů: {len(users)}\n")
        print(f"{'ID':<5} {'JMÉNO':<20} {'EMAIL':<30} {'VYTVOŘENO':<20}")
        print("-" * 75)
        
        for user in users:
            print(f"{user['id']:<5} {user['name']:<20} {user['email']:<30} {user['created_at']:<20}")
    else:
        print("\n❌ Tabulka je prázdná - zatím žádní uživatelé!")
        
except Exception as e:
    print(f"\n❌ Chyba při čtení tabulky users: {e}")

print("\n" + "=" * 70)
print("📋 TABULKA: MESSAGES (Zprávy)")
print("=" * 70)

try:
    cursor.execute("""
        SELECT 
            m.id,
            m.user_id,
            u.name as user_name,
            u.email,
            m.message,
            m.created_at
        FROM messages m
        JOIN users u ON m.user_id = u.id
        ORDER BY m.created_at DESC
    """)
    messages = cursor.fetchall()
    
    if messages:
        print(f"\n✅ Počet zpráv: {len(messages)}\n")
        
        for i, msg in enumerate(messages, 1):
            print(f"{'─' * 70}")
            print(f"📝 Zpráva #{msg['id']} | Autor: {msg['user_name']} ({msg['email']})")
            print(f"⏰ Čas: {msg['created_at']}")
            print(f"💬 Text: {msg['message'][:100]}{'...' if len(msg['message']) > 100 else ''}")
            
    else:
        print("\n❌ Tabulka je prázdná - zatím žádné zprávy!")
        
except Exception as e:
    print(f"\n❌ Chyba při čtení tabulky messages: {e}")

# Statistika
print("\n" + "=" * 70)
print("📊 STATISTIKA")
print("=" * 70)

try:
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM messages")
    msg_count = cursor.fetchone()['count']
    
    print(f"\n👥 Celkem uživatelů: {user_count}")
    print(f"💬 Celkem zpráv: {msg_count}")
    
    if user_count > 0:
        print(f"📈 Průměr zpráv na uživatele: {msg_count / user_count:.2f}")
        
except Exception as e:
    print(f"\n❌ Chyba při výpočtu statistiky: {e}")

print("\n" + "=" * 70)
print("✅ Kontrola databáze hotova!")
print("=" * 70)

conn.close()
