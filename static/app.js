/**
 * Desi Explorer - Frontend Application Script
 * Full bilingual support (English & Hindi)
 * Real-time itinerary generation, chat, and place exploration.
 */

// Bilingual Translation Dictionary
const I18N = {
  en: {
    tagline: "AI-Powered Haryana Tourism & Hidden Gems Guide",
    statsText: "22 Verified Places | 5 Cities",
    aiStatusBtn: "AI Engine",
    heroTag: "✨ Discover Real Haryana",
    heroTitle: "Uncover Ancient History, Sacred Sarovars & Hidden Gems",
    heroDesc: "Tourists often only rush past GT Road highways and miss profound cultural landmarks. Desi Explorer crafts an authentic, grounded travel plan with verified local folklore, sacred history, must-try Haryanvi dishes, and guaranteed secret spots.",
    plannerHeading: "Trip Planner",
    plannerSub: "Personalize your Haryana cultural journey",
    labelCity: "Destination City / Area",
    labelTime: "Time Available",
    optTime2hr: "2 Hours",
    optTimeHalf: "Half Day",
    optTimeFull: "Full Day",
    labelInterests: "Interests (Select multiple)",
    optHeritage: "Heritage",
    optSpiritual: "Spiritual",
    optFood: "Food",
    optNature: "Nature",
    labelBudget: "Budget Level",
    optBudgetLow: "Budget / Free",
    optBudgetMid: "Standard",
    optBudgetHigh: "Comfort",
    hiddenGemGuarantee: "Every route is guaranteed to include at least 1 lesser-known Hidden Gem!",
    btnPlanRoute: "Generate AI Itinerary",
    loadingTitle: "Curating Your Haryana Itinerary...",
    loadingSub: "Filtering authentic monuments, secret spots, and heritage dhabas...",
    guideName: "Chacha Desi | Local Haryana Guide",
    guideStatus: "Grounded in verified historical facts & oral lore",
    chatPlaceholder: "Ask about any place, visiting hours, history, or local food...",
    btnSend: "Ask",
    settingsTitle: "Groq AI Settings",
    settingsDesc: "Desi Explorer uses Groq (llama-3.3-70b-versatile) for live itinerary synthesis. If no key is set, our built-in grounded rule-based engine powers itineraries and chat seamlessly without breaking!",
    labelApiKey: "Groq API Key",
    apiKeyHint: "Stored only in your local session or configured in .env file.",
    btnCancel: "Cancel",
    btnSaveKey: "Save & Connect",
    footerSub: "Curated strictly from verified historical monuments & traditional culinary archives across Karnal, Kurukshetra, Panipat, Pinjore, and Mullana/Ambala.",
    stopLabel: "Stop",
    hiddenGemBadge: "✨ Lesser-Known Hidden Gem",
    whyItMatters: "Why It Matters",
    threeLineStory: "3-Line Cultural Lore",
    foodBadge: "Traditional Taste Near This Stop",
    btnMaps: "Open in Google Maps",
    btnAskGuide: "Ask Guide About This",
    hoursLabel: "Hours",
    entryLabel: "Entry",
    bestTimeLabel: "Best Time",
    sourceAi: "Powered by Groq (Llama 3.3 70B)",
    sourceFallback: "Verified Local Grounded Engine",
    guideWelcome: "Ram Ram ji! I am Chacha Desi, your native guide for Haryana. Ask me anything about Karnal, Kurukshetra, Panipat, Pinjore, or Mullana/Ambala — historical folklore, entry timings, or where to get authentic Bajra Roti and Rabri!",
    prompts: [
      "What is special about Sheikh Chilli's tomb in Kurukshetra?",
      "Where can I get authentic Bajra Roti & Makhan?",
      "Tell me about the First Battle of Panipat at Kabuli Bagh",
      "Why is Bhima Devi Temple called North India's Khajuraho?",
      "Is Brahma Sarovar accessible early morning?"
    ]
  },
  hi: {
    tagline: "हरियाणा का एआई-संचालित पर्यटन व छिपे हुए रत्नों का मार्गदर्शक",
    statsText: "22 प्रामाणिक स्थल | 5 ऐतिहासिक शहर",
    aiStatusBtn: "एआई इंजन",
    heroTag: "✨ असली हरियाणा की खोज",
    heroTitle: "प्राचीन इतिहास, पवित्र सरोवर और अनदेखे रत्नों का सफर",
    heroDesc: "अक्सर पर्यटक जीटी रोड हाईवे से तेजी से गुजर जाते हैं और हरियाणा की असीम सांस्कृतिक धरोहर से वंचित रह जाते हैं। देसी एक्सप्लोरर आपके लिए प्रामाणिक इतिहास, लोक कथाओं, पारंपरिक हरियाणवी खान-पान और अनदेखे 'Hidden Gems' से भरपूर योजना तैयार करता है।",
    plannerHeading: "यात्रा योजक (Planner)",
    plannerSub: "अपनी रुचि के अनुसार हरियाणा भ्रमण मार्ग तैयार करें",
    labelCity: "गंतव्य शहर / क्षेत्र",
    labelTime: "उपलब्ध समय",
    optTime2hr: "2 घंटे",
    optTimeHalf: "आधा दिन (4-5 घंटे)",
    optTimeFull: "पूरा दिन (8 घंटे)",
    labelInterests: "आपकी रुचि (एक या अधिक चुनें)",
    optHeritage: "ऐतिहासिक",
    optSpiritual: "धार्मिक",
    optFood: "खानपान",
    optNature: "प्रकृति",
    labelBudget: "बजट स्तर",
    optBudgetLow: "बजट / निःशुल्क",
    optBudgetMid: "मध्यम",
    optBudgetHigh: "सुविधाजनक",
    hiddenGemGuarantee: "प्रत्येक योजना में कम से कम 1 अनदेखा 'छिपा हुआ रत्न' (Hidden Gem) अवश्य शामिल रहेगा!",
    btnPlanRoute: "मेरी एआई यात्रा योजना बनाएं",
    loadingTitle: "आपकी हरियाणा यात्रा तैयार हो रही है...",
    loadingSub: "प्रामाणिक ऐतिहासिक स्थलों, गुप्त विरासतों और ढाबों का चयन किया जा रहा है...",
    guideName: "चाचा देसी | हरियाणवी स्थानीय गाइड",
    guideStatus: "प्रामाणिक ऐतिहासिक तथ्यों एवं लोक परंपराओं पर आधारित",
    chatPlaceholder: "किसी भी स्थल, इतिहास, समय या पारंपरिक खान-पान के बारे में पूछें...",
    btnSend: "पूछें",
    settingsTitle: "ग्रॉक एआई सेटिंग्स",
    settingsDesc: "देसी एक्सप्लोरर त्वरित यात्रा योजना निर्माण हेतु ग्रॉक (Llama 3.3 70B) का उपयोग करता है। यदि कुंजी उपलब्ध नहीं है, तो भी हमारा स्थानीय ज्ञान इंजन बिना रुके कार्य करता है!",
    labelApiKey: "ग्रॉक एपीआई कुंजी (Groq API Key)",
    apiKeyHint: "केवल आपके स्थानीय सत्र में सुरक्षित अथवा .env फ़ाइल में सहेजी जाती है।",
    btnCancel: "रद्द करें",
    btnSaveKey: "सहेजें और जोड़ें",
    footerSub: "करनाल, कुरुक्षेत्र, पानीपत, पिंजौर एवं मुलाना/अंबाला के ऐतिहासिक अभिलेखों व पारंपरिक व्यंजनों से संकलित।",
    stopLabel: "पड़ाव",
    hiddenGemBadge: "✨ कम चर्चित गुप्त रत्न (Hidden Gem)",
    whyItMatters: "यह क्यों विशेष है?",
    threeLineStory: "3-पंक्तियों में इतिहास व संस्कृति",
    foodBadge: "इस पड़ाव के पास का पारंपरिक स्वाद",
    btnMaps: "गूगल मैप्स पर देखें",
    btnAskGuide: "गाइड से इसके बारे में पूछें",
    hoursLabel: "समय",
    entryLabel: "प्रवेश शुल्क",
    bestTimeLabel: "उत्तम समय",
    sourceAi: "ग्रॉक (Llama 3.3 70B) द्वारा संचालित",
    sourceFallback: "प्रामाणिक स्थानीय ज्ञान इंजन",
    guideWelcome: "राम-राम जी! मैं चाचा देसी, हरियाणा का आपका स्थानीय मार्गदर्शक हूँ। करनाल, कुरुक्षेत्र, पानीपत, पिंजौर या मुलाना/अंबाला के इतिहास, दर्शन समय या असली बाजरे की रोटी व रबड़ी के बारे में मुझसे बेझिझक पूछें!",
    prompts: [
      "कुरुक्षेत्र में शेख चिल्ली के मकबरे की क्या खासियत है?",
      "असली बाजरा रोटी और देशी मक्खन कहाँ मिलेगा?",
      "पानीपत की पहली लड़ाई और काबुली बाग मस्जिद का इतिहास बताइए",
      "पिंजौर के भीमा देवी मंदिर को उत्तर भारत का खजुराहो क्यों कहते हैं?",
      "क्या ब्रह्म सरोवर सुबह जल्दी दर्शन के लिए खुला रहता है?"
    ]
  }
};

