# 🧬 AniVerse AI — Find the Anime That Matches Your Imagination

> **A Premium, AI-Powered Anime Discovery Platform & Anime DNA Engine**  
> *Built for a Winning Hackathon Submission & SaaS Commercialization.*

---

## 🌟 Executive Summary

Traditional anime recommendation systems suffer from severe **popularity bias** and **keyword brittleness**. Platforms like MyAnimeList, AniList, and streaming portals rely on shallow tags and community score sorting. If a user asks for:

> *"A dark psychological battle of wits with an intelligent mastermind protagonist and high stakes under 25 episodes"*

Conventional search engines fail completely, returning either empty lists or standard top 10 shonen titles.

**AniVerse AI** solves this problem by introducing the **Anime DNA Engine** — an interpretable, 8-dimensional mathematical vector representation of storytelling, psychology, tone, and pacing. AniVerse AI deconstructs natural language requests into structured multi-dimensional criteria, calculates vector resonance, explains *why* every title was recommended, and dynamically adapts to explicit user feedback.

---

## 🚀 Key Features & Innovations

### 1. 🧬 The Signature Innovation: Anime DNA Engine
Every anime narrative and viewer intent is projected into an **8-Dimensional Vector Space**:
1. **Psychological Mind Games**: Intellectual battles, deception, and mental tension.
2. **Action & Combat Intensity**: Kinetic sakuga, choreography, and explosive battles.
3. **Narrative Complexity**: Plot twists, non-linear timelines, and puzzle payoffs.
4. **Emotional Depth**: Vulnerability, grief, catharsis, and tear-jerker resonance.
5. **Pacing Momentum**: Continuum from atmospheric slow-burns to breakneck high-octane thrillers.
6. **Darkness / Grimdark Tone**: Continuum from pure wholesome comfort to mature existential dread.
7. **World Building & Immersion**: Expansive lore, cultural systems, and fantasy/sci-fi immersion.
8. **Philosophical Depth**: Existential ethics, morality, and the human condition.

**Similarity Metric**: Weighted hybrid blend of normalized **Cosine Similarity** (directional alignment) and **Euclidean Affinity** (intensity matching) with adaptive penalties for viewing commitment constraints.

### 2. 🤖 Natural Language Semantic Intent Parser
- Free-form text parser that extracts implicit genres, protagonist archetypes (*"Mastermind / Strategist"*, *"Anti-hero"*, *"Underdog"*, *"Cynical Lone Wolf"*), and strict episode constraints (*"under 25 episodes"*, *"single season"*, *"quick binge"*).
- Instant visual feedback displaying detected intent pills in the UI.

### 3. 🔍 Explainable AI (XAI)
- Transparent reasoning statements for every recommendation:
  - Compatibility score (e.g. `96% DNA Match`)
  - Dimensional breakdown bars for all 8 attributes
  - Highlights specific tropes, watch motivations, and viewing duration fit.

### 4. 🧪 Taste Cross-Referencing ("The DNA Taste Blender")
- Select 2 or 3 anchor titles (e.g., *Death Note* + *Cyberpunk: Edgerunners*) to synthesize their mathematical centroid in vector space.
- Discovers hidden gems located at the exact intersection of those narrative styles (e.g., *Psycho-Pass*).

### 5. ⏱️ Smart Binge Commitment Calculator & Watchlist
- Interactive watch-list manager with status filtering (*Plan to Watch*, *Watching*, *Completed*).
- **Binge Time Calculator**: Input your daily watch budget (e.g. 1.5 hours/day) and calculate total episodes, hours, days to finish, and daily episode milestones.
- **Milestone Calendar**: Predicted completion dates for each series.
- **Taste DNA Persona**: Aggregated Otaku Persona from watchlist titles (*Mastermind Chessmaster*, *Sakuga Hunter*, etc.).
- **Binge Fatigue Detector**: Detects cognitive strain from intense series and recommends palate cleansers.
- Export watchlist as JSON.

### 6. 🌐 Live Global MAL Search (Jikan API Integration)
- Search any anime title across the entire global MyAnimeList database with on-the-fly Anime DNA synthesis based on MAL genres, themes, and demographics.

