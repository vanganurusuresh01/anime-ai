from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class AnimeDNAModel(BaseModel):
    """
    8-Dimensional Anime DNA Vector (values 0.0 to 100.0)
    Quantifies the narrative, psychological, and pacing signature of an anime.
    """
    psychological: float = Field(default=50.0, ge=0.0, le=100.0, description="Intellectual mind games, psychological tension")
    action_intensity: float = Field(default=50.0, ge=0.0, le=100.0, description="Combat, explosive kinetic motion, battles")
    narrative_complexity: float = Field(default=50.0, ge=0.0, le=100.0, description="Plot twists, non-linear storytelling, depth")
    emotional_depth: float = Field(default=50.0, ge=0.0, le=100.0, description="Emotional resonance, melancholy, character vulnerability")
    pacing: float = Field(default=50.0, ge=0.0, le=100.0, description="0=Atmospheric slow-burn, 100=Breakneck high-octane")
    darkness: float = Field(default=50.0, ge=0.0, le=100.0, description="0=Pure wholesome/light, 100=Grimdark, existential dread")
    world_building: float = Field(default=50.0, ge=0.0, le=100.0, description="Lore, immersion, vast distinct universe")
    philosophical: float = Field(default=50.0, ge=0.0, le=100.0, description="Existential questions, ethics, human condition")

    def to_vector(self) -> List[float]:
        return [
            self.psychological,
            self.action_intensity,
            self.narrative_complexity,
            self.emotional_depth,
            self.pacing,
            self.darkness,
            self.world_building,
            self.philosophical
        ]

    @classmethod
    def from_vector(cls, v: List[float]) -> "AnimeDNAModel":
        return cls(
            psychological=round(v[0], 1),
            action_intensity=round(v[1], 1),
            narrative_complexity=round(v[2], 1),
            emotional_depth=round(v[3], 1),
            pacing=round(v[4], 1),
            darkness=round(v[5], 1),
            world_building=round(v[6], 1),
            philosophical=round(v[7], 1)
        )


class AnimeItem(BaseModel):
    id: str
    title: str
    title_jp: Optional[str] = ""
    synopsis: str
    image_url: str
    banner_url: Optional[str] = ""
    score: float
    episodes: int
    duration_min: int = 24
    status: str = "Finished Airing"
    year: int
    season: Optional[str] = "All-Time"
    studio: str
    genres: List[str]
    tags: List[str] = []
    archetypes: List[str] = []
    character_dynamics: List[str] = []
    dna: AnimeDNAModel
    streaming: List[str] = ["Crunchyroll", "Netflix"]
    dub_tier: Optional[str] = "A-Tier Great"  # S-Tier Legendary, A-Tier Great, B-Tier Decent, Sub Recommended
    dub_cast: List[str] = []
    sub_cast: List[str] = []
    iconic_quote: Optional[Dict[str, str]] = None
    soundtrack_genre: Optional[str] = "Cinematic"
    why_watch: str
    rank: Optional[int] = None


class SearchQuery(BaseModel):
    prompt: Optional[str] = Field(default="", description="Natural language prompt")
    dna_override: Optional[AnimeDNAModel] = None
    max_episodes: Optional[int] = None
    min_score: Optional[float] = None
    genre_filter: Optional[List[str]] = None
    archetype_filter: Optional[List[str]] = None
    dub_tier_filter: Optional[str] = None
    sort_by: Optional[str] = "dna_match"  # dna_match, score, episodes_asc
    exclude_ids: Optional[List[str]] = []
    limit: Optional[int] = 15


class MatchResult(BaseModel):
    anime: AnimeItem
    compatibility_score: float  # 0 to 100%
    breakdown: Dict[str, float]
    ai_explanation: str
    matched_aspects: List[str]


class RecommendationResponse(BaseModel):
    query: str
    extracted_intent: Dict[str, Any]
    target_dna: AnimeDNAModel
    total_matches: int
    results: List[MatchResult]
    suggested_refinements: List[str]


class TasteCrossQuery(BaseModel):
    anime_ids: List[str]
    weights: Optional[List[float]] = None
    limit: Optional[int] = 10


class CompareQuery(BaseModel):
    anime_id_1: str
    anime_id_2: str


class CompareResponse(BaseModel):
    anime_1: AnimeItem
    anime_2: AnimeItem
    dna_1: AnimeDNAModel
    dna_2: AnimeDNAModel
    overlap_score: float
    dimension_deltas: Dict[str, float]
    comparison_summary: str
    divergence_highlights: List[str]


class QuizSubmission(BaseModel):
    mood: str
    pacing: str
    complexity: str
    episode_budget: str
    protagonist_preference: Optional[str] = "balanced"


class UserFeedback(BaseModel):
    anime_id: str
    action: str  # like, dislike, save, watchlist, completed
    comment: Optional[str] = None


class WatchlistEntry(BaseModel):
    anime_id: str
    status: str = "plan_to_watch"  # plan_to_watch, watching, completed, dropped
    current_episode: int = 0
    rating: Optional[float] = None
    added_at: Optional[str] = None
