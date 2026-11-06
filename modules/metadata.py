import json
import re
from datetime import datetime, timezone
from modules.base import BaseModule

class MetadataModule(BaseModule):
    name = "metadata"

    def score_title(self, title: str, top_competitor_titles: list, primary_keyword: str) -> dict:
        """
        Scores a title option (0-100) based on algorithmic and psychological factors:
        - Character Length (<70 chars, sweet spot 45-65)
        - Keyword placement (front-loaded)
        - Power / Curiosity words (without cheap deceit)
        - Token overlap with top velocity competitor titles
        """
        score = 0
        notes = []

        length = len(title)
        # 1. Length constraint: strictly < 70 chars
        if length > 70:
            notes.append("Truncation Warning: Over 70 characters (will get cut off on mobile)")
            score += 10
        elif 45 <= length <= 68:
            score += 25
            notes.append(f"Optimal length ({length} chars)")
        elif length < 45:
            score += 15
            notes.append(f"Slightly short ({length} chars), could add specific context")

        # 2. Keyword presence & placement
        kw_lower = primary_keyword.lower()
        title_lower = title.lower()
        if kw_lower in title_lower:
            # Check if in first half
            pos = title_lower.find(kw_lower)
            if pos <= 25:
                score += 25
                notes.append("Primary keyword strongly front-loaded")
            else:
                score += 15
                notes.append("Primary keyword present but placed late")
        else:
            # Partial word overlap
            kw_tokens = set(kw_lower.split())
            overlap = kw_tokens.intersection(set(title_lower.split()))
            if overlap:
                score += 10
                notes.append(f"Partial keyword overlap: {overlap}")
            else:
                notes.append("Primary keyword missing")

        # 3. Emotional / Curiosity / Clarity hooks
        hook_triggers = [
            "truth", "honest", "test", "mistake", "vs", "guide",
            "before you", "why", "how to", "real", "cost", "survive"
        ]
        has_trigger = any(t in title_lower for t in hook_triggers)
        if has_trigger:
            score += 20
            notes.append("Contains high-engagement hook trigger word")
        else:
            score += 5

        # 4. No cheap deceitful clickbait check
        spam_words = ["you won't believe", "insane!!!", "omg", "shocking", "died", "cops called"]
        if any(sw in title_lower for sw in spam_words):
            score -= 30
            notes.append("Spam/Misleading clickbait penalty applied")
        else:
            score += 10
            notes.append("Clean, non-misleading curiosity gap")

        # 5. Overlap with top niche titles
        all_comp_tokens = set()
        for t in top_competitor_titles:
            words = re.findall(r"\w+", t.lower())
            all_comp_tokens.update(words)

        title_words = set(re.findall(r"\w+", title_lower))
        comp_overlap = title_words.intersection(all_comp_tokens)
        overlap_score = min(20, len(comp_overlap) * 4)
        score += overlap_score
        notes.append(f"Niche vocabulary resonance ({len(comp_overlap)} matching keywords)")

        final_score = min(100, max(0, score))
        return {
            "title": title,
            "char_count": length,
            "score": final_score,
            "grade": "A+" if final_score >= 85 else ("A" if final_score >= 75 else ("B" if final_score >= 60 else "C")),
            "breakdown": notes
        }

    def run(self, draft_topic_or_script: str = None, **kwargs) -> dict:
        competitor_vids = self.db.get_competitor_videos(days_limit=90)
        top_titles = [v["title"] for v in competitor_vids[:10]]
        sample_size = len(competitor_vids)
        confidence = self.get_confidence(sample_size)
        data_source = f"SQLite cache: Top {min(10, sample_size)} competitor titles ranked by view velocity"

        # Topic fallback if none passed
        default_topic = (
            "Solo motorcycle touring packing list, luggage choices, action camera mounts, and fuel management on Himalayan 450"
        )
        input_text = draft_topic_or_script or default_topic
        primary_keyword = "motorcycle touring packing list"

        # Generate 5 titles strictly < 70 chars with clear non-clickbait value propositions
        raw_titles = [
            "Motorcycle Touring Packing List: 7 Items I Regret Carrying",  # 57 chars
            "Himalayan 450 Touring Setup: The Real Luggage & Tool Kit",      # 55 chars
            "Packing for Ladakh Solo Ride: What Actually Fits in 40L",       # 54 chars
            "Soft Bags vs Hard Panniers: Touring Truth After 5,000 KM",     # 57 chars
            "5 Essential Motorcycle Packing Hacks for Long Highway Tours"   # 59 chars
        ]

        scored_titles = [
            self.score_title(t, top_titles, primary_keyword) for t in raw_titles
        ]
        scored_titles.sort(key=lambda x: x["score"], reverse=True)

        # Generate Description with first 150 chars front-loaded for SEO & CTA
        # First 150 chars appear in search snippet and mobile preview
        first_150_chars = (
            "Get my complete motorcycle touring packing list and luggage setup for 2026. Download the free PDF checklist here: https://souviksays.com/pack"
        )
        description_body = f"""{first_150_chars}

In this video, I break down my field-tested packing system for long-distance motorcycle expeditions and high-altitude mountain touring. We cover soft luggage vs aluminum boxes, emergency toolkits, and cold-weather camera battery hacks.

📌 TIMESTAMPS:
00:00 - The Harsh Truth About Touring Weight
01:15 - Soft Panniers vs Hard Aluminum Luggage
03:40 - Action Camera Cold Weather Battery Trick
06:20 - Emergency Spare Parts & Tube Kit
09:10 - Complete Saddlebag Weigh-in
11:00 - Route Advice & Wrap-up

🔧 GEAR SHOWN IN VIDEO:
- Waterproof Saddlebags: 40L Dual-side
- Tool Roll: 21mm wrench, chain breaker, tire levers
- Chin Mount: Full-face curved bracket + deadcat mic

💬 QUESTION FOR THE COMMUNTIY:
What is the one piece of gear you NEVER tour without? Drop your thoughts below!

#motovlog #motorcyclepacking #himalayan450 #motorcycletouring #biketrip"""

        # 15 Targeted Tags (Tiered: Broad, Specific, Long-tail)
        tags = [
            "motorcycle touring packing list",
            "motovlog",
            "motorcycle touring gear",
            "himalayan 450 touring",
            "motorcycle packing tips",
            "soft luggage vs hard panniers",
            "ladakh bike trip packing",
            "motorcycle emergency toolkit",
            "adventure motorcycle gear",
            "spiti valley bike trip",
            "action camera motovlog mount",
            "bike trip preparation",
            "long distance motorcycle riding",
            "motorcycle maintenance",
            "mototech explorer"
        ]

        return {
            "module": self.name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "data_source": data_source,
            "confidence": confidence,
            "input_topic_or_script": input_text,
            "primary_keyword": primary_keyword,
            "title_options": scored_titles,
            "description": {
                "first_150_chars": first_150_chars,
                "first_150_char_length": len(first_150_chars),
                "full_text": description_body
            },
            "tags_15": tags,
            "tag_count": len(tags)
        }

    def to_markdown(self, result: dict) -> str:
        md = []
        md.append("# 🏷️ Module 2: Metadata Optimization & Title Scoring\n")
        md.append(f"- **Data Source:** {result['data_source']}")
        md.append(f"- **Confidence Level:** {result['confidence']}")
        md.append(f"- **Target Keyword:** `{result['primary_keyword']}`\n")

        md.append("## 🏆 5 Scored Title Options (Ranked by Algorithmic Score)")
        md.append("| Rank | Title (<70 chars) | Chars | Score | Grade | Key Signals |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for i, t in enumerate(result["title_options"], 1):
            signals = ", ".join(t["breakdown"][:2])
            md.append(f"| #{i} | **{t['title']}** | {t['char_count']} | {t['score']}/100 | `{t['grade']}` | {signals} |")

        md.append("\n### Title Recommendation:")
        best = result["title_options"][0]
        md.append(f"- **Selected Top Title:** `{best['title']}`")
        for b in best["breakdown"]:
            md.append(f"  - {b}")

        md.append("\n## 📝 Description (SEO Front-Loaded)")
        md.append(f"**First 150 Characters (Search Snippet Preview - Length: {result['description']['first_150_char_length']} chars):**")
        md.append(f"> *\"{result['description']['first_150_chars']}\"*\n")

        md.append("```text")
        md.append(result["description"]["full_text"])
        md.append("```")

        md.append(f"\n## 🏷️ 15 Targeted Tags (Count: {result['tag_count']})")
        md.append("```text")
        md.append(", ".join(result["tags_15"]))
        md.append("```\n")

        return "\n".join(md)