### 7. 🏆 Interactive Hackathon Judge Pitch Mode
- Embedded 5-slide interactive presentation tour directly within the application covering Problem Statement, Signature Innovation, Vector Architecture, Tech Stack, and Monetization Roadmap.

### 8. ⚖️ Side-by-Side Anime DNA Comparator
- Compare any two anime side-by-side in 8-dimensional narrative space.
- Overlaid dual-polygon spider chart (Anime A in Cyan, Anime B in Neon Pink).
- Calculates exact narrative vector overlap percentage and produces dimension-by-dimension delta tables with automatic stylistic divergence explanations.

### 9. 🎯 30-Second Anime DNA Onboarding Quiz
- Intuitive 4-question wizard (*Atmosphere/Mood*, *Twist Complexity*, *Pacing Tempo*, *Viewing Commitment*).
- Instantly synthesizes an 8D Anime DNA vector and redirects to tailored recommendations with sub-millisecond response time.

### 10. 🎭 Character Archetypes & Dynamics Matrix
- Structured character archetype classification:
  - *Mastermind / Strategist* (Death Note, Code Geass, Monster)
  - *Anti-Hero* (Chainsaw Man, Attack on Titan, Vinland Saga)
  - *Underdog* (Mob Psycho 100, Bocchi the Rock!, Ping Pong)
  - *Cynical Lone Wolf* (Cowboy Bebop, Serial Experiments Lain)
  - *Empathetic Leader* (Frieren, A Silent Voice, Fullmetal Alchemist)
  - *Overpowered (OP)* (Mob Psycho 100, Frieren)
- Character Dynamics: *Cat & Mouse Battle of Wits*, *Mentor & Prodigy*, *Found Family in Dark World*, *Symbiotic Alter-Ego*.

### 11. 🎙️ Premium Audio & Dubbing Metadata Engine
- **Dub Tier Classification**: S-Tier Legendary, A-Tier Great, B-Tier Decent, Sub Recommended.
- **Full Dub & Sub Cast Listings**: English dub and Japanese sub voice actors for each curated entry.
- **Iconic Quotes**: Famous quotes with character attribution in both English and Japanese.
- **Soundtrack Genre**: Each title tagged with its musical identity (Gothic Orchestral, Synthwave, Chamber Noir, etc.).
- **Streaming Availability**: Platform badges (Netflix, Crunchyroll, Hulu).

### 12. 👑 Premium Collaboration Watch Rooms
- **Premium Subscription Gate**: Unlock collaborative features with a single click (demo mode).
- **Watch Room Creation**: Create named Watch Rooms and generate shareable invite links.
- **Friend Simulation**: Simulate friends joining with their own watchlists for demo purposes.
- **Watchlist Merging**: Automatically merge all members' watchlists into a unified shared list.
- **Vote-to-Watch-Next**: Each member can upvote titles — the shared list ranks by vote count.
- **Export Shared Watchlist**: Download the entire room's merged watchlist as JSON.
- **Member Avatars**: Color-coded member badges with initial-letter avatars.

---

## 🛠️ Technology Stack

| Layer | Technology |
|:---|:---|
| **Backend** | Python 3.13, FastAPI (ASGI async), Uvicorn, Pydantic V2 |
| **Vector Engine** | Pure high-performance Python mathematical engine (zero heavy binary deps) |
| **Frontend** | Modern ES6+ JavaScript, Responsive CSS3 Glassmorphism, HTML5 Canvas |
| **External API** | Jikan REST API (MyAnimeList open integration) |
| **Testing** | Python `unittest` — 12 automated tests covering vectors, NLP, ranking, feedback, dubbing, archetypes, and catalog diversity |

---

## 📦 Quick Start & Installation

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)

### Installation
```bash
# 1. Clone or open the repository
cd anime

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Run the automated unit tests
python -m unittest app/tests/test_engine.py -v

# 4. Launch the application
python run.py
```

Open your browser to:
- **Live Application**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Health Check**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## 📁 Project Structure

