# 📘 AI Simulated Lab Partner — Product Requirement Document (PRD)

## 🎯 Product Vision
Her öğrencinin, fizik/kimya/biyoloji deneylerini gerçek bir partnerle yapıyormuş gibi yaşayabileceği,  
multi-agent + Wolfram destekli interaktif deney simülasyon sistemi.

**Amaç:** Evde, düşük imkanlarda bile gerçek laboratuvar öğrenimi deneyimini yeniden üretmek.

---

## 🧪 Core Features

### 1) AI Lab Partner (Primary Agent)
- Öğrenciyle konuşur, tartışır, hata yapar, birlikte çözüm üretir.  
- “İnsan partner” hissi verir.  
- **Kişilik:** meraklı, hafif sabırsız, motive edici.  
- Duruma göre:  
  - Fikir verir  
  - Yanlış şeyi savunur (öğrenci yanlışları fark etsin)  
  - Birlikte deney planı çıkarır  

### 2) Mentor Agent (Overseer)
- Partner’in ve öğrencinin konuşmalarını değerlendirir.  
- Yanlış kavramları tespit eder.  
- Öğrenciye küçük ipuçları verir.  
- Gerektiğinde düzeltir.  

### 3) Experiment Engine (Wolfram Core)
- Her deney için:  
  - Hesaplamalar  
  - Grafikler (pH, hız, enerji, momentum, sıcaklık vb.)  
  - Simülasyon sonuçları  
  - Deney parametreleri değiştiğinde anında sonuç üretme  

### 4) Scenario System
- Öğrenci bir deney seçer → sistem dinamik senaryo oluşturur.  
- Örnek:  
  - Kimya: Asit-Baz titrasyonu  
  - Fizik: Yay sabiti ölçümü  
  - Biyoloji: Hücre zarından madde geçişi simülasyonu  

---

## 🌍 Why This Project Wins?
- Eğitimsel etki: yüksek  
- Eğlenceli → öğrenciyi içine çeker  
- Teknik derinlik: multi-agent + Wolfram computation  
- UX: oyun gibi  
- Yenilik: gerçek partner simülasyonu  
- Accessibility: evde laboratuvarı olmayan öğrenciler için birebir  

---

# 📘 README.md

## 🧪 AI Simulated Lab Partner
Your personal interactive science lab buddy — built with OpenAI, Wolfram, Cline CLI, GitBook

### 🚀 Overview
AI Simulated Lab Partner, fizik/kimya/biyoloji deneylerini gerçek bir partnerle çalışıyormuş gibi interaktif şekilde yapmanı sağlayan bir eğitim aracıdır.  
Sistem; multi-agent mimarisi, Wolfram real-time computation, Cline CLI otomasyon pipeline ve GitBook dynamic documentation üzerine kuruludur.

### ✨ Features
- 🧍 **AI Lab Partner** – tartışır, hata yapar, fikir üretir  
- 🧠 **Mentor Agent** – rehberlik eder, yanlışları düzeltir  
- 🔬 **Wolfram Simulation Engine** – grafik, hesaplama, deney sonuçları  
- 📚 **Dynamic GitBook** – her deney GitBook üzerinde otomatik oluşturulur  
- 🔧 **Cline CLI Workflow** – senaryo dosyalarından otomatik içerik üretir  
- 🎮 **Interactive Experience** – gerçek partner gibi tepki veren sistem  

### 🛠 Tech Stack

| Teknoloji | Kullanım |
|-----------|---------|
| OpenAI GPT-4.2/5 Agents | Partner, Mentor, Evaluator |
| Wolfram Cloud | Gerçek zamanlı deney hesaplama & grafik |
| Cline CLI | Scenario → Agents → GitBook pipeline |
| GitBook API | Dinamik dokümantasyon |
| FastAPI | Backend & agent routing |
| Claude / Gemini | Alternatif reasoning agents |

### 🏗 Installation
```bash
git clone <repo>
cd ai-lab-partner
pip install -r requirements.txt
cp .env.example .env
# OPENAI_API_KEY, WOLFRAM_APPID doldur
uvicorn app:server --reload
```
📐 System Architecture
             +--------------------+
             |   GitBook Client   |
             +--------------------+
                      |
                      v
------------------------------------------------------
|                     API Server                     |
|  (FastAPI + Router + Webhooks)                     |
------------------------------------------------------
   |                 |                   |
   v                 v                   v
Partner Agent   Mentor Agent       Evaluator Agent
   |                 |                   |
   ----------- Multi-Agent Layer ---------
                      |
                      v
             Wolfram Compute Engine
                      |
                      v
           Experiment Simulation Output


# 📘 Tech Stack & Why

### OpenAI Agents
- İnsan partner davranışını en iyi taklit eden sistem

### Wolfram
- Sayısal doğruluk  
- Grafik üretimi  
- Formül bazlı deney simülasyonu

### Cline CLI
- Tek komutla GitBook + senaryo + agent pipeline çalıştırma

### GitBook
- Öğrenci deneylerinin otomatik olarak dokümante edilmesi  
- Eğitim platformu oluşturma

---

# 📘 API SPEC

## POST /simulate
Senaryo başlatır.

**Body:**
```json
{
  "experiment": "acid_base_titration",
  "level": "beginner"
}
```
Response:
```json
{
  "partner": "Bugün titrasyon yapıyoruz!",
  "mentor": "Önce neyi ölçmek istediğimizi belirleyelim.",
  "wolfram_graph": "<base64 svg>"
}
```

📘 Multi-Agent Tasarımı
Partner Agent
Persona: eğlenceli, konuşkan, hafif rekabetçi
Amaç: öğrenciyle birlikte karar vermek

Prompt:
You are an AI lab partner. You think like a human, talk like a student, and sometimes make mistakes to encourage discussion.

Mentor Agent
Her diyaloğu analiz eder
Partner + öğrenci etkileşimini değerlendirir
Gerektiğinde mini ders verir
Evaluator Agent
Öğrenci anladı mı?
Yanlış kavram varsa işaretler

📘 Wolfram Module
Example: Titrasyon
Plot[pH[x], {x,0,20}]

Example: Hooke’s Law
Plot[k x, {x,0,10}]

📘 GitBook Structure
/experiments
   /physics
      - hookes-law.md
   /chemistry
      - titration.md
   /biology
      - osmosis.md

Cline CLI her çalıştırmada otomatik güncelliyor:
cline build-experiment titration.scn

📘 Cline CLI Automation

Pipeline:
experiment.scn → agents → wolfram → markdown → GitBook push


Command:
cline run pipeline --scenario titration.scn

📘 Demo Script (Hakemlere)

Öğrenci: “Asit baz titrasyonu yapmak istiyorum.”
Partner: “Süper! İlk önce çözeltileri hazırlayalım mı?”
Mentor: “Önce amaç: asidin molaritesini bulmak.”
Öğrenci hacmi girer
Wolfram grafik çıkar
Partner grafiği yorumlar
GitBook’ta deney otomatik oluşturulur
Jüri: whoa effect

📘 Roadmap
Day-1 Deliverables (Hackathon için yeterli)
3 deney senaryosu
Partner + Mentor agent
Wolfram destekli grafik
GitBook dinamik sayfa
CLI pipeline

📘 Prompt Pack
Claude/GPT için dev prompt
You are the "AI Lab Partner System". You receive experiment scenarios and generate partner dialogue, mentor guidance and Wolfram computation instructions. Maintain personality. Encourage discussion. Avoid giving full solutions immediately.
