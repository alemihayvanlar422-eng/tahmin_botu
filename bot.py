import asyncio
import os
import pandas as pd
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading


TOKEN = "8972298154:AAFH7Rf6cauKkXGNN0BAN1L-855Wn8Ntww0"

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Robot aktif ve calisiyor!")

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# --- YAPAY ZEKA VE İSTATİSTİKSEL ANALİZ MOTORU ---
def yapay_zeka_analiz_motoru():
    try:
        # Robot güncel İngiltere Premier Lig verilerini internetten canlı çekiyor
        url = "https://football-data.co.uk"
        df = pd.read_csv(url)
        
        # Boş istatistik tabloları oluşturuyoruz
        takimlar = {}
        
        # Robot geçmiş tüm maçları tek tek inceleyerek takımların karakterini analiz ediyor
        for index, row in df.iterrows():
            ev = row['HomeTeam']
            dep = row['AwayTeam']
            ev_gol = row['FTHG']
            dep_gol = row['FTAG']
            
            if ev not in takimlar: takimlar[ev] = {'atilan': 0, 'yenilen': 0, 'mac': 0}
            if dep not in takimlar: takimlar[dep] = {'atilan': 0, 'yenilen': 0, 'mac': 0}
            
            takimlar[ev]['atilan'] += ev_gol
            takimlar[ev]['yenilen'] += dep_gol
            takimlar[ev]['mac'] += 1
            
            takimlar[dep]['atilan'] += dep_gol
            takimlar[dep]['yenilen'] += ev_gol
            takimlar[dep]['mac'] += 1

        # Robot son oynanan 3 maçı alıp, gelecek maçlarmış gibi analiz simülasyonu yapıyor
        son_maclar = df.tail(3)
        mesaj_metni = "🧠 **PRO YAPAY ZEKA ANALİZ RAPORU** 🧠\n"
        mesaj_metni += "📊 *Lig geneli ve takım form durumları analiz edildi.*\n\n"
        
        for index, row in son_maclar.iterrows():
            ev = row['HomeTeam']
            dep = row['AwayTeam']
            
            # Takımların maç başına gol ortalamalarını hesaplıyoruz
            ev_ort_gol = takimlar[ev]['atilan'] / takimlar[ev]['mac']
            dep_ort_gol = takimlar[dep]['atilan'] / takimlar[dep]['mac']
            
            # MATEMATİKSEL TAHMİN FORMÜLÜ:
            # İki takımın gol ortalamalarının toplamı 2.8'den büyükse ÜST, değilse ALT tahmini üret
            toplam_gol_beklentisi = ev_ort_gol + dep_ort_gol
            
            if toplam_gol_beklentisi > 2.8:
                tahmin = "2.5 ÜST"
                # Güven oranını gol beklentisinin yüksekliğine göre dinamik hesaplıyoruz
                guven_orani = min(int(65 + (toplam_gol_beklentisi * 5)), 95)
            else:
                tahmin = "2.5 ALT"
                guven_orani = min(int(65 + ((3 - toplam_gol_beklentisi) * 8)), 93)
                
            mesaj_metni += f"⚽ **{ev} vs {dep}**\n"
            mesaj_metni += f"📈 Toplam Gol Trendi: {toplam_gol_beklentisi:.2f}\n"
            mesaj_metni += f"🎯 Yapay Zeka Tahmini: *{tahmin}*\n"
            mesaj_metni += f"📊 Güven Oranı: %{guven_orani}\n"
            mesaj_metni += "-------------------------\n"
            
        return mesaj_metni
        
    except Exception as e:
        # Eğer internette veya veride bir sorun olursa robot akıllı tahmin üretemezse bu yedek devreye girer
        return "⚠️ Canlı veriler işlenirken hata oluştu! Lütfen daha sonra tekrar deneyin."

async def tahmin_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 Kullanıcı akıllı tahmin istedi, hesaplanıyor...")
    mesaj = yapay_zeka_analiz_motoru()
    await update.message.reply_text(mesaj, parse_mode="Markdown")

def main():
    print("🚀 Sahte web sunucusu baslatiliyor...")
    threading.Thread(target=start_health_server, daemon=True).start()
    
    print("🚀 Robot 7/24 dinleme modunda başlatılıyor...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("tahmin", tahmin_komutu))
    app.run_polling()

if __name__ == '__main__':
    main()
            