// Global App State
const state = {
  lang: "en",
  city: "Kurukshetra",
  time_available: "half_day",
  interests: ["heritage", "spiritual"],
  budget: "low",
  apiKey: sessionStorage.getItem("desi_groq_api_key") || "",
  currentItinerary: null,
  chatHistory: []
};

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
  applyLanguage(state.lang);
  checkBackendHealth();
  // Generate initial default itinerary on page load
  loadItinerary();
});

// Check Server Health
async function checkBackendHealth() {
  try {
    const res = await fetch("/api/health");
    const data = await res.json();
    const dot = document.getElementById("keyStatusDot");
    if (dot) {
      if (data.groq_configured || data.ai_configured || data.gemini_configured || state.apiKey) {
        dot.style.backgroundColor = "#10B981";
        dot.title = "Groq Llama 3.3 70B Active";
      } else {
        dot.style.backgroundColor = "#F59E0B";
        dot.title = "Rule-based Grounded Engine Active (Add Groq key to enable AI)";
      }
    }
  } catch (err) {
    console.warn("Health check error:", err);
  }
}

// Language Switching
function setLanguage(lang) {
  if (state.lang === lang) return;
  state.lang = lang;

  document.getElementById("btnLangEn").classList.toggle("active", lang === "en");
  document.getElementById("btnLangHi").classList.toggle("active", lang === "hi");

  applyLanguage(lang);
  // Re-fetch current itinerary in new language
  loadItinerary();
}

