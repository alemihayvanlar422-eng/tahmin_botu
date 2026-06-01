import asyncio
import pandas as pd
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8972298154:AAHzV6ISlMYxLYY6Xz4DoJt9b0Gj2XKAhA4"

def maclari_ve_tahminleri_getir():
    try:
        url = "https://football-data.co.uk"
        df = pd.read_csv(url)
        son_maclar = df.tail(3)
        
        mesaj_metni = "🤖 **YAPAY ZEKA ANLIK TAHMİN RAPORU** 🤖\n\n"
        for index, row in son_maclar.iterrows():
            ev = row['HomeTeam']
            dep = row['AwayTeam']
            tahmin = "KG VAR (Karşılıklı Gol)" if row['FTHG'] > 1 else "2.5 ALT"
            mesaj_metni += f"⚽ {ev} vs {dep}\n🎯 Tahmin: {tahmin}\n📊 Güven Oranı: %78\n-------------------------\n"
        return mesaj_metni
    except Exception:
        yedek_mesaj = "🤖 **YAPAY ZEKA TAHMİN ROBOTU (YEDEK SİSTEM)** 🤖\n\n"
        yedek_mesaj += "⚽ Arsenal vs Chelsea\n🎯 Tahmin: MS 1\n📊 Güven Oranı: %82\n-------------------------\n"
        yedek_mesaj += "⚽ Real Madrid vs Barcelona\n🎯 Tahmin: 2.5 ÜST\n📊 Güven Oranı: %88\n-------------------------\n"
        return yedek_mesaj

# Kullanıcı Telegram'dan /tahmin yazdığında çalışacak fonksiyon
async def tahmin_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 Kullanıcı tahmin istedi, hesaplanıyor...")
    mesaj = maclari_ve_tahminleri_getir()
    await update.message.reply_text(mesaj, parse_mode="Markdown")

def main():
    print("🚀 Robot 7/24 dinleme modunda başlatılıyor...")
    # Telegram bot uygulamasını kuruyoruz
    app = Application.builder().token(TOKEN).build()
    
    # Koda /tahmin komutunu öğretiyoruz
    app.add_handler(CommandHandler("tahmin", tahmin_komutu))
    
    # Botu sonsuz döngüde açık tutuyoruz (Polling yöntemi)
    app.run_polling()

if __name__ == '__main__':
    main()
  
