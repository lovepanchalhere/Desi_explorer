import sys
import io
import json
import engine
import server

# Ensure stdout encodes UTF-8
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_tests():
    print("=== TEST 1: Load Places Dataset ===")
    places = engine.load_places()
    assert len(places) >= 20, f"Expected >= 20 places, got {len(places)}"
    print(f"PASS: Loaded {len(places)} authentic places.")

    cities = set(p["city"] for p in places)
    print("Found cities:", cities)
    expected_cities = {"Karnal", "Kurukshetra", "Panipat", "Pinjore", "Mullana/Ambala"}
    for ec in expected_cities:
        assert ec in cities, f"Missing city: {ec}"
    print("PASS: All 5 required cities present.")

    hidden_gems = [p for p in places if p.get("hidden_gem")]
    print(f"Hidden gems count: {len(hidden_gems)}")
    assert len(hidden_gems) >= 5, "Expected at least 5 hidden gems across cities"
    print("PASS: Hidden gems verified.")

    print("\n=== TEST 2: Rule-based Itinerary Generation (Kurukshetra, Half Day) ===")
    itin_kkr = engine.generate_fallback_itinerary(
        city="Kurukshetra",
        time_available="half_day",
        interests=["spiritual", "heritage"],
        budget="low",
        lang="en"
    )
    assert itin_kkr["stops"], "No stops generated"
    assert len(itin_kkr["stops"]) == 3, f"Expected 3 stops for half day, got {len(itin_kkr['stops'])}"
    has_gem = any(s["hidden_gem"] for s in itin_kkr["stops"])
    assert has_gem, "Itinerary MUST contain at least one hidden gem!"
    print(f"PASS: Title: {itin_kkr['title']}")
    for s in itin_kkr["stops"]:
        print(f"  - Stop {s['stop_number']}: {s['name']} [{s['timing']}] (Hidden Gem: {s['hidden_gem']})")
        assert len(s["history_culture_3line"]) == 3, f"Expected 3-line history, got {len(s['history_culture_3line'])}"
        assert s["why_it_matters"], "Missing why it matters"
        assert s["local_food"]["dish"], "Missing local food dish"
        assert "maps.google.com" in s["maps_url"] or "google.com/maps" in s["maps_url"], "Invalid Google Maps URL"

    print("\n=== TEST 3: Rule-based Itinerary Generation (Panipat, 2 Hours, Hindi) ===")
    itin_pan = engine.generate_fallback_itinerary(
        city="Panipat",
        time_available="2_hours",
        interests=["heritage"],
        budget="low",
        lang="hi"
    )
    assert len(itin_pan["stops"]) == 2, f"Expected 2 stops for 2 hours, got {len(itin_pan['stops'])}"
    has_gem_pan = any(s["hidden_gem"] for s in itin_pan["stops"])
    assert has_gem_pan, "Panipat 2hr itinerary MUST contain at least one hidden gem!"
    print(f"PASS Hindi: {itin_pan['title']}")
    for s in itin_pan["stops"]:
        print(f"  - पड़ाव {s['stop_number']}: {s['name']} (Hidden Gem: {s['hidden_gem']})")
        print(f"    भोजन: {s['local_food']['dish']}")

    print("\n=== TEST 4: Rule-based Itinerary Generation (Karnal, Full Day) ===")
    itin_kar = engine.generate_fallback_itinerary(
        city="Karnal",
        time_available="full_day",
        interests=["nature", "heritage"],
        budget="medium",
        lang="en"
    )
    assert len(itin_kar["stops"]) >= 4, f"Expected >= 4 stops for full day, got {len(itin_kar['stops'])}"
    assert any(s["hidden_gem"] for s in itin_kar["stops"]), "Karnal full day MUST have hidden gem"
    print(f"PASS: Karnal full day stops: {len(itin_kar['stops'])}")

    print("\n=== TEST 5: Ask Local Guide (Grounded Q&A) ===")
    q1 = engine.ask_local_guide("Tell me about Sheikh Chilli tomb", lang="en")
    assert "Sheikh Chilli" in q1["answer"] or "Dara Shikoh" in q1["answer"] or "Taj Mahal" in q1["answer"]
    print("PASS Guide Q1 (English): Answer found.")

    q2 = engine.ask_local_guide("असली बाजरा रोटी और देशी मक्खन कहाँ मिलेगा?", lang="hi")
    assert "बाजरे की रोटी" in q2["answer"] or "मक्खन" in q2["answer"]
    print("PASS Guide Q2 (Hindi): Authentic food answer verified.")

    q3 = engine.ask_local_guide("What are the hidden gems in Haryana?", lang="en")
    assert "hidden gems" in q3["answer"].lower()
    print("PASS Guide Q3 (Hidden gems query): Verified.")

    print("\n=== ALL UNIT & INTEGRATION TESTS PASSED 100%! ===")

if __name__ == "__main__":
    run_tests()