```
anime/
├── run.py                      # Application entry point with auto-port detection
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
├── .gitignore                  # Git ignore rules
├── app/
│   ├── __init__.py             # Package initializer
│   ├── main.py                 # FastAPI routes & endpoints (14 API routes)
│   ├── models.py               # Pydantic data models (AnimeDNA, AnimeItem, SearchQuery, etc.)
│   ├── dna_engine.py           # Core 8D vector engine (cosine, euclidean, blending, feedback)
│   ├── nlp_parser.py           # Natural language semantic intent parser
│   ├── external_api.py         # Jikan MAL API integration + dynamic DNA inference
│   ├── anime_database.py       # Curated anime catalog with 8D vectors & premium metadata
│   └── tests/
│       ├── __init__.py
│       └── test_engine.py      # 12 automated unit tests
└── static/
    ├── index.html              # Single-page application HTML (614 lines)
    ├── css/
    │   └── style.css           # Complete design system (1100+ lines)
    └── js/
        ├── app.js              # Core frontend controller (1200+ lines)
        ├── watchlist.js         # Watchlist manager + CollaborationManager (440+ lines)
        ├── dna_radar.js         # HTML5 Canvas 8-axis radar chart renderer
        └── pitch_mode.js        # Hackathon pitch overlay tour
```

---

## 🧪 Automated Test Suite

Run unit tests directly:
```bash
python -m unittest app/tests/test_engine.py -v
```

All **12 tests** pass with 100% success rate:

```
Ran 12 tests in 0.006s — OK

✓ test_dna_vector_serialization ........... 8D vector roundtrip fidelity
✓ test_nlp_parser_complex_query ........... Semantic dimension boosting & constraint parsing
✓ test_recommendation_ranking ............. Accurate ranking of psychological mastermind anime
✓ test_episode_constraint_enforcement ..... Validation of episode ceilings
✓ test_taste_cross_blending ............... Centroid discovery between disparate anime
✓ test_adaptive_feedback_loop ............. Taste vector evolution via exponential moving average
✓ test_anime_comparison ................... Side-by-side overlap scoring & divergence statements
✓ test_quiz_dna_synthesis ................. 4-question wizard translation to 8D vector
✓ test_dubbing_metadata_in_database ....... Premium dub tier, cast, quotes & soundtrack validation
✓ test_archetype_classification ........... NLP protagonist archetype pattern matching
✓ test_external_dna_inference ............. Jikan MAL dynamic DNA vector generation
✓ test_episode_diversity .................. Catalog variety (short/medium/long series mix)
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/api/health` | System health check and catalog size |
| `GET` | `/api/presets` | Demo preset prompts for hackathon judges |
| `GET` | `/api/anime` | Full anime catalog with optional filters |
| `GET` | `/api/anime/{id}` | Anime detail with DNA siblings |
| `GET` | `/api/user-profile` | Current adaptive user taste DNA vector |
| `GET` | `/api/archetypes` | Character archetype & dynamics matrix |
| `GET` | `/api/external/search?q=` | Live Jikan MAL search with DNA inference |
| `POST` | `/api/recommend` | AI-powered recommendation engine |
| `POST` | `/api/blend` | Taste cross-referencing centroid synthesis |
| `POST` | `/api/compare` | Side-by-side DNA differential analysis |
| `POST` | `/api/quiz` | 30-second onboarding quiz DNA synthesis |
| `POST` | `/api/feedback` | Adaptive taste profile evolution |

---

## 💼 Business Model & Monetization

1. **B2B Streaming Service Integration**: License the Anime DNA Engine SDK to streaming platforms (Crunchyroll, Netflix Anime, Hulu) to reduce catalog drop-off and boost binge completion.
2. **B2C Freemium SaaS (AniVerse Pro)**: \$4.99/month for Premium Watch Rooms, unlimited taste blending, AI episode companion notes, cross-platform watch history sync, and Discord bot integration.
3. **Market Size**: Global Anime Market was valued at **\$31.2 Billion in 2024**, projected to exceed **\$60 Billion by 2032** (CAGR 9.8%).

---

## 📜 License
Developed for Hackathon Exhibition & Open Innovation.
#   a n i m e - a i  
 #   a n i m e - a i  
 #   a n i m e - a i  
 #   a n i m e - a i  
 #   a n i m e - a i  
 