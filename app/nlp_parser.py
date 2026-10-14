import re
from typing import Dict, Any, List, Optional, Tuple
from app.models import AnimeDNAModel


class NLPSemanticParser:
    """
    Parses natural language anime queries into structured multi-dimensional DNA criteria,
    genre preferences, archetypes, and viewing constraints.
    """

    # Keyword rules for dimension tuning
    DIMENSION_SIGNALS = {
        "psychological": [
            "psychological", "mind game", "battle of wits", "cat and mouse", "intellectual",
            "cunning", "manipulation", "sanity", "mental", "chess match", "deception", "paranoia"
        ],
        "action_intensity": [
            "action", "fight", "battle", "combat", "explosive", "kinetic", "sakuga",
            "hype", "martial arts", "adrenaline", "shonen battle", "swords", "guns"
        ],
        "narrative_complexity": [
            "complex", "twist", "mind-bending", "plot twist", "non-linear", "puzzle",
            "deep plot", "intricate", "mystery", "conspiracy", "secrets", "timeline", "time travel"
        ],
        "emotional_depth": [
            "emotional", "cry", "tear-jerker", "touching", "sad", "melancholy", "heartbreaking",
            "wholesome", "feelings", "grief", "poignant", "heartfelt", "drama", "healing"
        ],
        "pacing": {
            "fast": ["fast-paced", "quick", "breakneck", "intense", "bingeable", "non-stop", "thrilling", "rapid"],
            "slow": ["slow-burn", "atmospheric", "meditative", "chill", "contemplative", "deliberate", "relaxing", "calm"]
        },
        "darkness": {
            "dark": ["dark", "gritty", "grimdark", "bloody", "mature", "seinen", "violent", "horror", "brutal", "disturbing", "cruel", "existential dread"],
            "light": ["lighthearted", "wholesome", "comedy", "funny", "cute", "cheerful", "uplifting", "feel-good", "pure", "cozy"]
        },
        "world_building": [
            "world-building", "lore", "immersion", "universe", "vast world", "fantasy world",
            "sci-fi universe", "cyberpunk city", "dystopia", "kingdom", "magic system"
        ],
        "philosophical": [
            "philosophical", "existential", "morality", "human condition", "ethics",
            "meaning of life", "nihilism", "society", "allegory", "deep themes", "thought-provoking"
        ]
    }

    GENRE_MAP = {
        "psychological": ["Psychological", "Thriller"],
        "thriller": ["Thriller", "Suspense"],
        "sci-fi": ["Sci-Fi", "Science Fiction"],
        "cyberpunk": ["Sci-Fi", "Action"],
        "action": ["Action", "Adventure"],
        "fantasy": ["Fantasy", "Adventure"],
        "mystery": ["Mystery", "Suspense"],
        "horror": ["Horror", "Supernatural"],
        "romance": ["Romance", "Drama"],
        "slice of life": ["Slice of Life"],
        "comedy": ["Comedy"],
        "sports": ["Sports"],
        "supernatural": ["Supernatural", "Fantasy"],
        "mecha": ["Mecha", "Sci-Fi"]
    }

    ARCHETYPE_PATTERNS = {
        "Anti-hero": ["anti-hero", "antihero", "morally grey", "ruthless", "villain protagonist", "dark protagonist"],
        "Mastermind / Strategist": ["mastermind", "strategist", "genius", "tactician", "calculating", "smart protagonist", "intelligent lead"],
        "Underdog": ["underdog", "hard work", "zero to hero", "struggling", "overcoming odds"],
        "Cynical Lone Wolf": ["lone wolf", "cynical", "stoic", "edgy", "isolated detective", "bounty hunter"],
        "Empathetic Leader": ["empathetic", "compassionate", "kind-hearted", "protecting friends", "inspiring leader"],
        "Overpowered (OP)": ["overpowered", "op protagonist", "god-like", "unstoppable"]
    }

    EPISODE_PATTERNS = [
        (r"(?:under|less than|fewer than|max|maximum of|<=)\s*(\d+)\s*(?:episodes|eps|ep)", "max"),
        (r"(\d+)\s*(?:episodes|eps|ep)\s*(?:or less|max)", "max"),
        (r"short\s*(?:anime|series)?", 13),
        (r"quick\s*binge", 13),
        (r"single\s*season", 25),
        (r"long\s*epic|long-running", 75)
    ]

    @classmethod
    def parse(cls, prompt: str) -> Tuple[AnimeDNAModel, Dict[str, Any]]:
        """
        Parses text prompt into an 8D AnimeDNAModel and extracted metadata.
        """
        if not prompt or not prompt.strip():
            # Return balanced defaults
            return AnimeDNAModel(), {
                "detected_genres": [],
                "detected_archetypes": [],
                "priority_dimensions": [],
                "max_episodes": None,
                "summary": "Balanced Exploration"
            }

        text = prompt.lower()

        # Initialize DNA dimensions at neutral 50.0
        dna_scores = {dim: 50.0 for dim in [
            "psychological", "action_intensity", "narrative_complexity",
            "emotional_depth", "pacing", "darkness", "world_building", "philosophical"
        ]}
        
        priority_dimensions = []
        detected_genres = []
        detected_archetypes = []
        max_episodes = None

        # 1. Parse Episodes
        for pattern in cls.EPISODE_PATTERNS:
            if isinstance(pattern, tuple) and pattern[1] == "max":
                match = re.search(pattern[0], text)
                if match:
                    max_episodes = int(match.group(1))
                    break
            elif isinstance(pattern, tuple):
                if re.search(pattern[0], text):
                    max_episodes = pattern[1]
                    break

        # 2. Parse Genres
        for genre_key, mapped in cls.GENRE_MAP.items():
            if re.search(r"\b" + re.escape(genre_key) + r"\b", text):
                for g in mapped:
                    if g not in detected_genres:
                        detected_genres.append(g)

        # 3. Parse Archetypes
        for arch, triggers in cls.ARCHETYPE_PATTERNS.items():
            if any(t in text for t in triggers):
                detected_archetypes.append(arch)

        # 4. Evaluate DNA Signals
        # Psychological
        if any(w in text for w in cls.DIMENSION_SIGNALS["psychological"]):
            dna_scores["psychological"] = 88.0
            priority_dimensions.append("psychological")

        # Action Intensity
        if any(w in text for w in cls.DIMENSION_SIGNALS["action_intensity"]):
            dna_scores["action_intensity"] = 85.0
            priority_dimensions.append("action_intensity")

        # Narrative Complexity
        if any(w in text for w in cls.DIMENSION_SIGNALS["narrative_complexity"]):
            dna_scores["narrative_complexity"] = 90.0
            priority_dimensions.append("narrative_complexity")

        # Emotional Depth
        if any(w in text for w in cls.DIMENSION_SIGNALS["emotional_depth"]):
            dna_scores["emotional_depth"] = 88.0
            priority_dimensions.append("emotional_depth")

        # World Building
        if any(w in text for w in cls.DIMENSION_SIGNALS["world_building"]):
            dna_scores["world_building"] = 88.0
            priority_dimensions.append("world_building")

        # Philosophical
        if any(w in text for w in cls.DIMENSION_SIGNALS["philosophical"]):
            dna_scores["philosophical"] = 86.0
            priority_dimensions.append("philosophical")

        # Pacing (fast vs slow)
        if any(w in text for w in cls.DIMENSION_SIGNALS["pacing"]["fast"]):
            dna_scores["pacing"] = 85.0
            priority_dimensions.append("pacing")
        elif any(w in text for w in cls.DIMENSION_SIGNALS["pacing"]["slow"]):
            dna_scores["pacing"] = 25.0
            priority_dimensions.append("pacing")

        # Darkness (dark vs light)
        if any(w in text for w in cls.DIMENSION_SIGNALS["darkness"]["dark"]):
            dna_scores["darkness"] = 86.0
            priority_dimensions.append("darkness")
        elif any(w in text for w in cls.DIMENSION_SIGNALS["darkness"]["light"]):
            dna_scores["darkness"] = 18.0
            priority_dimensions.append("darkness")

        # Specific combo heuristics
        if "mastermind" in text or "death note" in text or "code geass" in text or "battle of wits" in text:
            dna_scores["psychological"] = max(dna_scores["psychological"], 96.0)
            dna_scores["narrative_complexity"] = max(dna_scores["narrative_complexity"], 92.0)
            dna_scores["pacing"] = max(dna_scores["pacing"], 80.0)
            dna_scores["darkness"] = max(dna_scores["darkness"], 75.0)
            if "psychological" not in priority_dimensions:
                priority_dimensions.append("psychological")
            if "narrative_complexity" not in priority_dimensions:
                priority_dimensions.append("narrative_complexity")
            if "Mastermind / Strategist" not in detected_archetypes:
                detected_archetypes.append("Mastermind / Strategist")

        if "cyberpunk" in text:
            dna_scores["darkness"] = max(dna_scores["darkness"], 82.0)
            dna_scores["action_intensity"] = max(dna_scores["action_intensity"], 86.0)
            dna_scores["world_building"] = max(dna_scores["world_building"], 88.0)

        # Build clean summary narrative
        intent_parts = []
        if priority_dimensions:
            dim_names = [d.replace("_", " ").title() for d in priority_dimensions[:3]]
            intent_parts.append(f"Emphasizing {' + '.join(dim_names)}")
        if detected_archetypes:
            intent_parts.append(f"Protagonist: {', '.join(detected_archetypes)}")
        if max_episodes:
            intent_parts.append(f"Cap: ≤{max_episodes} eps")
        if detected_genres:
            intent_parts.append(f"Genres: {', '.join(detected_genres[:2])}")

        summary = " | ".join(intent_parts) if intent_parts else "Comprehensive Semantic Analysis"

        metadata = {
            "detected_genres": detected_genres,
            "detected_archetypes": detected_archetypes,
            "priority_dimensions": priority_dimensions,
            "max_episodes": max_episodes,
            "summary": summary
        }

        target_dna = AnimeDNAModel(**dna_scores)
        return target_dna, metadata
