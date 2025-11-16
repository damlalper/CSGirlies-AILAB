# 🚀 Groq API Setup (ÜCRETSIZ!)

## Neden Groq?

- ✅ **TAMAMEN ÜCRETSIZ** - Kredi kartı gerekmez!
- ✅ **ÇOK HIZLI** - OpenAI'dan 10x daha hızlı yanıt
- ✅ **YÜKSEK LIMIT** - Günde binlerce istek
- ✅ **KOLAY SETUP** - 2 dakikada hazır

---

## 📝 Adım Adım Groq API Key Alma

### 1. Groq Hesabı Oluştur (1 dakika)

1. **Web sitesine git:** https://console.groq.com
2. **Sign Up tıkla**
3. **Email ile kaydol** (Google/GitHub da olur)
4. **Email doğrula**

### 2. API Key Oluştur (30 saniye)

1. Dashboard'a gir
2. Sol menüden **"API Keys"** tıkla
3. **"Create API Key"** tıkla
4. İsim ver (örn: "CSGirlies-AILAB")
5. **Key'i kopyala** (`gsk_...` ile başlar)

⚠️ **ÖNEMLİ:** Key'i kopyaladıktan sonra bir daha göremezsin!

### 3. Projede Ayarla (30 saniye)

```bash
# .env dosyasını oluştur
cp .env.example .env

# .env dosyasını düzenle
notepad .env
```

**.env içine şunu ekle:**
```env
AI_PROVIDER=groq
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Test Et

```bash
# Kurulum
python cline.py setup

# Health check
python cline.py health

# Sunucuyu başlat
python cline.py start
```

---

## 🎯 Groq vs OpenAI Karşılaştırması

| Özellik | Groq | OpenAI |
|---------|------|--------|
| **Fiyat** | 🟢 ÜCRETSIZ | 🔴 Ücretli ($0.01/1K token) |
| **Hız** | 🟢 Çok Hızlı (800 tokens/s) | 🟡 Orta (50 tokens/s) |
| **Limit** | 🟢 30 req/min ücretsiz | 🔴 Kredi gerekli |
| **Model** | Llama 3.1 70B | GPT-4 Turbo |
| **Kalite** | 🟢 Mükemmel | 🟢 Mükemmel |
| **Setup** | 🟢 Çok Kolay | 🟡 Kredi kartı gerekli |

---

## 🤖 Kullanılabilir Groq Modelleri

Projemiz şu modeli kullanıyor:
- **llama-3.1-70b-versatile** (Önerilen - En dengeli)

Diğer seçenekler (.env'de değiştirebilirsin):
```env
# Daha hızlı, daha kısa yanıtlar
GROQ_MODEL=llama-3.1-8b-instant

# Daha detaylı, daha uzun yanıtlar
GROQ_MODEL=llama-3.1-70b-versatile

# En güçlü (biraz daha yavaş)
GROQ_MODEL=llama-3.1-405b-reasoning
```

---

## 📊 Groq Ücretsiz Limitleri

**Günlük Limitler:**
- ✅ 14,400 istek/gün
- ✅ 30 istek/dakika
- ✅ 7,000 token/dakika

**Projemiz için yeterli mi?**
- Bir deney: ~10-15 istek
- 14,400 ÷ 15 = **960 deney/gün!**
- **EVET, bol bol yeterli!** 🎉

---

## 🔄 OpenAI'dan Groq'a Geçiş

Eğer OpenAI kullanıyorduysan:

1. **.env dosyasını düzenle:**
```env
# OpenAI'yı kapat
AI_PROVIDER=groq

# Groq key ekle
GROQ_API_KEY=gsk_xxxxxxxx
```

2. **Sunucuyu yeniden başlat:**
```bash
python cline.py start
```

**O kadar!** Kod değişikliği gerekmez. 🎉

---

## 🆘 Sorun Giderme

### Hata: "Invalid API Key"
```bash
# Key'i doğru kopyaladın mı kontrol et
# gsk_ ile başlamalı

# .env dosyasında tırnak işareti olmamalı
# YANLIŞ: GROQ_API_KEY="gsk_xxx"
# DOĞRU:  GROQ_API_KEY=gsk_xxx
```

### Hata: "Rate Limit Exceeded"
```bash
# Çok fazla istek atmışsın, 1 dakika bekle
# Veya .env'de model değiştir:
GROQ_MODEL=llama-3.1-8b-instant  # Daha hızlı, daha az limit
```

### Hata: "Connection Error"
```bash
# İnternet bağlantını kontrol et
# Groq sunucuları çalışıyor mu: https://status.groq.com
```

---

## 💡 İpuçları

### 1. Hız İçin Optimizasyon
```env
# En hızlı model
GROQ_MODEL=llama-3.1-8b-instant
```

### 2. Kalite İçin Optimizasyon
```env
# En kaliteli model
GROQ_MODEL=llama-3.1-70b-versatile
```

### 3. Her İkisini Dene
```bash
# Groq ile test et
AI_PROVIDER=groq
python cline.py start

# OpenAI ile karşılaştır (eğer key'in varsa)
AI_PROVIDER=openai
python cline.py start
```

---

## 🎓 Groq Hakkında

**Groq nedir?**
- Yapay zeka donanımı yapan şirket
- LPU (Language Processing Unit) teknolojisi
- Meta'nın Llama modellerini çalıştırıyor
- Araştırma ve eğitim için ücretsiz API

**Neden bu kadar hızlı?**
- Özel AI çipleri (LPU)
- Optimize edilmiş mimari
- GPU'dan 10x daha hızlı

---

## ✅ Tamamlandı Kontrolü

Groq doğru kuruldu mu kontrol et:

```bash
# 1. Health check
python cline.py health

# Çıktıda görmeli sin:
# [OK] AI Provider: groq
# [OK] Groq API Key configured

# 2. Hızlı test
python cline.py demo

# Eğer AI yanıtları geliyorsa: ✅ BAŞARILI!
```

---

## 📞 Yardım

**Groq Dökümanları:**
- https://console.groq.com/docs

**Groq Discord:**
- https://discord.gg/groq

**Bizim Projede Sorun:**
- GitHub Issues açabilirsin

---

**Başarılar!** 🚀

*Not: Groq, hackathon için MÜKEMMEL çünkü ücretsiz ve hızlı. Jüri test ederken kredi limitine takılmazsın!*
