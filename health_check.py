import os
import sys
import json
import engine
from server import load_env_file

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_env_file()

def run_comprehensive_check():
    print("=" * 60)
    print("DESI EXPLORER - COMPREHENSIVE SYSTEM AUDIT")
    print("=" * 60)

    # 1. Dataset Verification
    print("\n[1/5] Checking Dataset (data/places.json)...")
    places = engine.load_places()
    assert len(places) >= 20, f"Expected >= 20 places, found {len(places)}"
    cities = set(p["city"] for p in places)
    expected_cities = {"Karnal", "Kurukshetra", "Panipat", "Pinjore", "Mullana/Ambala"}
    assert expected_cities.issubset(cities), f"Missing cities: {expected_cities - cities}"
    hidden_gems = [p for p in places if p.get("hidden_gem")]
    assert len(hidden_gems) >= 5, "Insufficient hidden gems"
    print(f"  ✓ Total places: {len(places)}")
    print(f"  ✓ Cities covered: {', '.join(sorted(cities))}")
    print(f"  ✓ Hidden gems: {len(hidden_gems)} verified")

    # 2. Key & Environment
    print("\n[2/5] Checking Configuration & Security...")
    groq_key = os.environ.get("GROQ_API_KEY", "")
    assert groq_key, "GROQ_API_KEY is missing from environment"
    with open(".gitignore", "r", encoding="utf-8") as f:
        git_content = f.read()
    assert ".env" in git_content, ".env is not in .gitignore"
    print(f"  ✓ GROQ_API_KEY loaded: {groq_key[:8]}...{groq_key[-4:]}")
    print("  ✓ .gitignore properly excludes .env")

    # 3. AI Itinerary Generation (English & Hindi via Groq)
    print("\n[3/5] Testing AI Itinerary Generation with Groq...")
    # English test
    itin_en = engine.generate_ai_itinerary("Kurukshetra", "half_day", ["heritage"], "low", "en")
    assert itin_en.get("stops"), "No stops in English itinerary"
    assert any(s.get("hidden_gem") for s in itin_en["stops"]), "English itinerary missing hidden gem"
    print(f"  ✓ English route: '{itin_en.get('title')}' (Source: {itin_en.get('source')}, Stops: {len(itin_en['stops'])})")

    # Hindi test
    itin_hi = engine.generate_ai_itinerary("Panipat", "2_hours", ["heritage"], "low", "hi")
    assert itin_hi.get("stops"), "No stops in Hindi itinerary"
    assert any(s.get("hidden_gem") for s in itin_hi["stops"]), "Hindi itinerary missing hidden gem"
    print(f"  ✓ Hindi route: '{itin_hi.get('title')}' (Source: {itin_hi.get('source')}, Stops: {len(itin_hi['stops'])})")

    # 4. Fallback Engine Resiliency (Without API Key)
    print("\n[4/5] Testing Rule-Based Fallback Engine (Offline/Resilience)...")
    fallback_itin = engine.generate_fallback_itinerary("Karnal", "full_day", ["nature"], "medium", "en")
    assert len(fallback_itin["stops"]) >= 4, "Fallback full day stops insufficient"
    assert any(s["hidden_gem"] for s in fallback_itin["stops"]), "Fallback missing hidden gem"
    for s in fallback_itin["stops"]:
        assert len(s["history_culture_3line"]) == 3, "Stop history must be 3 lines"
        assert s["why_it_matters"], "Stop missing why_it_matters"
        assert s["local_food"]["dish"], "Stop missing local food dish"
        assert "google.com/maps" in s["maps_url"], "Invalid Google Maps URL"
    print(f"  ✓ Fallback itinerary verified: {len(fallback_itin['stops'])} stops with 3-line lore & maps links")

    # 5. Local Guide Chat (Grounded Q&A)
    print("\n[5/5] Testing 'Ask Local Guide' Chat Q&A...")
    chat_en = engine.ask_local_guide("What makes Sheikh Chilli tomb special?", lang="en")
    assert chat_en.get("answer"), "No answer returned for English query"
    print(f"  ✓ Chat (English) response generated ({chat_en.get('source')})")

    chat_hi = engine.ask_local_guide("असली हरियाणवी बाजरा रोटी कहाँ मिलेगी?", lang="hi")
    assert chat_hi.get("answer"), "No answer returned for Hindi query"
    print(f"  ✓ Chat (Hindi) response generated ({chat_hi.get('source')})")

    print("\n" + "=" * 60)
    print("ALL 5 SYSTEM CHECKS PASSED: EVERYTHING IS RUNNING PROPERLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_comprehensive_check()

