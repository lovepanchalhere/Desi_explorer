# 🌾 Desi Explorer (देसी Explorer)
### AI-Powered Local Tourism Guide for Haryana's Heritage & Hidden Gems

> **"Uncover Haryana beyond the highway."** Built for tourists who want authentic cultural depth, sacred lore, verified history, mouth-watering local tastes, and guaranteed secret spots in **Karnal, Kurukshetra, Panipat, Pinjore, and Mullana/Ambala**.

---

## 📌 Problem It Solves

Most tourists traveling through Haryana stick strictly to GT Road highway dhabas or 1-2 generic spots (like Brahma Sarovar or Pinjore Gardens) before moving on. They face:
1. **Information Gaps**: Historical context is fragmented; oral traditions and deeper meanings behind monuments are hard to find.
2. **Hidden Gems Stay Undiscovered**: Incredible architectural wonders like *Sheikh Chilli's Tomb* (Haryana's Taj Mahal), *Bhima Devi Temple* (North India's Khajuraho), *Tarain Battlefield Fort*, or *Cantonment Church Tower* are routinely bypassed.
3. **Generic Itineraries**: Mainstream travel apps suggest generic North Indian food instead of authentic Haryanvi dishes (like *Bajra Roti with fresh white butter & jaggery*, *Kachri ki chutney*, or *Panipat Baoli Kadhi Kachori*).

---

## 💡 Solution: Desi Explorer

**Desi Explorer** is a zero-friction, bilingual (English & Hindi) single-page AI tourism application grounded in an authentic dataset of 22 verified historical and cultural spots across 5 key Haryana districts.

- **Personalized Time & Budget Routing**: Generates sequential, travel-optimized routes for quick 2-hour sprints, half-day trips, or full-day cultural immersions.
- **100% Guaranteed Hidden Gem**: Every single plan is guaranteed to include at least one lesser-known local treasure with its cultural context.
- **Authentic Culinary Pairings**: Recommends real traditional dishes and iconic dhabas/halwais near each stop.
- **"Chacha Desi" Local Guide Chat**: A grounded conversational guide that answers questions about entry fees, visiting hours, history, and secret lore without hallucinations.
- **Zero-Failure Architecture**: Uses Google Gemini 2.0 Flash with a robust, rule-based fallback knowledge engine so the app **never breaks** even without an API key or when offline.

---

## 🚀 Core Features

| Feature | Description |
| :--- | :--- |
| **🧭 Cultural Planner Form** | Filter by city (*Karnal, Kurukshetra, Panipat, Pinjore, Mullana/Ambala, or All*), time (*2 hrs, half day, full day*), interests (*Heritage, Spiritual, Food, Nature*), and budget (*Low, Medium, High*). |
| **⏱️ Sequential AI Itinerary** | Realistic time slots, logical travel order, and highlighted **Hidden Gem** badge with warm amber glow. |
| **📜 3-Line Cultural Lore** | Exactly 3 punchy, factual lines detailing the historical origin, architectural wonder, and cultural relevance for every stop. |
| **⭐ "Why It Matters"** | Concise takeaway explaining the living significance of the site. |
| **🗺️ One-Click Google Maps** | Direct link formatted as `https://www.google.com/maps/search/?api=1&query=PLACE+NAME` for instant GPS navigation. |
| **🍲 Local Food Picks** | Real traditional food pairings (e.g., *Kurukshetra Rabri & Khurchan Peda*, *Panipat Pachranga Achaar & Paratha*, *Ambala Cantt Kali Mirch Chaat*). |
| **👳‍♂️ "Ask the Local Guide" Chat** | Conversational chat grounded strictly in verified places data, featuring one-click suggestion pills and "Ask about this stop" deep-links. |
| **🇮🇳 Hindi / English Toggle** | Instant live bilingual toggle for all UI elements, labels, buttons, stop details, and guide replies. |

---

## 🛠️ Tech Stack

- **Backend**: Python 3 standard library (`http.server.ThreadingHTTPServer`, `urllib.request`, `json`, `os`, `re`).
  - *Zero pip dependencies needed!* Runs instantly on any machine with Python 3 installed.
- **Frontend**: Vanilla HTML5, modern CSS3 (Custom Properties, Flexbox, CSS Grid), Vanilla ES6+ JavaScript.
  - Saffron & Green theme (`#E65100` / `#1B5E20`) inspired by Haryana's agrarian and spiritual heritage.
- **AI Engine**: Groq API (`https://api.groq.com/openai/v1/chat/completions`, model `llama-3.3-70b-versatile`).
- **Data Engine**: Curated JSON repository (`data/places.json`) containing 22 verified locations with bilingual attributes, GPS coordinates, timings, and culinary pairings.

---

## 🤖 How AI Is Used

1. **Context-Grounded Itinerary Synthesis**:
   - The user's preferences (city, duration, interests, budget, language) are converted into a structured prompt.
   - Only matching candidate places from `data/places.json` are passed into the Groq prompt as strict context.
   - The model is instructed to output strictly valid JSON matching the itinerary schema, enforcing the rule to include at least one hidden gem.
2. **Grounded Conversational Guide**:
   - When asking "Chacha Desi", the prompt feeds factual attributes from the verified places dataset.
   - Zero hallucination policy: the model is explicitly instructed to never invent non-existent places or false dates.
3. **Resilient Dual-Engine Fallback**:
   - If `GROQ_API_KEY` is absent, quota is exceeded, or offline, the application seamlessly delegates to the built-in deterministic scoring algorithm in `engine.py`.
   - The UI displays an indicator showing whether Groq AI or the Grounded Knowledge Base generated the response.

---

## 📂 Project Structure

```text
Hacksprint/
├── data/
│   └── places.json          # 22 verified places across 5 Haryana cities
├── static/
│   ├── index.html           # Single-page bilingual frontend
│   ├── styles.css           # Saffron/Green themed responsive styles
│   └── app.js               # Bilingual UI logic, itinerary renderer & chat
├── engine.py                # Itinerary generator, Groq caller & fallback logic
├── server.py                # Zero-dependency HTTP & REST API server
├── test_suite.py            # Automated unit and integration test suite
├── .env.example             # Template for API keys
├── .env                     # Local environment variables (git-ignored)
├── .gitignore               # Excludes secrets, bytecode, and temp files
└── README.md                # Documentation & quickstart
```

---

## ⚡ Quickstart: Setup & Run Locally

### 1. Prerequisites
- Python 3.8+ (No external pip packages required!).

### 2. Configure Groq API Key
To enable live Groq AI generation:
1. Open `.env` (or copy `.env.example` to `.env`):
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   PORT=5000
   ```
2. *Note*: If no Groq API key is provided, the app runs on the built-in grounded knowledge engine. You can also paste your key directly into the UI via the **"AI Engine"** button in the top navigation.

### 3. Run the Server
From the project root directory, run:

```bash
python server.py
```

### 4. Open in Browser
Visit:
```text
http://127.0.0.1:5000/
```

---

## 🧪 Running the Automated Test Suite

To verify the dataset, bilingual itinerary rules, hidden gem constraints, and grounded chat responses:

```bash
python test_suite.py
```

Expected output:
```text
=== ALL UNIT & INTEGRATION TESTS PASSED 100%! ===
```

---

## 🏛️ Verified Cultural Coverage

- **Kurukshetra**: Brahma Sarovar, Jyotisar (Birthplace of Gita), Sheikh Chilli's Tomb (Hidden Gem), Dharohar Folk Museum (Hidden Gem), Shri Devikoop Bhadrakali Shaktipeeth.
- **Karnal**: Karna Lake, Cantonment Church Tower (Hidden Gem), Kalandar Shah's Tomb (Hidden Gem), Taraori Fort / Tarain Battlefield (Hidden Gem).
- **Panipat**: Kabuli Bagh Mosque (Babur, 1526), Kala Amb War Memorial (1761), Ibrahim Lodi's Tomb (Hidden Gem), Salar Ganj Gate (Hidden Gem), Dargah Bu-Ali Shah Qalandar.
- **Pinjore**: Yadavindra Gardens (Pinjore Terraced Gardens), Bhima Devi Temple Complex (North India's Khajuraho - Hidden Gem), Kaushalya Dam & Wetland (Hidden Gem).
- **Mullana / Ambala**: Rani Ka Talab & Patel Park, Holy Redeemer Church (1848 - Hidden Gem), Gurudwara Panjokhra Sahib, Medieval Kos Minar (Hidden Gem), Cloth Market & Purani Mandi (Hidden Gem).

