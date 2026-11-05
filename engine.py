import json
import os
import urllib.request
import urllib.parse
import ssl
import re

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "places.json")

def load_places():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def filter_places(places, city=None, interests=None, budget=None):
    filtered = places[:]
    if city and city.lower() not in ["all", "all cities", "sab", "sab shehar"]:
        c_low = city.lower().strip()
        filtered = [
            p for p in filtered
            if c_low in p["city"].lower() or c_low in p.get("city_hi", "").lower()
        ]
        # If city filter is too restrictive and yields fewer than 2 places, fallback to all places in that city
        if not filtered:
            filtered = [p for p in places if c_low in p["city"].lower()]

    if not filtered:
        filtered = places[:]
    return filtered

def score_place(p, interests, budget):
    score = 0
    cat = p.get("category", "").lower()
    if interests:
        user_interests = [i.lower() for i in interests]
        if any(ui in cat for ui in user_interests):
            score += 3
    if budget:
        if p.get("budget_level", "").lower() == budget.lower():
            score += 2
    return score

def generate_fallback_itinerary(city="Kurukshetra", time_available="half_day", interests=None, budget="low", lang="en"):
    all_places = load_places()
    candidates = filter_places(all_places, city, interests, budget)

    # Determine number of stops
    t_val = (time_available or "").lower()
    if "2" in t_val or "two" in t_val:
        num_stops = 2
        time_slots = ["09:30 AM - 10:45 AM", "11:00 AM - 12:15 PM"]
    elif "full" in t_val or "day" in t_val and "half" not in t_val:
        num_stops = 5
        time_slots = [
            "08:30 AM - 10:00 AM",
            "10:15 AM - 11:45 AM",
            "12:00 PM - 01:30 PM",
            "02:30 PM - 04:00 PM",
            "04:30 PM - 06:30 PM"
        ]
    else: # half_day default
        num_stops = 3
        time_slots = [
            "09:00 AM - 10:30 AM",
            "10:45 AM - 12:15 PM",
            "12:30 PM - 02:00 PM"
        ]

    # Score candidates
    scored = sorted(candidates, key=lambda p: score_place(p, interests, budget), reverse=True)

    # Make sure we have at least 1 hidden gem
    hidden_gems = [p for p in scored if p.get("hidden_gem")]
    regular = [p for p in scored if not p.get("hidden_gem")]

    selected = []
    # If no hidden gem in current city pool, grab from all places
    if not hidden_gems:
        hidden_gems = [p for p in all_places if p.get("hidden_gem")]

    # Select primary stops
    needed_regulars = num_stops - 1
    selected.extend(regular[:needed_regulars])

    # If still need places, fill from available
    if len(selected) < needed_regulars:
        for p in regular:
            if p not in selected:
                selected.append(p)
                if len(selected) == needed_regulars:
                    break

    # Add hidden gem
    if hidden_gems:
        gem = hidden_gems[0]
        if gem not in selected:
            selected.append(gem)
        else:
            for g in hidden_gems:
                if g not in selected:
                    selected.append(g)
                    break

    # If still short, pull from candidates
    for p in scored:
        if len(selected) >= num_stops:
            break
        if p not in selected:
            selected.append(p)

    selected = selected[:num_stops]

    is_hindi = (lang == "hi")
    itinerary_stops = []

    for idx, place in enumerate(selected):
        slot = time_slots[idx] if idx < len(time_slots) else f"Stop {idx+1}"
        place_name = place.get("name_hi") if is_hindi and place.get("name_hi") else place.get("name")
        city_name = place.get("city_hi") if is_hindi and place.get("city_hi") else place.get("city")
        desc = place.get("description_hi") if is_hindi and place.get("description_hi") else place.get("description")
        hist = place.get("history_hi") if is_hindi and place.get("history_hi") else place.get("history")
        why = place.get("why_it_matters_hi") if is_hindi and place.get("why_it_matters_hi") else place.get("why_it_matters")
        entry = place.get("entry_fee_hi") if is_hindi and place.get("entry_fee_hi") else place.get("entry_fee")
        best = place.get("best_time_hi") if is_hindi and place.get("best_time_hi") else place.get("best_time")

        # History 3-line format
        history_sentences = [s.strip() for s in hist.split(". ") if s.strip()]
        if len(history_sentences) < 3:
            # Add context sentence
            if is_hindi:
                history_3lines = [
                    f"1. ऐतिहासिक संदर्भ: {hist}",
                    f"2. सांस्कृतिक महत्व: {desc}",
                    f"3. धरोहर मूल्य: {why}"
                ]
            else:
                history_3lines = [
                    f"1. Historical Context: {hist}",
                    f"2. Cultural Roots: {desc}",
                    f"3. Living Heritage: {why}"
                ]
        else:
            history_3lines = [f"{i+1}. {history_sentences[i]}." for i in range(min(3, len(history_sentences)))]

        # Food item
        food = place.get("nearby_food", {})
        food_dish = food.get("dish_hi") if is_hindi and food.get("dish_hi") else food.get("dish")
        food_joint = food.get("joint_hi") if is_hindi and food.get("joint_hi") else food.get("joint")
        food_desc = food.get("description_hi") if is_hindi and food.get("description_hi") else food.get("description")

        maps_query = urllib.parse.quote_plus(f"{place['name']} {place['city']} Haryana")
        maps_link = f"https://www.google.com/maps/search/?api=1&query={maps_query}"

        itinerary_stops.append({
            "stop_number": idx + 1,
            "place_id": place.get("id"),
            "name": place_name,
            "city": city_name,
            "timing": slot,
            "hidden_gem": place.get("hidden_gem", False),
            "category": place.get("category_hi" if is_hindi else "category"),
            "visiting_hours": place.get("visiting_hours", "Check locally"),
            "entry_fee": entry,
            "best_time": best,
            "maps_url": maps_link,
            "history_culture_3line": history_3lines,
            "why_it_matters": why,
            "local_food": {
                "dish": food_dish,
                "recommended_joint": food_joint,
                "description": food_desc
            }
        })

    title = (
        f"{city if city != 'All' else 'हरियाणा'} का विशेष भ्रमण मार्गदर्शक ({time_available})"
        if is_hindi else
        f"Handcrafted {city if city != 'All' else 'Haryana'} Discovery Route ({time_available.replace('_', ' ').title()})"
    )
    summary = (
        f"इस यात्रा योजना में हरियाणा की समृद्ध संस्कृति, इतिहास और कम चर्चित छिपे रत्नों ('Hidden Gems') को सम्मिलित किया गया है।"
        if is_hindi else
        f"Tailored plan featuring must-visit historical icons and lesser-known hidden gems with authentic local flavors."
    )

    return {
        "title": title,
        "summary": summary,
        "city": city,
        "duration": time_available,
        "total_stops": len(itinerary_stops),
        "source": "rule_based_fallback",
        "stops": itinerary_stops
    }

