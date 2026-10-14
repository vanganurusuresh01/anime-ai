from typing import List, Dict, Optional
from app.models import AnimeItem, AnimeDNAModel

# Curated High-Res Anime Database with 8-Dimensional DNA Vectors
RAW_ANIME_DATA: List[Dict] = [
    {
        "id": "death-note",
        "title": "Death Note",
        "title_jp": "デスノート",
        "synopsis": "An intelligent high school student discovers a supernatural notebook that grants the power to kill anyone whose name is written in it. As he cleanses the world of criminals under the moniker 'Kira', an enigmatic genius detective known only as 'L' begins a relentless battle of wits.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1079/138100.jpg",
        "banner_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=1200&auto=format&fit=crop&q=80",
        "score": 8.62,
        "episodes": 37,
        "duration_min": 23,
        "year": 2006,
        "season": "Fall",
        "studio": "Madhouse",
        "genres": ["Psychological", "Thriller", "Supernatural", "Mystery"],
        "tags": ["Cat and Mouse", "God Complex", "Detective", "Mind Games"],
        "archetypes": ["Anti-hero", "Mastermind / Strategist"],
        "dna": {
            "psychological": 98.0,
            "action_intensity": 42.0,
            "narrative_complexity": 91.0,
            "emotional_depth": 55.0,
            "pacing": 88.0,
            "darkness": 84.0,
            "world_building": 62.0,
            "philosophical": 82.0
        },
        "streaming": ["Netflix", "Crunchyroll", "Hulu"],
        "dub_tier": "S-Tier Legendary",
        "dub_cast": ["Brad Swaile (Light)", "Alessandro Juliani (L)", "Brian Drummond (Ryuk)"],
        "sub_cast": ["Mamoru Miyano", "Kappei Yamaguchi"],
        "iconic_quote": {
            "speaker": "Light Yagami",
            "en": "I'll take a potato chip... and EAT IT!",
            "jp": "ポテトチップスを食べてやる！"
        },
        "soundtrack_genre": "Gothic Orchestral",
        "why_watch": "The quintessential psychological cat-and-mouse duel that redefines tactical mind games."
    },
    {
        "id": "monster",
        "title": "Monster",
        "title_jp": "モンスター",
        "synopsis": "Dr. Kenzo Tenma, an elite neurosurgeon in Germany, risks his prestige to save the life of a dying young boy instead of the town mayor. Years later, he discovers the boy grew up to become a terrifying, charismatic sociopathic mastermind responsible for monstrous crimes.",
        "image_url": "https://cdn.myanimelist.net/images/anime/10/66831.jpg",
        "banner_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=1200&auto=format&fit=crop&q=80",
        "score": 8.88,
        "episodes": 74,
        "duration_min": 24,
        "year": 2004,
        "season": "Spring",
        "studio": "Madhouse",
        "genres": ["Psychological", "Mystery", "Thriller", "Seinen"],
        "tags": ["Doctor", "Sociopath", "Cold War Europe", "Moral Dilemma"],
        "archetypes": ["Empathetic Leader", "Cynical Lone Wolf"],
        "dna": {
            "psychological": 99.0,
            "action_intensity": 35.0,
            "narrative_complexity": 96.0,
            "emotional_depth": 88.0,
            "pacing": 38.0,
            "darkness": 92.0,
            "world_building": 89.0,
            "philosophical": 97.0
        },
        "streaming": ["Netflix"],
        "dub_tier": "S-Tier Legendary",
        "dub_cast": ["Liam O'Brien (Dr. Tenma)", "Keith Silverstein (Johan Liebert)", "Karen Strassman (Nina)"],
        "sub_cast": ["Hidenobu Kiuchi", "Tsutomu Isobe"],
        "iconic_quote": {
            "speaker": "Johan Liebert",
            "en": "Tell me, what do you think is the ultimate fear?",
            "jp": "教えてくれ、本当の恐怖とは何だと思う？"
        },
        "soundtrack_genre": "Chamber Noir",
        "why_watch": "A slow-burn, masterclass psychological noir dissecting evil, morality, and human redemption."
    },
    {
        "id": "steins-gate",
        "title": "Steins;Gate",
        "title_jp": "シュタインズ・ゲート",
        "synopsis": "Eccentric self-proclaimed mad scientist Rintaro Okabe accidentally discovers that his modified microwave can send text messages into the past. Tampering with the timeline triggers a cascade of catastrophic consequences from shadowy global organizations.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1935/127974.jpg",
        "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200&auto=format&fit=crop&q=80",
        "score": 9.07,
        "episodes": 24,
        "duration_min": 24,
        "year": 2011,
        "season": "Spring",
        "studio": "White Fox",
        "genres": ["Sci-Fi", "Thriller", "Psychological", "Mystery"],
        "tags": ["Time Travel", "Butterfly Effect", "Conspiracy", "Akihabara"],
        "archetypes": ["Mastermind / Strategist", "Empathetic Leader"],
        "dna": {
            "psychological": 93.0,
            "action_intensity": 40.0,
            "narrative_complexity": 97.0,
            "emotional_depth": 92.0,
            "pacing": 72.0,
            "darkness": 76.0,
            "world_building": 84.0,
            "philosophical": 85.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "dub_tier": "S-Tier Legendary",
        "dub_cast": ["J. Michael Tatum (Okabe)", "Trina Nishimura (Kurisu)", "Cherami Leigh (Suzuha)"],
        "sub_cast": ["Mamoru Miyano", "Asami Imai", "Kana Hanazawa"],
        "iconic_quote": {
            "speaker": "Rintaro Okabe",
            "en": "I am the great mad scientist, Hououin Kyouma! El Psy Kongroo.",
            "jp": "狂気のマッドサイエンティスト、鳳凰院凶真だ！エル・プサイ・コングルゥ。"
        },
        "soundtrack_genre": "Synth Mystery",
        "why_watch": "The gold standard of time-travel thrillers with heartbreaking stakes and mind-bending puzzle payoffs."
    },
    {
        "id": "psycho-pass",
        "title": "Psycho-Pass",
        "title_jp": "サイコパス",
        "synopsis": "In a 22nd-century dystopian Tokyo, the Sibyl System quantifies the mental state and criminal intent (Crime Coefficient) of every citizen. Rookie inspector Akane Tsunemori and Enforcer Shinya Kogami confront an elusive criminal mastermind who can bypass the system.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1522/119999.jpg",
        "banner_url": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1200&auto=format&fit=crop&q=80",
        "score": 8.33,
        "episodes": 22,
        "duration_min": 23,
        "year": 2012,
        "season": "Fall",
        "studio": "Production I.G",
        "genres": ["Action", "Sci-Fi", "Psychological", "Suspense"],
        "tags": ["Cyberpunk", "Dystopia", "Detective", "Free Will"],
        "archetypes": ["Cynical Lone Wolf", "Empathetic Leader"],
        "dna": {
            "psychological": 91.0,
            "action_intensity": 78.0,
            "narrative_complexity": 86.0,
            "emotional_depth": 74.0,
            "pacing": 82.0,
            "darkness": 87.0,
            "world_building": 92.0,
            "philosophical": 93.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "dub_tier": "A-Tier Great",
        "dub_cast": ["Robert McCollum (Kogami)", "Kate Oxley (Akane)", "Alex Organ (Makishima)"],
        "sub_cast": ["Tomokazu Seki", "Kana Hanazawa", "Takahiro Sakurai"],
        "iconic_quote": {
            "speaker": "Shinya Kogami",
            "en": "Law doesn't protect people. People protect the law.",
            "jp": "法が人を守るんじゃない。人が法を守るんだ。"
        },
        "soundtrack_genre": "Industrial Cyberpunk",
        "why_watch": "A gritty cyberpunk crime procedural tackling utilitarianism, authoritarianism, and moral conviction."
    },
    {
        "id": "cyberpunk-edgerunners",
        "title": "Cyberpunk: Edgerunners",
        "title_jp": "サイバーパンク エッジランナーズ",
        "synopsis": "In Night City, a street kid named David Martinez loses everything in a drive-by shooting and chooses to survive by getting military-grade cyberware implanted, transforming into a mercenary outlaw (Edgerunner) alongside the enigmatic netrunner Lucy.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1818/126435.jpg",
        "banner_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1200&auto=format&fit=crop&q=80",
        "score": 8.60,
        "episodes": 10,
        "duration_min": 24,
        "year": 2022,
        "season": "Summer",
        "studio": "Trigger",
        "genres": ["Action", "Sci-Fi", "Drama"],
        "tags": ["Cyberpunk", "Dystopia", "High Octane", "Tragic Romance"],
        "archetypes": ["Underdog", "Anti-hero"],
        "dna": {
            "psychological": 78.0,
            "action_intensity": 98.0,
            "narrative_complexity": 72.0,
            "emotional_depth": 91.0,
            "pacing": 96.0,
            "darkness": 90.0,
            "world_building": 94.0,
            "philosophical": 74.0
        },
        "streaming": ["Netflix"],
        "dub_tier": "S-Tier Legendary",
        "dub_cast": ["Zach Aguilar (David)", "Giancarlo Esposito (Faraday)", "Alex Cazares (Rebecca)"],
        "sub_cast": ["KENN", "Aoi Yuuki", "Hiroki Touchi"],
        "iconic_quote": {
            "speaker": "David Martinez",
            "en": "I'm built different. I'm taking you to the moon.",
            "jp": "俺は特別なんだ。君を月に連れて行く。"
        },
        "soundtrack_genre": "Synthwave Cyberpunk",
        "why_watch": "A 10-episode adrenaline shot of breathtaking Trigger animation, tragic romance, and neon chaos."
    },
    {
        "id": "odd-taxi",
        "title": "Odd Taxi",
        "title_jp": "オッドタクシー",
        "synopsis": "Hiroshi Odokawa, an eccentric and solitary 41-year-old walrus taxi driver, leads a quiet life. Through mundane conversations with diverse passengers, he unwittingly becomes tangled in the disappearance of a high school girl involving the yakuza, idols, and crooked cops.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1985/115805.jpg",
        "banner_url": "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1200&auto=format&fit=crop&q=80",
        "score": 8.67,
        "episodes": 13,
        "duration_min": 23,
        "year": 2021,
        "season": "Spring",
        "studio": "OLM / P.I.C.S.",
        "genres": ["Mystery", "Psychological", "Suspense"],
        "tags": ["Anthropomorphic", "Interlocking Narratives", "Quentin Tarantino style", "Subtle Clues"],
        "archetypes": ["Cynical Lone Wolf", "Mastermind / Strategist"],
        "dna": {
            "psychological": 90.0,
            "action_intensity": 36.0,
            "narrative_complexity": 95.0,
            "emotional_depth": 80.0,
            "pacing": 76.0,
            "darkness": 70.0,
            "world_building": 82.0,
            "philosophical": 84.0
        },
        "streaming": ["Crunchyroll"],
        "dub_tier": "A-Tier Great",
        "dub_cast": ["Mike McFarland (Odokawa)"],
        "sub_cast": ["Natsuki Hanae (Odokawa)"],
        "iconic_quote": {
            "speaker": "Odokawa",
            "en": "Everyone is hiding something behind the steering wheel.",
            "jp": "誰もがハンドルの向こうに何かを隠している。"
        },
        "soundtrack_genre": "City Pop & Hip Hop",
        "why_watch": "A razor-sharp dialogue-driven mystery where every single throwaway line is a clue to a stunning finale."
    },
    {
        "id": "vinland-saga",
        "title": "Vinland Saga",
        "title_jp": "ヴィンランド・サガ",
        "synopsis": "Raised by the Viking mercenary band that murdered his father, young Thorfinn dedicates his life to vengeance against commander Askeladd. As political turmoil engulfs 11th-century England, Thorfinn is dragged into the bloody battle for the English crown.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1500/103005.jpg",
        "banner_url": "https://images.unsplash.com/photo-1533240332313-0db49b459ad6?w=1200&auto=format&fit=crop&q=80",
        "score": 8.76,
        "episodes": 48,
        "duration_min": 24,
        "year": 2019,
        "season": "Summer",
        "studio": "WIT Studio / MAPPA",
        "genres": ["Action", "Adventure", "Drama", "Seinen"],
        "tags": ["Vikings", "Historical", "Revenge", "Pacifism"],
        "archetypes": ["Anti-hero", "Mastermind / Strategist"],
        "dna": {
            "psychological": 89.0,
            "action_intensity": 92.0,
            "narrative_complexity": 88.0,
            "emotional_depth": 94.0,
            "pacing": 68.0,
            "darkness": 88.0,
            "world_building": 93.0,
            "philosophical": 95.0
        },
        "streaming": ["Netflix", "Crunchyroll", "Amazon Prime"],
        "dub_tier": "S-Tier Legendary",
        "dub_cast": ["Kirk Thornton (Askeladd)", "Aleks Le (Thorfinn)", "Patrick Seitz (Thorkell)"],
        "sub_cast": ["Naoya Uchida (Askeladd)", "Yuto Uemura (Thorfinn)"],
        "iconic_quote": {
            "speaker": "Askeladd",
            "en": "Everyone is a slave to something. Even you.",
            "jp": "誰しも何かの奴隷だ。お前もな。"
        },
        "soundtrack_genre": "Norse Folk Orchestral",
        "why_watch": "An epic historical saga that evolves from brutal bloodletting revenge into an unparalleled treatise on peace."
    },
    {
        "id": "frieren",
        "title": "Frieren: Beyond Journey's End",
        "title_jp": "葬送のフリーレン",
        "synopsis": "The elven mage Frieren and her party defeated the Demon King, bringing peace to the land. But for an elf who lives thousands of years, her human companions age and pass away in what feels like moments. Frieren sets out on a journey of discovery to understand the human heart.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1015/138006.jpg",
        "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200&auto=format&fit=crop&q=80",
        "score": 9.32,
        "episodes": 28,
        "duration_min": 24,
        "year": 2023,
        "season": "Fall",
        "studio": "Madhouse",
        "genres": ["Adventure", "Drama", "Fantasy"],
        "tags": ["Elves", "Passing of Time", "Poignant", "Magical Battles"],
        "archetypes": ["Empathetic Leader", "Overpowered (OP)"],
        "dna": {
            "psychological": 76.0,
            "action_intensity": 70.0,
            "narrative_complexity": 78.0,
            "emotional_depth": 97.0,
            "pacing": 46.0,
            "darkness": 32.0,
            "world_building": 96.0,
            "philosophical": 94.0
        },
        "streaming": ["Crunchyroll"],
        "dub_tier": "S-Tier Legendary",
        "dub_cast": ["Mallorie Rodak (Frieren)", "Jill Harris (Fern)", "Clifford Chapin (Stark)"],
        "sub_cast": ["Atsumi Tanezaki (Frieren)", "Kana Ichinose (Fern)"],
        "iconic_quote": {
            "speaker": "Frieren",
            "en": "Aura, kill yourself.",
            "jp": "アウラ、自害しろ。"
        },
        "soundtrack_genre": "Celtic Fantasy",
        "why_watch": "The highest-rated fantasy anime of all time; a deeply melancholic, gorgeous contemplation on memory and love."
    },
    {
        "id": "shinsekai-yori",
        "title": "From the New World (Shinsekai Yori)",
        "title_jp": "新世界より",
        "synopsis": "A millennium into the future, humans possess god-like psychokinetic powers (Cantus) and live in pastoral villages. When five children discover ancient automated libraries, they unravel the horrific dark secrets that underpin their utopian society.",
        "image_url": "https://cdn.myanimelist.net/images/anime/12/43971.jpg",
        "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200&auto=format&fit=crop&q=80",
        "score": 8.28,
        "episodes": 25,
        "duration_min": 23,
        "year": 2012,
        "season": "Fall",
        "studio": "A-1 Pictures",
        "genres": ["Drama", "Horror", "Mystery", "Psychological", "Sci-Fi"],
        "tags": ["Dystopia", "Psychic Powers", "Utopia Secret", "Coming of Age"],
        "archetypes": ["Empathetic Leader"],
        "dna": {
            "psychological": 95.0,
            "action_intensity": 62.0,
            "narrative_complexity": 94.0,
            "emotional_depth": 87.0,
            "pacing": 54.0,
            "darkness": 91.0,
            "world_building": 98.0,
            "philosophical": 96.0
        },
        "streaming": ["Crunchyroll", "HIDIVE"],
        "why_watch": "An atmospheric, chilling sci-fi masterpiece with peerless world-building and a profound ethical dilemma."
    },
    {
        "id": "erased",
        "title": "ERASED (Boku dake ga Inai Machi)",
        "title_jp": "僕だけがいない街",
        "synopsis": "Struggling manga artist Satoru Fujinuma possesses 'Revival'—an uncontrollable phenomenon that rewinds time right before a disaster. When his mother is murdered, he is sent back 18 years to his elementary school days to prevent the serial abduction of three classmates.",
        "image_url": "https://cdn.myanimelist.net/images/anime/10/77957.jpg",
        "banner_url": "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1200&auto=format&fit=crop&q=80",
        "score": 8.29,
        "episodes": 12,
        "duration_min": 23,
        "year": 2016,
        "season": "Winter",
        "studio": "A-1 Pictures",
        "genres": ["Mystery", "Psychological", "Supernatural", "Suspense"],
        "tags": ["Time Leap", "Serial Killer", "Childhood Rescue", "Emotional"],
        "archetypes": ["Underdog", "Empathetic Leader"],
        "dna": {
            "psychological": 88.0,
            "action_intensity": 48.0,
            "narrative_complexity": 84.0,
            "emotional_depth": 89.0,
            "pacing": 92.0,
            "darkness": 78.0,
            "world_building": 64.0,
            "philosophical": 72.0
        },
        "streaming": ["Netflix", "Crunchyroll", "Hulu"],
        "why_watch": "A heart-pounding 12-episode mystery thriller you can binge in a single day with immense emotional payoff."
    },
    {
        "id": "neon-genesis-evangelion",
        "title": "Neon Genesis Evangelion",
        "title_jp": "新世紀エヴァンゲリオン",
        "synopsis": "In a post-apocalyptic Tokyo-3, humanity is attacked by monstrous otherworldly beings called Angels. Fourteen-year-old Shinji Ikari is summoned by his estranged father to pilot Evangelion Unit-01, descending into intense existential trauma, psychoanalysis, and theological dread.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1314/108941.jpg",
        "banner_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=1200&auto=format&fit=crop&q=80",
        "score": 8.36,
        "episodes": 26,
        "duration_min": 24,
        "year": 1995,
        "season": "Fall",
        "studio": "Gainax",
        "genres": ["Action", "Drama", "Mecha", "Psychological", "Sci-Fi"],
        "tags": ["Hedgehog Dilemma", "Depression", "Angels", "Cult Classic"],
        "archetypes": ["Underdog", "Cynical Lone Wolf"],
        "dna": {
            "psychological": 99.0,
            "action_intensity": 75.0,
            "narrative_complexity": 96.0,
            "emotional_depth": 95.0,
            "pacing": 62.0,
            "darkness": 93.0,
            "world_building": 92.0,
            "philosophical": 99.0
        },
        "streaming": ["Netflix"],
        "why_watch": "The landmark psychological masterpiece that deconstructed mecha and pioneered deep psychological introspection in anime."
    },
    {
        "id": "madoka-magica",
        "title": "Puella Magi Madoka Magica",
        "title_jp": "魔法少女まどか☆マギカ",
        "synopsis": "Middle-schooler Madoka Kaname is offered a Faustian bargain by a mysterious cat-like creature named Kyubey: have any wish granted in exchange for becoming a magical girl to fight witches. But the reality of magical girls is filled with despair, entropy, and sacrifice.",
        "image_url": "https://cdn.myanimelist.net/images/anime/11/55225.jpg",
        "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200&auto=format&fit=crop&q=80",
        "score": 8.35,
        "episodes": 12,
        "duration_min": 24,
        "year": 2011,
        "season": "Winter",
        "studio": "Shaft",
        "genres": ["Drama", "Fantasy", "Psychological", "Suspense"],
        "tags": ["Deconstruction", "Dark Fantasy", "Time Loop", "Tragic"],
        "archetypes": ["Underdog", "Mastermind / Strategist"],
        "dna": {
            "psychological": 94.0,
            "action_intensity": 76.0,
            "narrative_complexity": 92.0,
            "emotional_depth": 93.0,
            "pacing": 88.0,
            "darkness": 89.0,
            "world_building": 80.0,
            "philosophical": 90.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "why_watch": "A legendary 12-episode subversion written by Gen Urobuchi that turns the magical girl genre on its head."
    },
    {
        "id": "parasyte",
        "title": "Parasyte -the maxim-",
        "title_jp": "寄生獣 セイの格率",
        "synopsis": "Alien parasitic creatures descend onto Earth, burrowing into human heads to hijack their brains. High schooler Shinichi Izumi manages to restrict a parasite to his right hand (Migi). Trapped in symbiosis, they must fight hostile parasites while Shinichi questions his own humanity.",
        "image_url": "https://cdn.myanimelist.net/images/anime/3/73178.jpg",
        "banner_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=1200&auto=format&fit=crop&q=80",
        "score": 8.33,
        "episodes": 24,
        "duration_min": 23,
        "year": 2014,
        "season": "Fall",
        "studio": "Madhouse",
        "genres": ["Action", "Horror", "Sci-Fi", "Psychological"],
        "tags": ["Body Horror", "Symbiosis", "Evolution", "Gory"],
        "archetypes": ["Anti-hero", "Underdog"],
        "dna": {
            "psychological": 88.0,
            "action_intensity": 89.0,
            "narrative_complexity": 81.0,
            "emotional_depth": 85.0,
            "pacing": 90.0,
            "darkness": 86.0,
            "world_building": 72.0,
            "philosophical": 87.0
        },
        "streaming": ["Netflix", "Crunchyroll", "Hulu"],
        "why_watch": "A relentless body-horror thriller with deep biological philosophy and a stunning character transformation."
    },
    {
        "id": "made-in-abyss",
        "title": "Made in Abyss",
        "title_jp": "メイドインアビス",
        "synopsis": "An enormous, unexplored chasm known as the Abyss plunges deep into the earth, filled with mysterious relics and dangerous creatures. Orphan girl Riko and robot boy Reg descend into the depths, confronting horrific physical and psychological curses with no hope of return.",
        "image_url": "https://cdn.myanimelist.net/images/anime/6/86733.jpg",
        "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200&auto=format&fit=crop&q=80",
        "score": 8.65,
        "episodes": 25,
        "duration_min": 25,
        "year": 2017,
        "season": "Summer",
        "studio": "Kinema Citrus",
        "genres": ["Adventure", "Drama", "Fantasy", "Mystery", "Sci-Fi"],
        "tags": ["Chasm Exploration", "Body Horror", "Sensory Immersion", "Haunting Soundtrack"],
        "archetypes": ["Underdog", "Empathetic Leader"],
        "dna": {
            "psychological": 89.0,
            "action_intensity": 74.0,
            "narrative_complexity": 86.0,
            "emotional_depth": 96.0,
            "pacing": 64.0,
            "darkness": 95.0,
            "world_building": 99.0,
            "philosophical": 88.0
        },
        "streaming": ["HIDIVE", "Amazon Prime"],
        "why_watch": "Deceptively storybook art masking one of the most punishing, imaginative, and unforgettable dark fantasy odysseys."
    },
    {
        "id": "violet-evergarden",
        "title": "Violet Evergarden",
        "title_jp": "ヴァイオレット・エヴァーガーデン",
        "synopsis": "Raised as a lethal weapon during the Great War, former child soldier Violet Evergarden begins working as an 'Auto Memory Doll'—a ghostwriter who crafts letters expressing clients' unspoken feelings—in search of the meaning behind her Major's final words: 'I love you.'",
        "image_url": "https://cdn.myanimelist.net/images/anime/1795/95088.jpg",
        "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200&auto=format&fit=crop&q=80",
        "score": 8.68,
        "episodes": 13,
        "duration_min": 24,
        "year": 2018,
        "season": "Winter",
        "studio": "Kyoto Animation",
        "genres": ["Drama", "Fantasy", "Slice of Life"],
        "tags": ["Post-War", "PTSD", "Letters", "Tear-Jerker", "Kyoto Animation Art"],
        "archetypes": ["Empathetic Leader"],
        "dna": {
            "psychological": 75.0,
            "action_intensity": 30.0,
            "narrative_complexity": 70.0,
            "emotional_depth": 99.0,
            "pacing": 50.0,
            "darkness": 42.0,
            "world_building": 85.0,
            "philosophical": 86.0
        },
        "streaming": ["Netflix"],
        "why_watch": "The gold standard of emotional tear-jerkers with peak Kyoto Animation visual perfection."
    },
    {
        "id": "bocchi-the-rock",
        "title": "Bocchi the Rock!",
        "title_jp": "ぼっち・ざ・ろっく！",
        "synopsis": "Hitori 'Bocchi' Gotoh is an extremely introverted, socially anxious guitarist who spends hours practicing alone in her closet. When drummer Nijika invites her to join Kessoku Band, Bocchi takes frantic, hilarious steps to overcome her social phobia.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1448/127956.jpg",
        "banner_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=1200&auto=format&fit=crop&q=80",
        "score": 8.78,
        "episodes": 12,
        "duration_min": 23,
        "year": 2022,
        "season": "Fall",
        "studio": "CloverWorks",
        "genres": ["Comedy", "Music"],
        "tags": ["Social Anxiety", "Indie Rock", "Visual Creativity", "Relatable"],
        "archetypes": ["Underdog"],
        "dna": {
            "psychological": 68.0,
            "action_intensity": 25.0,
            "narrative_complexity": 52.0,
            "emotional_depth": 82.0,
            "pacing": 84.0,
            "darkness": 15.0,
            "world_building": 48.0,
            "philosophical": 55.0
        },
        "streaming": ["Crunchyroll"],
        "why_watch": "An inventive, hyper-relatable comedy celebrating musical passion with mind-boggling creative animation shifts."
    },
    {
        "id": "cowboy-bebop",
        "title": "Cowboy Bebop",
        "title_jp": "カウボーイビバップ",
        "synopsis": "In 2071, bounty hunters Spike Spiegel, Jet Black, Faye Valentine, and Edward drift across the solar system aboard the Bebop spaceship catching criminals, all while haunted by the inescapable ghosts of their pasts.",
        "image_url": "https://cdn.myanimelist.net/images/anime/4/19644.jpg",
        "banner_url": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1200&auto=format&fit=crop&q=80",
        "score": 8.75,
        "episodes": 26,
        "duration_min": 24,
        "year": 1998,
        "season": "Spring",
        "studio": "Sunrise",
        "genres": ["Action", "Sci-Fi", "Award Winning"],
        "tags": ["Space Western", "Jazz", "Noir", "Bounty Hunters"],
        "archetypes": ["Cynical Lone Wolf", "Anti-hero"],
        "dna": {
            "psychological": 82.0,
            "action_intensity": 84.0,
            "narrative_complexity": 80.0,
            "emotional_depth": 90.0,
            "pacing": 70.0,
            "darkness": 68.0,
            "world_building": 92.0,
            "philosophical": 92.0
        },
        "streaming": ["Netflix", "Crunchyroll", "Hulu"],
        "why_watch": "A legendary blend of jazz, melancholic noir, and effortless cool that remains an enduring masterpiece."
    },
    {
        "id": "mob-psycho-100",
        "title": "Mob Psycho 100",
        "title_jp": "モブサイコ100",
        "synopsis": "Shigeo 'Mob' Kageyama possesses god-tier psychic powers, but desires only to be normal and win over his crush. Under the tutelage of con-man mentor Reigen Arataka, Mob learns that psychic powers don't make him superior to anyone else.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1918/96303.jpg",
        "banner_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=1200&auto=format&fit=crop&q=80",
        "score": 8.48,
        "episodes": 37,
        "duration_min": 24,
        "year": 2016,
        "season": "Summer",
        "studio": "Bones",
        "genres": ["Action", "Comedy", "Supernatural"],
        "tags": ["Esper", "Self-Improvement", "Sakuga Animation", "Wholesome Mentorship"],
        "archetypes": ["Underdog", "Overpowered (OP)", "Empathetic Leader"],
        "dna": {
            "psychological": 85.0,
            "action_intensity": 96.0,
            "narrative_complexity": 75.0,
            "emotional_depth": 94.0,
            "pacing": 86.0,
            "darkness": 40.0,
            "world_building": 78.0,
            "philosophical": 89.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "why_watch": "Spectacular combat sakuga wrapped around one of the most mature, heartwarming coming-of-age philosophies."
    },
    {
        "id": "chainsaw-man",
        "title": "Chainsaw Man",
        "title_jp": "チェンソーマン",
        "synopsis": "Denji lives in poverty paying off his deceased father's yakuza debt by working as a Devil Hunter with Pochita, the Chainsaw Devil. After a lethal betrayal, Pochita fuses with Denji's heart, turning him into a terrifying devil-human hybrid recruited by Makima's Public Safety.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1806/126216.jpg",
        "banner_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1200&auto=format&fit=crop&q=80",
        "score": 8.48,
        "episodes": 12,
        "duration_min": 24,
        "year": 2022,
        "season": "Fall",
        "studio": "MAPPA",
        "genres": ["Action", "Supernatural"],
        "tags": ["Devils", "Gore", "Cinematic", "Chaotic", "Unpredictable"],
        "archetypes": ["Anti-hero", "Underdog"],
        "dna": {
            "psychological": 82.0,
            "action_intensity": 97.0,
            "narrative_complexity": 80.0,
            "emotional_depth": 83.0,
            "pacing": 94.0,
            "darkness": 91.0,
            "world_building": 85.0,
            "philosophical": 81.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "why_watch": "A cinematic, gleefully unhinged subversion of shonen tropes with visceral battles and dark emotional currents."
    },
    {
        "id": "pluto",
        "title": "Pluto",
        "title_jp": "プルートゥ",
        "synopsis": "Europol detective Gesicht, an advanced humanoid robot, investigates a string of murders targeting the world's seven most advanced robots and human advocates of robot rights. As the mystery deepens, he uncovers a weapon of mass hatred born from past war crimes.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1760/139043.jpg",
        "banner_url": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1200&auto=format&fit=crop&q=80",
        "score": 8.47,
        "episodes": 8,
        "duration_min": 60,
        "year": 2023,
        "season": "Fall",
        "studio": "Studio M2",
        "genres": ["Action", "Mystery", "Sci-Fi", "Suspense"],
        "tags": ["Naoki Urasawa", "Astro Boy Reimagining", "AI Morality", "Grief"],
        "archetypes": ["Cynical Lone Wolf", "Empathetic Leader"],
        "dna": {
            "psychological": 95.0,
            "action_intensity": 75.0,
            "narrative_complexity": 93.0,
            "emotional_depth": 95.0,
            "pacing": 68.0,
            "darkness": 85.0,
            "world_building": 92.0,
            "philosophical": 98.0
        },
        "streaming": ["Netflix"],
        "why_watch": "Naoki Urasawa's masterstroke: 8 hour-long episodes probing the boundary between artificial consciousness and soul."
    },
    {
        "id": "terror-in-resonance",
        "title": "Terror in Resonance (Zankyou no Terror)",
        "title_jp": "残響のテロル",
        "synopsis": "Two teenage genius prodigies, Nine and Twelve, carry out complex bomb attacks across Tokyo with zero casualties, leaving bizarre riddles online under the moniker 'Sphinx'. Ace detective Shibazaki races against time to uncover the dark facility behind their birth.",
        "image_url": "https://cdn.myanimelist.net/images/anime/7/64293.jpg",
        "banner_url": "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1200&auto=format&fit=crop&q=80",
        "score": 8.09,
        "episodes": 11,
        "duration_min": 22,
        "year": 2014,
        "season": "Summer",
        "studio": "MAPPA",
        "genres": ["Mystery", "Psychological", "Suspense"],
        "tags": ["Shinichiro Watanabe", "Yoko Kanno Music", "Riddles", "Tokyo Catastrophe"],
        "archetypes": ["Anti-hero", "Mastermind / Strategist"],
        "dna": {
            "psychological": 92.0,
            "action_intensity": 68.0,
            "narrative_complexity": 85.0,
            "emotional_depth": 87.0,
            "pacing": 89.0,
            "darkness": 82.0,
            "world_building": 70.0,
            "philosophical": 84.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "why_watch": "A tight 11-episode adrenaline puzzle accompanied by a haunting Yoko Kanno soundtrack."
    },
    {
        "id": "attack-on-titan",
        "title": "Attack on Titan (Shingeki no Kyojin)",
        "title_jp": "進撃の巨人",
        "synopsis": "Humanity lives enclosed within three concentric walls to protect themselves from man-eating humanoid giants called Titans. When the outer wall is shattered, Eren Yeager enlists in the Scout Regiment, embarking on a devastating multi-generational geopolitical war.",
        "image_url": "https://cdn.myanimelist.net/images/anime/10/47347.jpg",
        "banner_url": "https://images.unsplash.com/photo-1533240332313-0db49b459ad6?w=1200&auto=format&fit=crop&q=80",
        "score": 8.55,
        "episodes": 89,
        "duration_min": 24,
        "year": 2013,
        "season": "Spring",
        "studio": "WIT Studio / MAPPA",
        "genres": ["Action", "Suspense", "Drama"],
        "tags": ["Titans", "Foreshadowing", "War Politics", "Cycle of Violence"],
        "archetypes": ["Anti-hero", "Underdog"],
        "dna": {
            "psychological": 90.0,
            "action_intensity": 98.0,
            "narrative_complexity": 96.0,
            "emotional_depth": 92.0,
            "pacing": 88.0,
            "darkness": 94.0,
            "world_building": 97.0,
            "philosophical": 93.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "why_watch": "A modern juggernaut featuring some of the most intricate long-term plot foreshadowing in television history."
    },
    {
        "id": "code-geass",
        "title": "Code Geass: Lelouch of the Rebellion",
        "title_jp": "コードギアス 反逆のルルーシュ",
        "synopsis": "Exiled Britannian prince Lelouch vi Britannia obtains the Geass—the power of absolute obedience. Donning the mask of Zero, he commands the Black Knights in a grand chess match against his father's global empire.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1032/135088.jpg",
        "banner_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=1200&auto=format&fit=crop&q=80",
        "score": 8.70,
        "episodes": 50,
        "duration_min": 24,
        "year": 2006,
        "season": "Fall",
        "studio": "Sunrise",
        "genres": ["Action", "Drama", "Mecha", "Sci-Fi"],
        "tags": ["Tactical Chess", "Masked Identity", "Empire Rebellion", "Legendary Ending"],
        "archetypes": ["Anti-hero", "Mastermind / Strategist"],
        "dna": {
            "psychological": 96.0,
            "action_intensity": 88.0,
            "narrative_complexity": 93.0,
            "emotional_depth": 88.0,
            "pacing": 92.0,
            "darkness": 78.0,
            "world_building": 89.0,
            "philosophical": 86.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "why_watch": "The gold standard of mastermind anti-hero strategy culminating in one of anime's greatest finales."
    },
    {
        "id": "serial-experiments-lain",
        "title": "Serial Experiments Lain",
        "title_jp": "シリアルエクスペリメンツレイン",
        "synopsis": "Fourteen-year-old Lain Iwakura receives an email from a classmate who committed suicide, claiming to have abandoned physical existence to live in The Wired. As Lain delves into the network, the boundary between physical reality and virtual deity collapses.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1915/144605.jpg",
        "banner_url": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1200&auto=format&fit=crop&q=80",
        "score": 8.08,
        "episodes": 13,
        "duration_min": 24,
        "year": 1998,
        "season": "Summer",
        "studio": "Triangle Staff",
        "genres": ["Avant Garde", "Drama", "Mystery", "Psychological", "Sci-Fi"],
        "tags": ["The Wired", "Cyberpunk", "Philosophical", "Prescient Internet"],
        "archetypes": ["Cynical Lone Wolf"],
        "dna": {
            "psychological": 99.0,
            "action_intensity": 15.0,
            "narrative_complexity": 98.0,
            "emotional_depth": 78.0,
            "pacing": 28.0,
            "darkness": 88.0,
            "world_building": 85.0,
            "philosophical": 100.0
        },
        "streaming": ["Crunchyroll"],
        "why_watch": "An eerie, avant-garde 1998 masterpiece that terrifyingly predicted social media, omnipresent internet, and transhumanism."
    },
    {
        "id": "ping-pong-the-animation",
        "title": "Ping Pong the Animation",
        "title_jp": "ピンポン THE ANIMATION",
        "synopsis": "Smile, a quiet table tennis prodigy who plays without passion, and Peco, a swaggering childhood friend who lives to be the hero, navigate fierce national high school tournaments, confronting ego, sacrifice, and the true meaning of athletic pursuit.",
        "image_url": "https://cdn.myanimelist.net/images/anime/10/58041.jpg",
        "banner_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=1200&auto=format&fit=crop&q=80",
        "score": 8.62,
        "episodes": 11,
        "duration_min": 23,
        "year": 2014,
        "season": "Spring",
        "studio": "Tatsunoko Production",
        "genres": ["Drama", "Sports"],
        "tags": ["Masaaki Yuasa", "Expressive Art", "Coming of Age", "Self-Discovery"],
        "archetypes": ["Underdog", "Empathetic Leader"],
        "dna": {
            "psychological": 88.0,
            "action_intensity": 82.0,
            "narrative_complexity": 76.0,
            "emotional_depth": 94.0,
            "pacing": 90.0,
            "darkness": 38.0,
            "world_building": 60.0,
            "philosophical": 93.0
        },
        "streaming": ["Crunchyroll"],
        "why_watch": "Masaaki Yuasa's kinetic, uninhibited 11-episode character study that transcends the sports genre."
    },
    {
        "id": "mushishi",
        "title": "Mushishi",
        "title_jp": "蟲師",
        "synopsis": "Ginko is a traveler known as a Mushi Master, investigating primordial life forms called 'Mushi' that exist beyond human perception and alter human bodies and natural landscapes in mystical, melancholic ways.",
        "image_url": "https://cdn.myanimelist.net/images/anime/2/73862.jpg",
        "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200&auto=format&fit=crop&q=80",
        "score": 8.67,
        "episodes": 26,
        "duration_min": 24,
        "year": 2005,
        "season": "Fall",
        "studio": "Artland",
        "genres": ["Adventure", "Fantasy", "Mystery", "Slice of Life", "Supernatural"],
        "tags": ["Folklore", "Atmospheric", "Episodic", "Meditative"],
        "archetypes": ["Empathetic Leader", "Cynical Lone Wolf"],
        "dna": {
            "psychological": 80.0,
            "action_intensity": 18.0,
            "narrative_complexity": 74.0,
            "emotional_depth": 92.0,
            "pacing": 20.0,
            "darkness": 45.0,
            "world_building": 97.0,
            "philosophical": 98.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "why_watch": "The pinnacle of meditative, atmospheric storytelling; a deeply calming yet haunting journey into folklore."
    },
    {
        "id": "summer-time-rendering",
        "title": "Summer Time Rendering",
        "title_jp": "サマータイムレンダ",
        "synopsis": "Shinpei Ajiro returns to his isolated island hometown for his childhood friend Ushio's funeral. But a mysterious shadow illness, doppelgängers, and violent murders plunge him into a deadly, high-stakes time loop battle against ancient entities.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1101/121111.jpg",
        "banner_url": "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1200&auto=format&fit=crop&q=80",
        "score": 8.49,
        "episodes": 25,
        "duration_min": 23,
        "year": 2022,
        "season": "Spring",
        "studio": "OLM",
        "genres": ["Mystery", "Supernatural", "Suspense"],
        "tags": ["Time Loop", "Doppelganger", "Island Mystery", "High Stakes"],
        "archetypes": ["Mastermind / Strategist", "Empathetic Leader"],
        "dna": {
            "psychological": 90.0,
            "action_intensity": 85.0,
            "narrative_complexity": 93.0,
            "emotional_depth": 84.0,
            "pacing": 94.0,
            "darkness": 82.0,
            "world_building": 81.0,
            "philosophical": 78.0
        },
        "streaming": ["Hulu", "Disney+"],
        "why_watch": "An electrifying time-loop mystery that maintains white-knuckle pacing with airtight tactical countermeasures."
    },
    {
        "id": "sonny-boy",
        "title": "Sonny Boy",
        "title_jp": "サニーボーイ",
        "synopsis": "During summer vacation, 36 high school students and their school building drift into an empty alternate dimension. As superpowers manifest among them, internal factions form while they wander through abstract worlds seeking a way home.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1997/115814.jpg",
        "banner_url": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1200&auto=format&fit=crop&q=80",
        "score": 7.78,
        "episodes": 12,
        "duration_min": 24,
        "year": 2021,
        "season": "Summer",
        "studio": "Madhouse",
        "genres": ["Adventure", "Mystery", "Sci-Fi"],
        "tags": ["Shingo Natsume", "Surrealism", "Youth Philosophy", "Underrated Gem"],
        "archetypes": ["Cynical Lone Wolf"],
        "dna": {
            "psychological": 91.0,
            "action_intensity": 38.0,
            "narrative_complexity": 96.0,
            "emotional_depth": 85.0,
            "pacing": 45.0,
            "darkness": 60.0,
            "world_building": 94.0,
            "philosophical": 99.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "why_watch": "An underrated avant-garde gem that explores teenage alienation through dazzling surrealist allegories."
    },
    {
        "id": "link-click",
        "title": "Link Click (Shiguang Dailiren)",
        "title_jp": "时光代理人",
        "synopsis": "Cheng Xiaoshi and Lu Guang operate the Time Photo Studio. By jumping into photographs provided by clients, they can experience past moments and change outcomes while trying desperately to adhere to the rule: 'No matter the past, no matter the future.'",
        "image_url": "https://cdn.myanimelist.net/images/anime/1135/114867.jpg",
        "banner_url": "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1200&auto=format&fit=crop&q=80",
        "score": 8.71,
        "episodes": 23,
        "duration_min": 23,
        "year": 2021,
        "season": "Spring",
        "studio": "Studio LAN",
        "genres": ["Drama", "Mystery", "Supernatural"],
        "tags": ["Photo Leap", "Serial Killer", "Cliffhangers", "Dynamic Duo"],
        "archetypes": ["Mastermind / Strategist", "Empathetic Leader"],
        "dna": {
            "psychological": 93.0,
            "action_intensity": 70.0,
            "narrative_complexity": 92.0,
            "emotional_depth": 95.0,
            "pacing": 95.0,
            "darkness": 79.0,
            "world_building": 78.0,
            "philosophical": 82.0
        },
        "streaming": ["Crunchyroll"],
        "why_watch": "Known for the most jaw-dropping cliffhangers in modern animation; a masterclass in emotional mystery."
    },
    {
        "id": "heavenly-delusion",
        "title": "Heavenly Delusion (Tengoku Daimakyou)",
        "title_jp": "天国大魔境",
        "synopsis": "Within a walled paradise, children are raised by robots without knowledge of the outside world. Meanwhile, in a post-apocalyptic outside ruin, Maru and his bodyguard Kiruko travel across monster-infested Japan searching for 'Heaven.'",
        "image_url": "https://cdn.myanimelist.net/images/anime/1154/133033.jpg",
        "banner_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=1200&auto=format&fit=crop&q=80",
        "score": 8.19,
        "episodes": 13,
        "duration_min": 23,
        "year": 2023,
        "season": "Spring",
        "studio": "Production I.G",
        "genres": ["Adventure", "Mystery", "Sci-Fi"],
        "tags": ["Post-Apocalypse", "Twin Timelines", "Eldritch Horrors", "Subtle Clues"],
        "archetypes": ["Underdog", "Empathetic Leader"],
        "dna": {
            "psychological": 89.0,
            "action_intensity": 83.0,
            "narrative_complexity": 95.0,
            "emotional_depth": 83.0,
            "pacing": 78.0,
            "darkness": 88.0,
            "world_building": 96.0,
            "philosophical": 86.0
        },
        "streaming": ["Hulu", "Disney+"],
        "why_watch": "A masterfully structured twin-timeline mystery where every visual background holds answers to the apocalypse."
    },
    {
        "id": "dororo",
        "title": "Dororo",
        "title_jp": "どろろ",
        "synopsis": "A samurai lord makes a pact with 12 demons for dominion, sacrificing his newborn son's organs and limbs. Cast adrift, the boy survives with prosthetic weaponry (Hyakkimaru) and sets out to slay the demons to reclaim his stolen body.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1879/100467.jpg",
        "banner_url": "https://images.unsplash.com/photo-1533240332313-0db49b459ad6?w=1200&auto=format&fit=crop&q=80",
        "score": 8.24,
        "episodes": 24,
        "duration_min": 24,
        "year": 2019,
        "season": "Winter",
        "studio": "MAPPA / Tezuka Productions",
        "genres": ["Action", "Adventure", "Supernatural"],
        "tags": ["Sengoku Japan", "Demons", "Prosthetic Blades", "Reclaiming Humanity"],
        "archetypes": ["Anti-hero", "Cynical Lone Wolf"],
        "dna": {
            "psychological": 83.0,
            "action_intensity": 90.0,
            "narrative_complexity": 80.0,
            "emotional_depth": 88.0,
            "pacing": 76.0,
            "darkness": 86.0,
            "world_building": 87.0,
            "philosophical": 91.0
        },
        "streaming": ["Amazon Prime", "Hulu"],
        "why_watch": "A visceral dark samurai tale raising questions about whether one boy's life can be sacrificed for peace."
    },
    {
        "id": "fullmetal-alchemist-brotherhood",
        "title": "Fullmetal Alchemist: Brotherhood",
        "title_jp": "鋼の錬金術師 FULLMETAL ALCHEMIST",
        "synopsis": "Brothers Edward and Alphonse Elric pay a disastrous price when attempting human transmutation: Ed loses his arm and leg, and Al loses his entire physical body. Seeking the Philosopher's Stone to restore themselves, they uncover a nation-wide conspiracy.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1223/96541.jpg",
        "banner_url": "https://images.unsplash.com/photo-1533240332313-0db49b459ad6?w=1200&auto=format&fit=crop&q=80",
        "score": 9.10,
        "episodes": 64,
        "duration_min": 24,
        "year": 2009,
        "season": "Spring",
        "studio": "Bones",
        "genres": ["Action", "Adventure", "Drama", "Fantasy"],
        "tags": ["Alchemy", "Homunculus", "Conspiracy", "Top Tier World Building"],
        "archetypes": ["Empathetic Leader", "Underdog"],
        "dna": {
            "psychological": 85.0,
            "action_intensity": 90.0,
            "narrative_complexity": 92.0,
            "emotional_depth": 94.0,
            "pacing": 88.0,
            "darkness": 68.0,
            "world_building": 97.0,
            "philosophical": 89.0
        },
        "streaming": ["Crunchyroll", "Hulu"],
        "why_watch": "Widely acclaimed as the most completely satisfying, airtight shonen story ever animated."
    },
    {
        "id": "jujutsu-kaisen",
        "title": "Jujutsu Kaisen",
        "title_jp": "呪術廻戦",
        "synopsis": "High school athlete Yuji Itadori swallows a cursed finger belonging to Ryomen Sukuna, the King of Curses, to save his friends. Enrolled at Tokyo Jujutsu High, he fights grotesque Curses while sharing his soul with a demon.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1171/109222.jpg",
        "banner_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1200&auto=format&fit=crop&q=80",
        "score": 8.61,
        "episodes": 47,
        "duration_min": 23,
        "year": 2020,
        "season": "Fall",
        "studio": "MAPPA",
        "genres": ["Action", "Fantasy", "Supernatural"],
        "tags": ["Curse Energy", "Domain Expansion", "Insane Sakuga", "Dark Fantasy"],
        "archetypes": ["Underdog", "Empathetic Leader"],
        "dna": {
            "psychological": 74.0,
            "action_intensity": 99.0,
            "narrative_complexity": 78.0,
            "emotional_depth": 80.0,
            "pacing": 96.0,
            "darkness": 84.0,
            "world_building": 86.0,
            "philosophical": 72.0
        },
        "streaming": ["Crunchyroll"],
        "why_watch": "Industry-defining martial arts choreography, explosive domain expansion clashes, and breakneck pacing."
    },
    {
        "id": "a-silent-voice",
        "title": "A Silent Voice (Koe no Katachi)",
        "title_jp": "聲の形",
        "synopsis": "In elementary school, Shoya Ishida ruthlessly bullied deaf transfer student Shoko Nishimiya until she transferred away, causing him to become a social outcast. Years later in high school, haunted by guilt, Shoya embarks on a path to atone and make amends.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1122/96442.jpg",
        "banner_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200&auto=format&fit=crop&q=80",
        "score": 8.94,
        "episodes": 1,
        "duration_min": 130,
        "year": 2016,
        "season": "Fall",
        "studio": "Kyoto Animation",
        "genres": ["Award Winning", "Drama"],
        "tags": ["Deaf", "Redemption", "Bullying", "Deep Empathy", "Masterpiece Film"],
        "archetypes": ["Empathetic Leader", "Underdog"],
        "dna": {
            "psychological": 87.0,
            "action_intensity": 15.0,
            "narrative_complexity": 74.0,
            "emotional_depth": 100.0,
            "pacing": 60.0,
            "darkness": 62.0,
            "world_building": 50.0,
            "philosophical": 92.0
        },
        "streaming": ["Netflix", "Amazon Prime"],
        "why_watch": "A monumental feature film that offers an honest, devastating, and uplifting examination of guilt and self-forgiveness."
    },
    {
        "id": "perfect-blue",
        "title": "Perfect Blue",
        "title_jp": "パーフェクトブルー",
        "synopsis": "Mima Kirigoe leaves her pop idol group to pursue a serious acting career. But an obsessive stalker, traumatic adult drama roles, and a phantom doppelgänger tear down her sanity until she can no longer distinguish delusion from reality.",
        "image_url": "https://cdn.myanimelist.net/images/anime/11/73611.jpg",
        "banner_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=1200&auto=format&fit=crop&q=80",
        "score": 8.54,
        "episodes": 1,
        "duration_min": 81,
        "year": 1997,
        "season": "Summer",
        "studio": "Madhouse",
        "genres": ["Avant Garde", "Drama", "Horror", "Psychological"],
        "tags": ["Satoshi Kon", "Idol Stalker", "Psychosis", "Cinema Legend"],
        "archetypes": ["Underdog"],
        "dna": {
            "psychological": 100.0,
            "action_intensity": 52.0,
            "narrative_complexity": 97.0,
            "emotional_depth": 88.0,
            "pacing": 88.0,
            "darkness": 95.0,
            "world_building": 60.0,
            "philosophical": 96.0
        },
        "streaming": ["Amazon Prime", "Tubi"],
        "why_watch": "Satoshi Kon's psychological horror triumph that inspired Darren Aronofsky's Black Swan."
    }
]


class AnimeDatabase:
    """
    In-memory curated anime repository with fast indexing,
    filtering, and DNA lookup.
    """
    _items: List[AnimeItem] = []
    _by_id: Dict[str, AnimeItem] = {}

    @classmethod
    def initialize(cls):
        if cls._items:
            return
        for raw in RAW_ANIME_DATA:
            dna = AnimeDNAModel(**raw["dna"])
            item = AnimeItem(
                id=raw["id"],
                title=raw["title"],
                title_jp=raw.get("title_jp", ""),
                synopsis=raw["synopsis"],
                image_url=raw["image_url"],
                banner_url=raw.get("banner_url", ""),
                score=raw["score"],
                episodes=raw["episodes"],
                duration_min=raw.get("duration_min", 24),
                year=raw["year"],
                season=raw.get("season", "All-Time"),
                studio=raw["studio"],
                genres=raw["genres"],
                tags=raw.get("tags", []),
                archetypes=raw.get("archetypes", []),
                character_dynamics=raw.get("character_dynamics", []),
                dna=dna,
                streaming=raw.get("streaming", ["Crunchyroll"]),
                dub_tier=raw.get("dub_tier", "A-Tier Great"),
                dub_cast=raw.get("dub_cast", []),
                sub_cast=raw.get("sub_cast", []),
                iconic_quote=raw.get("iconic_quote"),
                soundtrack_genre=raw.get("soundtrack_genre", "Cinematic"),
                why_watch=raw["why_watch"]
            )
            cls._items.append(item)
            cls._by_id[item.id] = item

    @classmethod
    def get_all(cls) -> List[AnimeItem]:
        cls.initialize()
        return cls._items

    @classmethod
    def get_by_id(cls, anime_id: str) -> Optional[AnimeItem]:
        cls.initialize()
        return cls._by_id.get(anime_id)

    @classmethod
    def add_or_update(cls, item: AnimeItem):
        cls.initialize()
        if item.id in cls._by_id:
            cls._items = [i if i.id != item.id else item for i in cls._items]
        else:
            cls._items.append(item)
        cls._by_id[item.id] = item

    @classmethod
    def filter_items(
        cls,
        max_episodes: Optional[int] = None,
        min_score: Optional[float] = None,
        genres: Optional[List[str]] = None,
        archetypes: Optional[List[str]] = None,
        dub_tier: Optional[str] = None,
        exclude_ids: Optional[List[str]] = None
    ) -> List[AnimeItem]:
        cls.initialize()
        results = cls._items

        if exclude_ids:
            exclude_set = set(exclude_ids)
            results = [a for a in results if a.id not in exclude_set]

        if min_score is not None:
            results = [a for a in results if a.score >= min_score]

        if max_episodes is not None:
            # allow some leeway for scoring, or hard filter if requested
            results = [a for a in results if a.episodes <= max_episodes]

        if dub_tier:
            results = [a for a in results if a.dub_tier == dub_tier]

        if genres:
            genre_set = {g.lower() for g in genres}
            results = [
                a for a in results
                if any(g.lower() in genre_set for g in a.genres)
            ]

        if archetypes:
            arch_set = {arc.lower() for arc in archetypes}
            results = [
                a for a in results
                if any(arc.lower() in arch_set for arc in a.archetypes)
            ]

        return results
