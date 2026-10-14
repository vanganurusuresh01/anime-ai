import os
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models import (
    AnimeItem, AnimeDNAModel, SearchQuery, MatchResult,
    RecommendationResponse, TasteCrossQuery, UserFeedback,
    CompareQuery, CompareResponse, QuizSubmission
)
from app.anime_database import AnimeDatabase
from app.dna_engine import AnimeDNAEngine
from app.nlp_parser import NLPSemanticParser
from app.external_api import search_jikan_anime

app = FastAPI(
    title="AniVerse AI",
    description="Find the anime that matches your imagination. AI-Powered Anime Discovery & Anime DNA Engine.",
    version="1.0.0"
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session user profile for dynamic learning
current_user_profile = AnimeDNAModel(
    psychological=65.0,
    action_intensity=60.0,
    narrative_complexity=70.0,
    emotional_depth=65.0,
    pacing=60.0,
    darkness=55.0,
    world_building=70.0,
    philosophical=65.0
)

# Demo Presets designed specifically for Hackathon Judges & Demos
DEMO_PRESETS = [
    {
        "id": "mastermind-short",
        "title": "Mastermind Mind Games (<25 eps)",
        "badge": "Psychological Battle",
        "prompt": "I want a dark psychological battle of wits with an intelligent mastermind protagonist and high stakes under 25 episodes."
    },
    {
        "id": "tear-jerker-wholesome",
        "title": "Emotional Tear-Jerker & Growth",
        "badge": "Heartfelt Resonance",
        "prompt": "Deeply emotional story about healing from grief, personal growth, and human empathy that will make me cry."
    },
    {
        "id": "cyberpunk-adrenaline",
        "title": "Breakneck Cyberpunk Adrenaline",
        "badge": "High-Octane Dystopia",
        "prompt": "Fast-paced adrenaline-fueled cyberpunk thriller with explosive action and morally grey mercenaries."
    },
    {
        "id": "slowburn-philosophical",
        "title": "Slow-Burn Philosophical Mystery",
        "badge": "Mind-Bending Lore",
        "prompt": "Atmospheric slow-burn mystery with deep world-building, philosophical exploration, and complex plot twists."
    },
    {
        "id": "underrated-gem",
        "title": "Underrated Avant-Garde Gem",
        "badge": "Unique Storytelling",
        "prompt": "Non-linear mind-bending storytelling with unique art style and existential themes under 15 episodes."
    }
]


@app.on_event("startup")
def startup_event():
    AnimeDatabase.initialize()


@app.get("/api/health")
def health_check():
    items = AnimeDatabase.get_all()
    return {
        "status": "healthy",
        "app": "AniVerse AI",
        "tagline": "Find the anime that matches your imagination",
        "total_catalog_size": len(items),
        "engine": "Anime DNA Engine v1.0",
        "dimensions": 8
    }


@app.get("/api/presets")
def get_demo_presets():
    return DEMO_PRESETS


@app.get("/api/user-profile")
def get_user_profile():
    return {
        "profile": current_user_profile,
        "vector": current_user_profile.to_vector()
    }


@app.get("/api/anime", response_model=List[AnimeItem])
def list_anime(
    genre: Optional[str] = None,
    max_episodes: Optional[int] = None,
    min_score: Optional[float] = None
):
    genres_filter = [genre] if genre else None
    return AnimeDatabase.filter_items(
        max_episodes=max_episodes,
        min_score=min_score,
        genres=genres_filter
    )


@app.get("/api/anime/{anime_id}")
def get_anime_details(anime_id: str):
    anime = AnimeDatabase.get_by_id(anime_id)
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")

    # Find top 4 closest DNA siblings
    all_anime = [a for a in AnimeDatabase.get_all() if a.id != anime_id]
    siblings = []
    for other in all_anime:
        sim, breakdown, aspects = AnimeDNAEngine.calculate_compatibility(
            anime.dna, other.dna
        )
        siblings.append({
            "anime": other,
            "similarity": sim,
            "shared_aspects": aspects
        })

    siblings.sort(key=lambda s: s["similarity"], reverse=True)

    return {
        "anime": anime,
        "dna_siblings": siblings[:4]
    }


@app.post("/api/recommend", response_model=RecommendationResponse)
def get_recommendations(query: SearchQuery):
    all_candidates = AnimeDatabase.get_all()

    # Step 1: Parse Natural Language Intent
    if query.dna_override:
        target_dna = query.dna_override
        intent = {
            "detected_genres": query.genre_filter or [],
            "detected_archetypes": query.archetype_filter or [],
            "priority_dimensions": [],
            "max_episodes": query.max_episodes,
            "summary": "Custom DNA Vector Calibration"
        }
    else:
        target_dna, intent = NLPSemanticParser.parse(query.prompt or "")
        # Merge manual filter overrides if provided
        if query.max_episodes:
            intent["max_episodes"] = query.max_episodes
        if query.genre_filter:
            intent["detected_genres"] = list(set(intent["detected_genres"] + query.genre_filter))

    # Step 2: Filter candidate pool
    filtered_pool = all_candidates
    if query.exclude_ids:
        filtered_pool = [a for a in filtered_pool if a.id not in query.exclude_ids]

    if query.min_score:
        filtered_pool = [a for a in filtered_pool if a.score >= query.min_score]

    # Step 3: Compute Anime DNA Compatibility Scores
    match_results: List[MatchResult] = []

    priority_dims = intent.get("priority_dimensions", [])
    max_eps = intent.get("max_episodes")

    for anime in filtered_pool:
        score, breakdown, matched_aspects = AnimeDNAEngine.calculate_compatibility(
            target_dna=target_dna,
            anime_dna=anime.dna,
            priority_dimensions=priority_dims,
            target_max_episodes=max_eps,
            anime_episodes=anime.episodes
        )

        # Soft boost if explicit genre match was extracted
        detected_genres = [g.lower() for g in intent.get("detected_genres", [])]
        if detected_genres and any(g.lower() in detected_genres for g in anime.genres):
            score = min(99.4, round(score + 3.5, 1))

        # Soft boost for archetype match
        detected_archetypes = intent.get("detected_archetypes", [])
        if detected_archetypes and any(arc in anime.archetypes for arc in detected_archetypes):
            score = min(99.4, round(score + 2.5, 1))

        ai_explanation = AnimeDNAEngine.generate_explanation(
            anime=anime,
            target_dna=target_dna,
            score=score,
            matched_aspects=matched_aspects,
            query_intent=intent
        )

        match_results.append(MatchResult(
            anime=anime,
            compatibility_score=score,
            breakdown=breakdown,
            ai_explanation=ai_explanation,
            matched_aspects=matched_aspects
        ))

    # Sort results
    if query.sort_by == "score":
        match_results.sort(key=lambda m: m.anime.score, reverse=True)
    elif query.sort_by == "episodes_asc":
        match_results.sort(key=lambda m: m.anime.episodes)
    else:
        match_results.sort(key=lambda m: m.compatibility_score, reverse=True)

    limit = query.limit or 15
    top_matches = match_results[:limit]

    # Generate dynamic refinement suggestions
    refinements = [
        "Dial up narrative complexity to find deeper plot twists",
        "Filter for series under 25 episodes for a weekend binge",
        "Cross-blend with your favorite thriller in the Taste Blender"
    ]

    return RecommendationResponse(
        query=query.prompt or "Direct DNA Profiler",
        extracted_intent=intent,
        target_dna=target_dna,
        total_matches=len(match_results),
        results=top_matches,
        suggested_refinements=refinements
    )


@app.post("/api/blend")
def blend_anime_tastes(query: TasteCrossQuery):
    """
    Signature Feature: Taste Cross-Referencing
    Takes 2 or 3 anime and discovers hidden gem titles residing at their exact DNA centroid.
    """
    if not query.anime_ids or len(query.anime_ids) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 anime IDs to cross-reference.")

    source_anime: List[AnimeItem] = []
    for aid in query.anime_ids:
        item = AnimeDatabase.get_by_id(aid)
        if item:
            source_anime.append(item)

    if len(source_anime) < 2:
        raise HTTPException(status_code=404, detail="Could not resolve selected anime in catalog.")

    # Synthesize blended DNA
    blended_dna = AnimeDNAEngine.blend_anime_dna(source_anime, query.weights)

    # Find closest matches excluding the source anime
    source_ids = {a.id for a in source_anime}
    candidates = [a for a in AnimeDatabase.get_all() if a.id not in source_ids]

    results = []
    for anime in candidates:
        score, breakdown, matched_aspects = AnimeDNAEngine.calculate_compatibility(
            target_dna=blended_dna,
            anime_dna=anime.dna
        )
        explanation = AnimeDNAEngine.generate_explanation(
            anime=anime,
            target_dna=blended_dna,
            score=score,
            matched_aspects=matched_aspects,
            query_intent={"summary": "Taste Cross-Referenced Centroid"}
        )
        results.append(MatchResult(
            anime=anime,
            compatibility_score=score,
            breakdown=breakdown,
            ai_explanation=explanation,
            matched_aspects=matched_aspects
        ))

    results.sort(key=lambda m: m.compatibility_score, reverse=True)
    limit = query.limit or 8

    return {
        "source_anime": source_anime,
        "blended_dna": blended_dna,
        "results": results[:limit]
    }


@app.post("/api/feedback")
def submit_feedback(feedback: UserFeedback):
    global current_user_profile
    anime = AnimeDatabase.get_by_id(feedback.anime_id)
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")

    old_profile = current_user_profile
    current_user_profile = AnimeDNAEngine.adapt_user_profile(
        current_profile=current_user_profile,
        anime=anime,
        action=feedback.action
    )

    return {
        "status": "success",
        "action": feedback.action,
        "anime_title": anime.title,
        "updated_profile": current_user_profile,
        "message": f"Taste DNA adapted dynamically based on '{feedback.action}' feedback."
    }


@app.get("/api/external/search")
def live_external_search(q: str = Query(..., min_length=2)):
    """
    Search any anime in existence via Jikan MAL API with real-time DNA vector synthesis.
    """
    live_results = search_jikan_anime(q)
    # Also index into in-memory database for seamless discovery and blends!
    for item in live_results:
        AnimeDatabase.add_or_update(item)
    return {"results": live_results}


@app.post("/api/compare", response_model=CompareResponse)
def compare_anime_pair(query: CompareQuery):
    a1 = AnimeDatabase.get_by_id(query.anime_id_1)
    a2 = AnimeDatabase.get_by_id(query.anime_id_2)
    if not a1 or not a2:
        raise HTTPException(status_code=404, detail="One or both anime could not be found.")

    comp = AnimeDNAEngine.compare_anime(a1, a2)
    return CompareResponse(**comp)


@app.post("/api/quiz", response_model=RecommendationResponse)
def submit_onboarding_quiz(quiz: QuizSubmission):
    dna, max_eps = AnimeDNAEngine.dna_from_quiz(
        mood=quiz.mood,
        pacing=quiz.pacing,
        complexity=quiz.complexity,
        episode_budget=quiz.episode_budget
    )

    query = SearchQuery(
        prompt=f"Onboarding Quiz Custom DNA ({quiz.mood.replace('_', ' ').title()})",
        dna_override=dna,
        max_episodes=max_eps,
        limit=12
    )
    return get_recommendations(query)


@app.get("/api/archetypes")
def get_character_archetypes():
    return {
        "archetypes": [
            {"id": "mastermind", "name": "Mastermind / Strategist", "desc": "Calculates every variable; intellectual chessmaster"},
            {"id": "anti-hero", "name": "Anti-Hero", "desc": "Morally grey, utilitarian, ruthlessly pragmatic"},
            {"id": "underdog", "name": "Underdog", "desc": "Constantly counted out; overcomes impossible odds"},
            {"id": "cynical-lone-wolf", "name": "Cynical Lone Wolf", "desc": "Detached observer driven by personal code"},
            {"id": "empathetic-leader", "name": "Empathetic Leader", "desc": "Draws strength from protecting comrades and humanity"},
            {"id": "overpowered", "name": "Overpowered (OP)", "desc": "God-tier abilities confronting existential ennui"}
        ],
        "character_dynamics": [
            {"id": "battle-of-wits", "name": "Cat & Mouse Battle of Wits", "example": "Death Note, Monster"},
            {"id": "mentor-student", "name": "Mentor & Prodigy", "example": "Mob Psycho 100, Vinland Saga"},
            {"id": "found-family", "name": "Found Family in Dark World", "example": "Cyberpunk: Edgerunners, Cowboy Bebop"},
            {"id": "reluctant-paragon", "name": "Reluctant Hero vs Inevitable Fate", "example": "Neon Genesis Evangelion, Steins;Gate"},
            {"id": "duality-symbiosis", "name": "Symbiotic Alter-Ego", "example": "Parasyte, Chainsaw Man"}
        ]
    }


# Mount Static Files (frontend)
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
def serve_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "message": "AniVerse AI Backend API is Running!",
        "docs": "/docs",
        "health": "/api/health"
    }