def clean_json_text(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()

def call_groq_api(prompt, api_key=None, json_mode=False):
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found in environment or request.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    models = ["llama-3.3-70b-versatile", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"]
    last_err = None

    for model in models:
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are the local historian and tour architect for 'Desi Explorer', an authentic Haryana tourism guide."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens": 2048
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            method="POST"
        )
        context = ssl.create_default_context()
        try:
            with urllib.request.urlopen(req, timeout=15, context=context) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                choices = res_json.get("choices", [])
                if choices:
                    msg = choices[0].get("message", {})
                    return msg.get("content", "")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            last_err = f"HTTP {e.code} for model {model}: {err_body}"
            print(f"[Groq model '{model}' error]: {last_err}")
            continue
        except Exception as e:
            last_err = f"Error with model {model}: {e}"
            print(f"[Groq model '{model}' exception]: {last_err}")
            continue

    raise RuntimeError(f"All Groq models failed: {last_err}")

def generate_ai_itinerary(city="Kurukshetra", time_available="half_day", interests=None, budget="low", lang="en", api_key=None):
    all_places = load_places()
    candidates = filter_places(all_places, city, interests, budget)

    # Always prepare fallback in case AI call fails
    fallback = generate_fallback_itinerary(city, time_available, interests, budget, lang)

    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        return fallback

    # Prepare compact context of allowed places
    compact_places = []
    for p in candidates:
        compact_places.append({
            "id": p["id"],
            "name": p["name"],
            "name_hi": p.get("name_hi"),
            "city": p["city"],
            "city_hi": p.get("city_hi"),
            "category": p["category"],
            "description": p["description_hi"] if lang == "hi" else p["description"],
            "history": p["history_hi"] if lang == "hi" else p["history"],
            "why_it_matters": p["why_it_matters_hi"] if lang == "hi" else p["why_it_matters"],
            "hidden_gem": p["hidden_gem"],
            "visiting_hours": p.get("visiting_hours", "Open daily"),
            "entry_fee": p.get("entry_fee_hi" if lang == "hi" else "entry_fee", "Free"),
            "best_time": p.get("best_time_hi" if lang == "hi" else "best_time", "Morning/Evening"),
            "nearby_food": p.get("nearby_food")
        })

    prompt_lang = "Hindi (हिंदी)" if lang == "hi" else "English"
    prompt = f"""You are the senior local historian and tour architect for "Desi Explorer", a local tourism guide for Haryana.
Your task is to generate a realistic, travel-optimized itinerary for a traveler with the following preferences:
- Destination City: {city}
- Available Time: {time_available}
- Interests: {', '.join(interests) if interests else 'All'}
- Budget: {budget}
- Output Language: {prompt_lang}

CRITICAL RULES:
1. ONLY select places from the provided JSON dataset below. NEVER invent places or facts.
2. The plan MUST include at least one place with "hidden_gem": true.
3. For a "2_hours" trip: pick exactly 2 stops.
4. For a "half_day" trip: pick 3 stops.
5. For a "full_day" trip: pick 4 or 5 stops.
6. Provide a short 3-line history/culture story for each stop (numbered 1, 2, 3).
7. Suggest realistic, sequential timings (e.g. "09:30 AM - 11:00 AM").
8. Always include the authentic nearby local food pick from the dataset.
9. Return ONLY valid JSON matching this schema with no markdown explanation:

{{
  "title": "Itinerary title in {prompt_lang}",
  "summary": "Brief 1-2 sentence overview in {prompt_lang}",
  "city": "{city}",
  "duration": "{time_available}",
  "total_stops": 3,
  "stops": [
    {{
      "stop_number": 1,
      "place_id": "id from dataset",
      "name": "Place name in {prompt_lang}",
      "city": "City name",
      "timing": "09:00 AM - 10:30 AM",
      "hidden_gem": true or false,
      "category": "heritage / spiritual / food / nature",
      "visiting_hours": "visiting hours",
      "entry_fee": "entry fee",
      "best_time": "best time",
      "maps_url": "https://www.google.com/maps/search/?api=1&query=ENCODED_NAME",
      "history_culture_3line": [
        "1. First sentence of history...",
        "2. Second sentence...",
        "3. Third sentence..."
      ],
      "why_it_matters": "Why it matters in {prompt_lang}",
      "local_food": {{
        "dish": "Dish name",
        "recommended_joint": "Eatery / Dhaba name",
        "description": "Short appetizing description"
      }}
    }}
  ]
}}

PLACES DATASET:
{json.dumps(compact_places, ensure_ascii=False)}
"""

    try:
        raw_text = call_groq_api(prompt, key, json_mode=True)
        cleaned = clean_json_text(raw_text)
        parsed = json.loads(cleaned)
        if "stops" in parsed and len(parsed["stops"]) > 0:
            parsed["source"] = "groq_ai"
            # Ensure maps_url and hidden_gem badge exist
            for st in parsed["stops"]:
                if not st.get("maps_url"):
                    q = urllib.parse.quote_plus(f"{st.get('name', '')} {st.get('city', '')} Haryana")
                    st["maps_url"] = f"https://www.google.com/maps/search/?api=1&query={q}"
            return parsed
        return fallback
    except Exception as e:
        print(f"[Groq API fallback triggered]: {e}")
        return fallback

def ask_local_guide(query, place_id=None, lang="en", api_key=None):
    all_places = load_places()
    is_hindi = (lang == "hi")

    # Find matched place if place_id given or query mentions place
    matched_place = None
    if place_id:
        for p in all_places:
            if p["id"] == place_id:
                matched_place = p
                break

    q_lower = query.lower()
    if not matched_place:
        for p in all_places:
            if p["name"].lower() in q_lower or p.get("name_hi", "").lower() in q_lower or p["id"].lower() in q_lower:
                matched_place = p
                break
        if not matched_place:
            for p in all_places:
                words = [w for w in re.findall(r"\w+", p["name"].lower()) if len(w) > 3]
                if any(w in q_lower for w in words):
                    matched_place = p
                    break

    # Check for dish match in places
    if not matched_place:
        for p in all_places:
            food_info = p.get("nearby_food", {})
            d_en = food_info.get("dish", "").lower()
            d_hi = food_info.get("dish_hi", "").lower()
            if any(term in q_lower for term in ["bajra", "बाजरा", "मक्खन", "rabri", "रबड़ी", "kullhad", "कुल्हड़", "khichdi", "खिचड़ी"]) and ("bajra" in d_en or "बाजरा" in d_hi):
                matched_place = p
                break
            if any(term in q_lower for term in ["achaar", "अचार", "पचरंगा", "pachranga"]) and ("pachranga" in d_en or "पचरंगा" in d_hi):
                matched_place = p
                break
            if any(term in q_lower for term in ["kadhi", "कढ़ी"]) and ("kadhi" in d_en or "कढ़ी" in d_hi):
                matched_place = p
                break

    # Grounded fallback answer generator
    def generate_grounded_fallback():
        if matched_place:
            name = matched_place["name_hi"] if is_hindi else matched_place["name"]
            city = matched_place["city_hi"] if is_hindi else matched_place["city"]
            desc = matched_place["description_hi"] if is_hindi else matched_place["description"]
            hist = matched_place["history_hi"] if is_hindi else matched_place["history"]
            why = matched_place["why_it_matters_hi"] if is_hindi else matched_place["why_it_matters"]
            hours = matched_place.get("visiting_hours", "Not specified")
            fee = matched_place.get("entry_fee_hi" if is_hindi else "entry_fee", "Free")
            gem = "हाँ (छिपा हुआ रत्न / Hidden Gem)" if (is_hindi and matched_place.get("hidden_gem")) else (
                "Yes (Hidden Gem)" if matched_place.get("hidden_gem") else ("प्रसिद्ध स्थल" if is_hindi else "Popular Landmark")
            )
            food = matched_place.get("nearby_food", {})
            food_dish = food.get("dish_hi" if is_hindi else "dish", "")
            food_joint = food.get("joint_hi" if is_hindi else "joint", "")

            if is_hindi:
                ans = f"**{name} ({city}) के बारे में स्थानीय मार्गदर्शक जानकारी:**\n\n"
                ans += f"• **परिचय:** {desc}\n"
                ans += f"• **इतिहास:** {hist}\n"
                ans += f"• **यह क्यों खास है:** {why}\n"
                ans += f"• **समय व टिकट:** समय: {hours} | प्रवेश: {fee}\n"
                ans += f"• **श्रेणी:** {gem}\n"
                ans += f"• **निकटवर्ती प्रामाणिक स्वाद:** {food_dish} ({food_joint} पर अवश्य चखें)।\n"
            else:
                ans = f"**Local Guide Insights for {name} ({city}):**\n\n"
                ans += f"• **Overview:** {desc}\n"
                ans += f"• **History:** {hist}\n"
                ans += f"• **Why it matters:** {why}\n"
                ans += f"• **Hours & Entry:** Hours: {hours} | Entry: {fee}\n"
                ans += f"• **Status:** {gem}\n"
                ans += f"• **Must-try food nearby:** {food_dish} at {food_joint}.\n"
            return ans

        # General food query fallback
        food_keywords = ["food", "khana", "dish", "khane", "roti", "sweet", "chaat", "खाने", "खाना", "भोजन", "व्यंजन", "स्वाद", "रोटी", "मिठाई", "ढाबा"]
        if any(fk in q_lower for fk in food_keywords):
            if is_hindi:
                return "हरियाणा के प्रामाणिक भोजन में चूल्हे की बाजरे की रोटी, देशी सफेद मक्खन, काचरी की चटनी, कुरुक्षेत्र की गाढ़ी रबड़ी व खुरचन पेड़ा, पानीपत का पचरंगा अचार व कढ़ी-कचौरी, और अंबाला का रबड़ी-मालपुआ प्रमुख हैं। आप किसी भी पड़ाव के साथ उसकी निकटवर्ती प्रसिद्ध डिश देख सकते हैं!"
            else:
                return "Authentic Haryanvi food highlights include hot Bajra Roti with fresh churned white butter & jaggery, Kurukshetra Rabri & Khurchan Peda, Panipat's 5-ingredient Pachranga pickle with stuffed parathas, and Ambala Cantt's famous Kali Mirch chaat & Rabri Malpua!"

        hidden_keywords = ["hidden gem", "secret", "छिपे", "अनदेखे", "रत्न", "अनोखे"]
        if any(hk in q_lower for hk in hidden_keywords):
            gems = [p for p in all_places if p.get("hidden_gem")]
            gem_names = [f"• {p['name_hi'] if is_hindi else p['name']} ({p['city']})" for p in gems[:4]]
            if is_hindi:
                return "हरियाणा के शीर्ष छिपे हुए रत्न (Hidden Gems) जिन्हें सामान्य पर्यटक छोड़ देते हैं:\n" + "\n".join(gem_names)
            else:
                return "Top hidden gems in Haryana that mainstream highway travelers often miss:\n" + "\n".join(gem_names)

        # Default help
        if is_hindi:
            return "नमस्ते! मैं देसी एक्सप्लोरर का स्थानीय गाइड हूँ। आप मुझसे करनाल, कुरुक्षेत्र, पानीपत, पिंजौर या मुलाना/अंबाला के किसी भी स्थल के इतिहास, घूमने के सही समय, टिकट या पारंपरिक खान-पान के बारे में पूछ सकते हैं।"
        else:
            return "Namaste! I am your Desi Explorer local guide. Ask me about any spot in Karnal, Kurukshetra, Panipat, Pinjore, or Mullana/Ambala — its historical lore, ideal visiting hours, entry fees, or authentic local food recommendations!"

    fallback_ans = generate_grounded_fallback()

    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        return {"answer": fallback_ans, "source": "grounded_knowledge_base"}

    # Groq prompt grounded in verified places (optimized compact context)
    knowledge_context = []
    if matched_place:
        knowledge_context.append(
            f"PRIMARY PLACE: {matched_place['name']} ({matched_place.get('name_hi')}), City: {matched_place['city']}, "
            f"Hidden Gem: {matched_place['hidden_gem']}, Hours: {matched_place.get('visiting_hours')}, "
            f"Entry: {matched_place.get('entry_fee')}, Best Time: {matched_place.get('best_time')}, "
            f"History: {matched_place.get('history')}, Why: {matched_place.get('why_it_matters')}, "
            f"Food: {matched_place.get('nearby_food', {}).get('dish')} at {matched_place.get('nearby_food', {}).get('joint')}"
        )
        # Add 1-2 companion places from the same city
        same_city = [p for p in all_places if p['city'] == matched_place['city'] and p['id'] != matched_place['id']]
        for p in same_city[:2]:
            knowledge_context.append(
                f"Nearby Place: {p['name']} ({p.get('name_hi')}), Hidden Gem: {p['hidden_gem']}, Food: {p.get('nearby_food', {}).get('dish')}"
            )
    else:
        for p in all_places:
            knowledge_context.append(
                f"Place: {p['name']} ({p.get('name_hi')}), City: {p['city']}, Hidden Gem: {p['hidden_gem']}, "
                f"Hours: {p.get('visiting_hours')}, Entry: {p.get('entry_fee')}, Food: {p.get('nearby_food', {}).get('dish')}"
            )

    prompt = f"""You are "Desi Explorer's Local Guide", an authentic, warm, and highly knowledgeable native of Haryana.
Answer the user's question using ONLY the provided verified factual knowledge base below.
Never invent facts, dates, or places outside this knowledge base.
Language to answer in: {'Hindi (हिंदी)' if is_hindi else 'English'}.

USER QUESTION: {query}

VERIFIED LOCAL KNOWLEDGE BASE:
{chr(10).join(knowledge_context)}

Respond in 2-4 friendly, concise paragraphs or bullet points. Include historical context, visiting tips, and local food recommendations whenever relevant.
"""
    try:
        reply = call_groq_api(prompt, key, json_mode=False)
        return {"answer": reply.strip(), "source": "groq_ai"}
    except Exception as e:
        print(f"[Groq Chat fallback]: {e}")
        return {"answer": fallback_ans, "source": "grounded_knowledge_base"}