function applyLanguage(lang) {
  const dict = I18N[lang] || I18N.en;

  // Update text nodes with data-i18n
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  // Update placeholders
  document.querySelectorAll("[data-i18n-ph]").forEach(el => {
    const key = el.getAttribute("data-i18n-ph");
    if (dict[key]) {
      el.placeholder = dict[key];
    }
  });

  // Update quick prompts
  renderQuickPrompts(dict.prompts);

  // If chat is empty, show welcome message
  if (state.chatHistory.length === 0) {
    renderWelcomeChatMessage(dict.guideWelcome);
  }
}

// Quick Prompts Rendering
function renderQuickPrompts(prompts) {
  const container = document.getElementById("quickPromptsRow");
  if (!container) return;
  container.innerHTML = prompts.map(p => `
    <button type="button" class="quick-prompt-pill" onclick="handleQuickPromptClick('${escapeHtml(p)}')">
      💡 ${escapeHtml(p)}
    </button>
  `).join("");
}

function handleQuickPromptClick(text) {
  const input = document.getElementById("chatInput");
  if (input) {
    input.value = text;
    sendChatMessage(text);
  }
}

function renderWelcomeChatMessage(welcomeText) {
  const container = document.getElementById("chatMessages");
  if (!container) return;
  container.innerHTML = `
    <div class="chat-bubble guide">
      <strong>👳‍♂️ Chacha Desi:</strong><br>
      ${welcomeText}
    </div>
  `;
}

