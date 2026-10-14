import requests
from typing import List, Optional, Dict, Any
from app.models import AnimeItem, AnimeDNAModel

JIKAN_BASE_URL = "https://api.jikan.moe/v4"


def infer_dna_from_mal(item_data: Dict[str, Any]) -> AnimeDNAModel:
    """
    Dynamically generates an 8-dimensional Anime DNA vector from MyAnimeList metadata.
    """
    genres = [g.get("name", "").lower() for g in item_data.get("genres", [])]
    themes = [t.get("name", "").lower() for t in item_data.get("themes", [])]
    demographics = [d.get("name", "").lower() for d in item_data.get("demographics", [])]
    synopsis = (item_data.get("synopsis") or "").lower()

    all_tokens = genres + themes + demographics

    psychological = 45.0
    action_intensity = 50.0
    narrative_complexity = 50.0
    emotional_depth = 50.0
    pacing = 55.0
    darkness = 45.0
    world_building = 50.0
    philosophical = 45.0

    # Adjust based on keywords
    if "psychological" in all_tokens or "mind" in synopsis:
        psychological += 38.0
        narrative_complexity += 22.0

    if "action" in all_tokens or "combat" in synopsis or "martial arts" in all_tokens:
        action_intensity += 35.0
        pacing += 20.0

    if "mystery" in all_tokens or "detective" in all_tokens or "suspense" in all_tokens:
        narrative_complexity += 32.0
        psychological += 20.0

    if "drama" in all_tokens or "grief" in synopsis or "tear" in synopsis:
        emotional_depth += 35.0

    if "horror" in all_tokens or "gore" in all_tokens or "seinen" in all_tokens:
        darkness += 38.0
        psychological += 15.0

    if "sci-fi" in all_tokens or "fantasy" in all_tokens or "space" in all_tokens:
        world_building += 35.0
        philosophical += 15.0

    if "comedy" in all_tokens or "parody" in all_tokens:
        darkness = max(10.0, darkness - 25.0)
        pacing += 15.0

    # Clamp all to 10-99
    return AnimeDNAModel(
        psychological=min(99.0, max(10.0, round(psychological, 1))),
        action_intensity=min(99.0, max(10.0, round(action_intensity, 1))),
        narrative_complexity=min(99.0, max(10.0, round(narrative_complexity, 1))),
        emotional_depth=min(99.0, max(10.0, round(emotional_depth, 1))),
        pacing=min(99.0, max(10.0, round(pacing, 1))),
        darkness=min(99.0, max(10.0, round(darkness, 1))),
        world_building=min(99.0, max(10.0, round(world_building, 1))),
        philosophical=min(99.0, max(10.0, round(philosophical, 1)))
    )


def search_jikan_anime(query: str, limit: int = 6) -> List[AnimeItem]:
    """
    Queries Jikan MAL API and dynamically maps into AnimeItem with computed Anime DNA.
    """
    if not query or len(query.strip()) < 2:
        return []

    try:
        url = f"{JIKAN_BASE_URL}/anime"
        params = {"q": query, "limit": limit, "sfw": True}
        response = requests.get(url, params=params, timeout=4.0)
        if response.status_code != 200:
            return []

        data = response.json().get("data", [])
        results: List[AnimeItem] = []

        for item in data:
            item_id = f"mal-{item.get('mal_id')}"
            title = item.get("title") or "Unknown Title"
            title_jp = item.get("title_japanese") or ""
            synopsis = item.get("synopsis") or "No synopsis available."
            score = float(item.get("score") or 7.5)
            episodes = int(item.get("episodes") or 12)
            year = item.get("year") or 2020
            
            # Extract genres
            genres = [g.get("name") for g in item.get("genres", []) if g.get("name")]
            if not genres:
                genres = ["Animation"]

            # Image
            images = item.get("images", {})
            jpg_info = images.get("jpg", {})
            img_url = jpg_info.get("large_image_url") or jpg_info.get("image_url") or ""

            # Studios
            studios = item.get("studios", [])
            studio_name = studios[0].get("name") if studios else "Animation Studio"

            # Dynamic DNA inference
            dna = infer_dna_from_mal(item)

            anime = AnimeItem(
                id=item_id,
                title=title,
                title_jp=title_jp,
                synopsis=synopsis[:400] + ("..." if len(synopsis) > 400 else ""),
                image_url=img_url,
                score=score,
                episodes=episodes,
                year=year,
                studio=studio_name,
                genres=genres,
                tags=[t.get("name") for t in item.get("themes", []) if t.get("name")],
                archetypes=["Dynamic Character"],
                dna=dna,
                streaming=["Crunchyroll", "Official Platforms"],
                why_watch=f"Dynamic MAL entry indexed with {round(score, 1)}/10 community rating."
            )
            results.append(anime)

        return results
    except Exception:
        # Fallback cleanly on network timeout or rate limit
        return []
