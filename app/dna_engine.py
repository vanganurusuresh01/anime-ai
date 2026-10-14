import math
from typing import List, Dict, Tuple, Optional, Any
from app.models import AnimeDNAModel, AnimeItem, MatchResult


DIMENSION_NAMES = [
    "psychological",
    "action_intensity",
    "narrative_complexity",
    "emotional_depth",
    "pacing",
    "darkness",
    "world_building",
    "philosophical"
]

DIMENSION_LABELS = {
    "psychological": "Psychological Mind Games",
    "action_intensity": "Action & Combat Intensity",
    "narrative_complexity": "Plot Complexity & Twists",
    "emotional_depth": "Emotional Resonance",
    "pacing": "Pacing & Narrative Momentum",
    "darkness": "Grimdark / Mature Tone",
    "world_building": "World Building & Lore",
    "philosophical": "Philosophical & Existential Depth"
}


class AnimeDNAEngine:
    """
    The Signature Innovation: Anime DNA Engine
    Computes high-dimensional vector similarity, intent-weighted distance,
    and produces explainable AI recommendation breakdowns.
    """

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float], weights: Optional[List[float]] = None) -> float:
        """
        Compute weighted cosine similarity between two DNA vectors.
        Returns value between 0.0 and 1.0.
        """
        if weights is None:
            weights = [1.0] * len(v1)

        dot = 0.0
        norm1 = 0.0
        norm2 = 0.0

        for a, b, w in zip(v1, v2, weights):
            wa = a * w
            wb = b * w
            dot += wa * wb
            norm1 += wa * wa
            norm2 += wb * wb

        if norm1 <= 0.0 or norm2 <= 0.0:
            return 0.5

        sim = dot / (math.sqrt(norm1) * math.sqrt(norm2))
        return max(0.0, min(1.0, sim))

    @staticmethod
    def euclidean_affinity(v1: List[float], v2: List[float], weights: Optional[List[float]] = None) -> float:
        """
        Normalized Euclidean distance converted to affinity (0.0 to 1.0).
        Max possible distance in 8D 100-scale box is sqrt(8 * 100^2) = 282.84
        """
        if weights is None:
            weights = [1.0] * len(v1)

        total_weight = sum(weights)
        dist_sq = 0.0

        for a, b, w in zip(v1, v2, weights):
            diff = (a - b)
            dist_sq += w * (diff * diff)

        avg_dist = math.sqrt(dist_sq / total_weight)
        # 100 is max single-dimension distance
        affinity = 1.0 - (avg_dist / 100.0)
        return max(0.0, min(1.0, affinity))

    @classmethod
    def calculate_compatibility(
        cls,
        target_dna: AnimeDNAModel,
        anime_dna: AnimeDNAModel,
        priority_dimensions: Optional[List[str]] = None,
        target_max_episodes: Optional[int] = None,
        anime_episodes: Optional[int] = None
    ) -> Tuple[float, Dict[str, float], List[str]]:
        """
        Calculates compatibility score (0-100%), individual dimension match breakdown,
        and high-alignment callouts.
        """
        v_target = target_dna.to_vector()
        v_anime = anime_dna.to_vector()

        # Build dimension weights based on user emphasis
        weights = [1.0] * len(DIMENSION_NAMES)
        if priority_dimensions:
            for i, name in enumerate(DIMENSION_NAMES):
                if name in priority_dimensions:
                    weights[i] = 2.4  # boost priority dimensions significantly

        # Blend weighted Cosine (angle) and Euclidean (magnitude) affinities
        cos_sim = cls.cosine_similarity(v_target, v_anime, weights)
        euc_aff = cls.euclidean_affinity(v_target, v_anime, weights)
        raw_score = (cos_sim * 0.45 + euc_aff * 0.55) * 100.0

        # Episode commitment bonus or penalty
        if target_max_episodes and anime_episodes:
            if anime_episodes <= target_max_episodes:
                raw_score += 4.0  # reward meeting episode constraint
            else:
                # Moderate penalty for exceeding episode cap
                over = (anime_episodes - target_max_episodes) / target_max_episodes
                raw_score -= min(18.0, over * 15.0)

        # Dimension-by-dimension breakdown (100% - delta)
        breakdown: Dict[str, float] = {}
        matched_aspects: List[str] = []

        for name, t_val, a_val in zip(DIMENSION_NAMES, v_target, v_anime):
            delta = abs(t_val - a_val)
            dim_match = max(0.0, round(100.0 - delta, 1))
            breakdown[name] = dim_match

            # Identify standouts
            if dim_match >= 82.0 and (t_val >= 60.0 or (priority_dimensions and name in priority_dimensions)):
                matched_aspects.append(DIMENSION_LABELS.get(name, name))

        final_score = max(10.0, min(99.4, round(raw_score, 1)))
        return final_score, breakdown, matched_aspects

    @classmethod
    def generate_explanation(
        cls,
        anime: AnimeItem,
        target_dna: AnimeDNAModel,
        score: float,
        matched_aspects: List[str],
        query_intent: Dict[str, Any]
    ) -> str:
        """
        Generates an articulate, explainable AI narrative detailing why this anime matches.
        """
        phrases = []

        # Highlight primary DNA alignment
        top_dims = sorted(
            DIMENSION_NAMES,
            key=lambda d: getattr(anime.dna, d),
            reverse=True
        )[:2]

        dna_labels = [DIMENSION_LABELS[d] for d in top_dims]
        
        if score >= 90:
            fit_desc = "Exceptional direct resonance"
        elif score >= 80:
            fit_desc = "Strong thematic alignment"
        else:
            fit_desc = "Compelling alternative with shared DNA"

        # Check episode fit
        ep_text = f"{anime.episodes} episodes" if anime.episodes > 1 else "Film"
        
        # Check archetypes
        archetype_text = f"featuring {', '.join(anime.archetypes[:2])}" if anime.archetypes else ""

        # Construct concise, impressive narrative
        aspects_str = ", ".join(matched_aspects[:2]) if matched_aspects else dna_labels[0]
        
        explanation = (
            f"{fit_desc} ({score}% match). Dominates in {aspects_str}. "
            f"Delivers a {anime.why_watch} ({ep_text}{f', {archetype_text}' if archetype_text else ''})."
        )
        return explanation

    @classmethod
    def blend_anime_dna(cls, anime_list: List[AnimeItem], weights: Optional[List[float]] = None) -> AnimeDNAModel:
        """
        Synthesize a hybrid DNA vector from multiple anime (Taste Cross-Referencing).
        """
        if not anime_list:
            return AnimeDNAModel()

        if weights is None or len(weights) != len(anime_list):
            weights = [1.0 / len(anime_list)] * len(anime_list)
        else:
            total = sum(weights) or 1.0
            weights = [w / total for w in weights]

        blended_vector = [0.0] * len(DIMENSION_NAMES)

        for anime, weight in zip(anime_list, weights):
            vec = anime.dna.to_vector()
            for i in range(len(DIMENSION_NAMES)):
                blended_vector[i] += vec[i] * weight

        return AnimeDNAModel.from_vector(blended_vector)

    @classmethod
    def adapt_user_profile(
        cls,
        current_profile: AnimeDNAModel,
        anime: AnimeItem,
        action: str
    ) -> AnimeDNAModel:
        """
        Evolves user taste vector dynamically with exponential moving average:
        - 'like' / 'watchlist' nudges target profile closer (alpha = 0.15)
        - 'dislike' nudges target profile slightly away (alpha = -0.10)
        """
        alpha_map = {
            "like": 0.18,
            "save": 0.15,
            "watchlist": 0.15,
            "completed": 0.10,
            "dislike": -0.10
        }
        alpha = alpha_map.get(action.lower(), 0.0)
        if alpha == 0.0:
            return current_profile

        curr_vec = current_profile.to_vector()
        anime_vec = anime.dna.to_vector()

        updated_vec = []
        for c, a in zip(curr_vec, anime_vec):
            if alpha > 0:
                new_val = c * (1.0 - alpha) + a * alpha
            else:
                # Nudge away from disliked anime
                diff = c - a
                new_val = c + (diff * abs(alpha) * 0.5)
            updated_vec.append(max(0.0, min(100.0, new_val)))

        return AnimeDNAModel.from_vector(updated_vec)

    @classmethod
    def compare_anime(cls, a1: AnimeItem, a2: AnimeItem) -> Dict[str, Any]:
        """
        Calculates side-by-side vector differences, overall overlap percentage,
        and generates an explainable differential report.
        """
        v1 = a1.dna.to_vector()
        v2 = a2.dna.to_vector()

        deltas: Dict[str, float] = {}
        divergences: List[str] = []

        for name, val1, val2 in zip(DIMENSION_NAMES, v1, v2):
            diff = round(val1 - val2, 1)
            deltas[name] = diff
            label = DIMENSION_LABELS.get(name, name)
            if abs(diff) >= 20.0:
                higher_title = a1.title if diff > 0 else a2.title
                divergences.append(f"{higher_title} leads by {abs(diff)}% in {label}")

        overlap = cls.cosine_similarity(v1, v2) * 100.0
        overlap_score = round(overlap, 1)

        summary = (
            f"{a1.title} and {a2.title} share a {overlap_score}% narrative vector overlap. "
            f"Both resonate strongly in {DIMENSION_LABELS[max(DIMENSION_NAMES, key=lambda d: getattr(a1.dna, d))]}. "
            f"Key divergence: {divergences[0] if divergences else 'Remarkably balanced parity across all axes'}."
        )

        return {
            "anime_1": a1,
            "anime_2": a2,
            "dna_1": a1.dna,
            "dna_2": a2.dna,
            "overlap_score": overlap_score,
            "dimension_deltas": deltas,
            "comparison_summary": summary,
            "divergence_highlights": divergences[:4]
        }

    @classmethod
    def dna_from_quiz(cls, mood: str, pacing: str, complexity: str, episode_budget: str) -> Tuple[AnimeDNAModel, Optional[int]]:
        """
        Translates interactive onboarding quiz choices into an 8D Anime DNA vector
        and target episode limit.
        """
        # Base neutral
        scores = {dim: 50.0 for dim in DIMENSION_NAMES}

        # Mood handling
        if mood == "mind_games":
            scores["psychological"] = 95.0
            scores["narrative_complexity"] = 90.0
            scores["darkness"] = 75.0
            scores["pacing"] = 80.0
        elif mood == "hype_action":
            scores["action_intensity"] = 98.0
            scores["pacing"] = 90.0
            scores["darkness"] = 65.0
        elif mood == "emotional_journey":
            scores["emotional_depth"] = 98.0
            scores["philosophical"] = 85.0
            scores["darkness"] = 40.0
            scores["pacing"] = 55.0
        elif mood == "deep_mystery":
            scores["narrative_complexity"] = 96.0
            scores["world_building"] = 92.0
            scores["philosophical"] = 90.0
            scores["pacing"] = 60.0
        elif mood == "chill_wholesome":
            scores["darkness"] = 15.0
            scores["emotional_depth"] = 80.0
            scores["pacing"] = 70.0
            scores["action_intensity"] = 25.0

        # Pacing adjustment
        if pacing == "slow_burn":
            scores["pacing"] = min(scores["pacing"], 35.0)
            scores["world_building"] = max(scores["world_building"], 85.0)
        elif pacing == "breakneck":
            scores["pacing"] = max(scores["pacing"], 92.0)

        # Complexity adjustment
        if complexity == "mind_bending":
            scores["narrative_complexity"] = max(scores["narrative_complexity"], 95.0)
            scores["philosophical"] = max(scores["philosophical"], 88.0)
        elif complexity == "straightforward":
            scores["narrative_complexity"] = min(scores["narrative_complexity"], 50.0)

        # Episode budget
        max_eps = None
        if episode_budget == "under_13":
            max_eps = 13
        elif episode_budget == "under_26":
            max_eps = 26
        elif episode_budget == "long_epic":
            max_eps = None  # open, but world-building boosted
            scores["world_building"] = max(scores["world_building"], 95.0)

        return AnimeDNAModel(**scores), max_eps