// Form Option Toggles
function selectTimeOption(val) {
  state.time_available = val;
  document.querySelectorAll("#timeGrid .option-btn").forEach(el => {
    el.classList.toggle("selected", el.getAttribute("data-value") === val);
  });
}

function toggleInterestOption(val) {
  const idx = state.interests.indexOf(val);
  if (idx > -1) {
    if (state.interests.length > 1) { // keep at least 1 interest
      state.interests.splice(idx, 1);
    }
  } else {
    state.interests.push(val);
  }
  document.querySelectorAll("#interestGrid .option-btn").forEach(el => {
    const v = el.getAttribute("data-value");
    el.classList.toggle("selected", state.interests.includes(v));
  });
}

function selectBudgetOption(val) {
  state.budget = val;
  document.querySelectorAll("#budgetGrid .option-btn").forEach(el => {
    el.classList.toggle("selected", el.getAttribute("data-value") === val);
  });
}

function handleFormSubmit(e) {
  if (e) e.preventDefault();
  const citySelect = document.getElementById("citySelect");
  if (citySelect) {
    state.city = citySelect.value;
  }
  loadItinerary();
}

// Fetch and Render Itinerary
async function loadItinerary() {
  const loadingBox = document.getElementById("loadingBox");
  const container = document.getElementById("itineraryContainer");

  loadingBox.style.display = "block";
  container.style.display = "none";

  const payload = {
    city: state.city,
    time_available: state.time_available,
    interests: state.interests,
    budget: state.budget,
    lang: state.lang,
    api_key: state.apiKey || undefined
  };

  try {
    const response = await fetch("/api/itinerary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`Server returned status ${response.status}`);
    }

    const data = await response.json();
    state.currentItinerary = data;
    renderItinerary(data);
  } catch (err) {
    console.error("Itinerary fetch failed:", err);
    container.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: #DC2626;">
        <h3>⚠️ Could not generate itinerary</h3>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">${escapeHtml(err.message)}</p>
        <button class="btn-generate" style="width: auto; margin: 1rem auto;" onclick="loadItinerary()">Retry</button>
      </div>
    `;
    container.style.display = "block";
  } finally {
    loadingBox.style.display = "none";
  }
}

// Render Itinerary Cards
function renderItinerary(data) {
  const container = document.getElementById("itineraryContainer");
  const dict = I18N[state.lang] || I18N.en;

  const isAi = data.source === "groq_ai" || data.source === "gemini_ai";
  const sourceText = isAi ? dict.sourceAi : dict.sourceFallback;
  const sourceClass = isAi ? "badge-ai" : "badge-city";

  let html = `
    <div class="itinerary-header">
      <div class="itinerary-badges">
        <span class="badge ${sourceClass}">⚡ ${escapeHtml(sourceText)}</span>
        <span class="badge badge-city">📍 ${escapeHtml(data.city || state.city)}</span>
        <span class="badge badge-duration">⏱️ ${escapeHtml((data.duration || state.time_available).replace('_', ' ').toUpperCase())}</span>
        <span class="badge" style="background:#FEF3C7; color:#B45309; border:1px solid #FDE68A;">
          🏛️ ${data.total_stops || data.stops.length} ${dict.stopLabel}s
        </span>
      </div>
      <h2 class="itinerary-title">${escapeHtml(data.title)}</h2>
      <p class="itinerary-summary">${escapeHtml(data.summary)}</p>
    </div>

    <div class="timeline">
  `;

  data.stops.forEach((stop, idx) => {
    const isHidden = Boolean(stop.hidden_gem);
    const stopNum = stop.stop_number || (idx + 1);

    // Format 3-line history
    let historyLines = [];
    if (Array.isArray(stop.history_culture_3line)) {
      historyLines = stop.history_culture_3line;
    } else if (typeof stop.history_culture_3line === "string") {
      historyLines = stop.history_culture_3line.split("\n").filter(s => s.trim());
    } else {
      historyLines = [stop.description || "Historical landmark in Haryana."];
    }

    const food = stop.local_food || {};
    const mapsLink = stop.maps_url || `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(stop.name + " " + stop.city)}`;

    html += `
      <div class="stop-card ${isHidden ? 'is-hidden-gem' : ''}" id="stop-${stop.place_id || idx}">
        <div class="stop-marker">${stopNum}</div>

        ${isHidden ? `
          <div class="gem-pill-banner">
            ${dict.hiddenGemBadge}
          </div>
        ` : ''}

        <div class="stop-top-meta">
          <div class="stop-timing">
            <span>🕒</span> <span>${escapeHtml(stop.timing || "Recommended Slot")}</span>
          </div>
          <div class="stop-tags-row">
            ${stop.category ? `<span class="stop-tag">${escapeHtml(stop.category)}</span>` : ''}
            ${stop.visiting_hours ? `<span class="stop-tag">⏰ ${dict.hoursLabel}: ${escapeHtml(stop.visiting_hours)}</span>` : ''}
            ${stop.entry_fee ? `<span class="stop-tag">🎟️ ${dict.entryLabel}: ${escapeHtml(stop.entry_fee)}</span>` : ''}
          </div>
        </div>

        <h3 class="stop-name">${escapeHtml(stop.name)} <span style="font-size: 0.9rem; font-weight: 500; color: #6B7280;">(${escapeHtml(stop.city)})</span></h3>

        <!-- 3-line history lore -->
        <div class="history-box">
          <div class="history-box-label">
            <span>📜</span> <span>${dict.threeLineStory}</span>
          </div>
          ${historyLines.map(line => `<div class="history-line">${escapeHtml(line)}</div>`).join("")}
        </div>

        <!-- Why it matters -->
        <div class="why-matters-box">
          <div class="why-matters-title">
            <span>⭐</span> <span>${dict.whyItMatters}</span>
          </div>
          <div class="why-matters-desc">${escapeHtml(stop.why_it_matters || stop.description || '')}</div>
        </div>

        <!-- Local Food Pick -->
        ${food.dish ? `
          <div class="food-pick-card">
            <div class="food-icon-wrap">🍲</div>
            <div class="food-details">
              <div class="food-badge">${dict.foodBadge}</div>
              <div class="food-dish-name">${escapeHtml(food.dish)}</div>
              ${food.recommended_joint ? `<div class="food-joint">📍 ${escapeHtml(food.recommended_joint)}</div>` : ''}
              ${food.description ? `<div class="food-desc">${escapeHtml(food.description)}</div>` : ''}
            </div>
          </div>
        ` : ''}

        <!-- Stop Actions -->
        <div class="stop-actions">
          <a href="${escapeHtml(mapsLink)}" target="_blank" rel="noopener noreferrer" class="btn-maps">
            <span>🗺️</span> <span>${dict.btnMaps}</span>
          </a>
          <button type="button" class="btn-ask-this-place" onclick="askAboutPlace('${escapeHtml(stop.name)}')">
            <span>💬</span> <span>${dict.btnAskGuide}</span>
          </button>
        </div>

      </div>
    `;
  });

  html += `</div>`;
  container.innerHTML = html;
  container.style.display = "block";
}

// "Ask Guide About This Stop" trigger
function askAboutPlace(placeName) {
  const query = state.lang === "hi" 
    ? `${placeName} के बारे में कुछ और खास बातें और इतिहास बताएं`
    : `Tell me more fascinating stories, tips and secrets about ${placeName}`;
  const input = document.getElementById("chatInput");
  if (input) {
    input.value = query;
  }
  document.getElementById("guideChatSection").scrollIntoView({ behavior: "smooth" });
  sendChatMessage(query);
}

// Chat Handlers
function handleChatSubmit(e) {
  if (e) e.preventDefault();
  const input = document.getElementById("chatInput");
  const query = input.value.trim();
  if (!query) return;
  sendChatMessage(query);
  input.value = "";
}

async function sendChatMessage(query) {
  const messagesBox = document.getElementById("chatMessages");
  const sendBtn = document.getElementById("btnChatSend");

  // Append user bubble
  const userBubble = document.createElement("div");
  userBubble.className = "chat-bubble user";
  userBubble.textContent = query;
  messagesBox.appendChild(userBubble);

  // Append typing indicator
  const typingBubble = document.createElement("div");
  typingBubble.className = "chat-bubble guide";
  typingBubble.id = "guideTypingIndicator";
  typingBubble.innerHTML = `<em>${state.lang === "hi" ? "चाचा देसी सोच रहे हैं..." : "Chacha Desi is recalling verified lore..."}</em>`;
  messagesBox.appendChild(typingBubble);
  messagesBox.scrollTop = messagesBox.scrollHeight;

  if (sendBtn) sendBtn.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: query,
        lang: state.lang,
        api_key: state.apiKey || undefined
      })
    });

    const data = await res.json();
    typingBubble.remove();

    // Render guide reply
    const guideBubble = document.createElement("div");
    guideBubble.className = "chat-bubble guide";

    // Format markdown-like bold and bullet text
    const formatted = formatChatText(data.answer);
    guideBubble.innerHTML = formatted;

    const sourceTag = document.createElement("div");
    sourceTag.className = "chat-bubble-source";
    sourceTag.textContent = data.source === "groq_ai" ? "⚡ Groq (Llama 3.3 70B)" : (data.source === "gemini_ai" ? "⚡ Gemini" : "🛡️ Grounded Haryana Knowledge Base");
    guideBubble.appendChild(sourceTag);

    messagesBox.appendChild(guideBubble);
    state.chatHistory.push({ user: query, guide: data.answer });
  } catch (err) {
    typingBubble.remove();
    const errorBubble = document.createElement("div");
    errorBubble.className = "chat-bubble guide";
    errorBubble.style.borderColor = "#F87171";
    errorBubble.textContent = state.lang === "hi"
      ? "क्षमा करें, उत्तर प्राप्त करने में समस्या हुई। कृपया पुनः प्रयास करें।"
      : "Apologies, could not fetch an answer right now. Please try again.";
    messagesBox.appendChild(errorBubble);
  } finally {
    if (sendBtn) sendBtn.disabled = false;
    messagesBox.scrollTop = messagesBox.scrollHeight;
  }
}

function formatChatText(text) {
  if (!text) return "";
  let clean = escapeHtml(text);
  // Bold **text**
  clean = clean.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  // Bullets • or *
  clean = clean.replace(/(?:^|\n)[•*]\s*(.*?)(?=\n|$)/g, "<br>• $1");
  // Line breaks
  clean = clean.replace(/\n\n/g, "<br><br>");
  return clean;
}

// Modal Handlers
function openKeyModal() {
  const modal = document.getElementById("keyModal");
  const input = document.getElementById("apiKeyInput");
  if (input) input.value = state.apiKey;
  if (modal) modal.style.display = "flex";
}

function closeKeyModal() {
  const modal = document.getElementById("keyModal");
  if (modal) modal.style.display = "none";
}

function closeKeyModalOnOverlay(e) {
  if (e.target.id === "keyModal") {
    closeKeyModal();
  }
}

async function saveApiKey() {
  const input = document.getElementById("apiKeyInput");
  const key = input ? input.value.trim() : "";
  state.apiKey = key;
  sessionStorage.setItem("desi_groq_api_key", key);

  if (key) {
    try {
      await fetch("/api/set-key", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: key })
      });
    } catch (e) {
      console.warn("Could not set session key on server:", e);
    }
  }

  checkBackendHealth();
  closeKeyModal();
  // Reload current itinerary with the new key!
  loadItinerary();
}

// Utilities
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

