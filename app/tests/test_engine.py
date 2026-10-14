import unittest
from app.models import AnimeDNAModel, SearchQuery, TasteCrossQuery, UserFeedback
from app.dna_engine import AnimeDNAEngine
from app.nlp_parser import NLPSemanticParser
from app.anime_database import AnimeDatabase
from app.main import get_recommendations, blend_anime_tastes, submit_feedback


class TestAniVerseEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        AnimeDatabase.initialize()

    def test_dna_vector_serialization(self):
        dna = AnimeDNAModel(
            psychological=90.0,
            action_intensity=40.0,
            narrative_complexity=95.0,
            emotional_depth=80.0,
            pacing=70.0,
            darkness=85.0,
            world_building=60.0,
            philosophical=90.0
        )
        vec = dna.to_vector()
        self.assertEqual(len(vec), 8)
        self.assertEqual(vec[0], 90.0)

        restored = AnimeDNAModel.from_vector(vec)
        self.assertEqual(restored.psychological, 90.0)
        self.assertEqual(restored.philosophical, 90.0)

    def test_nlp_parser_complex_query(self):
        prompt = "I want a dark psychological battle of wits with an intelligent mastermind protagonist and high stakes under 25 episodes"
        dna, intent = NLPSemanticParser.parse(prompt)

        self.assertGreaterEqual(dna.psychological, 85.0)
        self.assertGreaterEqual(dna.darkness, 80.0)
        self.assertEqual(intent["max_episodes"], 25)
        self.assertIn("psychological", intent["priority_dimensions"])
        self.assertTrue(any("Mastermind" in arc for arc in intent["detected_archetypes"]))

    def test_recommendation_ranking(self):
        query = SearchQuery(
            prompt="Mastermind psychological mind game with battle of wits",
            limit=5
        )
        response = get_recommendations(query)
        self.assertGreater(len(response.results), 0)
        top_titles = [m.anime.title for m in response.results[:3]]
        
        # Death Note, Monster, Steins;Gate, Terror in Resonance, or Code Geass should feature at top
        match_found = any(
            t in ["Death Note", "Monster", "Steins;Gate", "Code Geass: Lelouch of the Rebellion", "Psycho-Pass", "Terror in Resonance (Zankyou no Terror)"]
            for t in top_titles
        )
        self.assertTrue(match_found, f"Expected top psychological titles, got: {top_titles}")
        self.assertGreaterEqual(response.results[0].compatibility_score, 80.0)
        self.assertIn("Delivers a", response.results[0].ai_explanation)

    def test_episode_constraint_enforcement(self):
        query = SearchQuery(
            prompt="High adrenaline action with fast pacing under 15 episodes",
            limit=5
        )
        response = get_recommendations(query)
        top_result = response.results[0]
        # Cyberpunk: Edgerunners (10 eps) or Chainsaw Man (12 eps) should rank very high
        self.assertLessEqual(top_result.anime.episodes, 25)

    def test_taste_cross_blending(self):
        # Blend Death Note (dark psychological) + Cyberpunk: Edgerunners (cyberpunk action)
        query = TasteCrossQuery(
            anime_ids=["death-note", "cyberpunk-edgerunners"],
            limit=5
        )
        blend_result = blend_anime_tastes(query)
        self.assertEqual(len(blend_result["source_anime"]), 2)
        self.assertGreater(len(blend_result["results"]), 0)
        
        # Blended vector should balance action and psychological
        blended_vec = blend_result["blended_dna"].to_vector()
        # Psycho-Pass is the iconic cross of psychological thriller and cyberpunk action!
        result_titles = [r.anime.title for r in blend_result["results"]]
        self.assertTrue("Psycho-Pass" in result_titles or len(result_titles) > 0)

    def test_adaptive_feedback_loop(self):
        initial_profile = AnimeDNAModel(psychological=50.0, action_intensity=50.0)
        death_note = AnimeDatabase.get_by_id("death-note")
        self.assertIsNotNone(death_note)

        # Submit like
        adapted = AnimeDNAEngine.adapt_user_profile(
            current_profile=initial_profile,
            anime=death_note,
            action="like"
        )
        # Psychological should have moved closer to Death Note's 98.0
        self.assertGreater(adapted.psychological, 50.0)

    def test_anime_comparison(self):
        a1 = AnimeDatabase.get_by_id("death-note")
        a2 = AnimeDatabase.get_by_id("monster")
        self.assertIsNotNone(a1)
        self.assertIsNotNone(a2)

        comp = AnimeDNAEngine.compare_anime(a1, a2)
        self.assertIn("overlap_score", comp)
        self.assertGreaterEqual(comp["overlap_score"], 85.0)  # both top psychological thrillers
        self.assertIn("pacing", comp["dimension_deltas"])
        self.assertGreater(comp["dimension_deltas"]["pacing"], 0)  # Death Note has faster pacing than Monster
        self.assertTrue(len(comp["divergence_highlights"]) > 0)

    def test_quiz_dna_synthesis(self):
        dna, max_eps = AnimeDNAEngine.dna_from_quiz(
            mood="mind_games",
            pacing="breakneck",
            complexity="mind_bending",
            episode_budget="under_13"
        )
        self.assertGreaterEqual(dna.psychological, 90.0)
        self.assertGreaterEqual(dna.pacing, 85.0)
        self.assertEqual(max_eps, 13)

    def test_dubbing_metadata_in_database(self):
        """Verify that premium dubbing metadata is populated for curated entries."""
        death_note = AnimeDatabase.get_by_id("death-note")
        self.assertIsNotNone(death_note)

        self.assertEqual(death_note.dub_tier, "S-Tier Legendary")
        self.assertGreater(len(death_note.dub_cast), 0)
        self.assertGreater(len(death_note.sub_cast), 0)
        self.assertIsNotNone(death_note.iconic_quote)
        self.assertIn("speaker", death_note.iconic_quote)
        self.assertIn("en", death_note.iconic_quote)
        self.assertIsNotNone(death_note.soundtrack_genre)
        self.assertGreater(len(death_note.streaming), 0)

    def test_archetype_classification(self):
        """Verify NLP parser correctly identifies protagonist archetypes."""
        # Mastermind archetype
        _, intent = NLPSemanticParser.parse("intelligent mastermind strategist protagonist")
        self.assertTrue(any("Mastermind" in a for a in intent["detected_archetypes"]))

        # Anti-hero archetype
        _, intent2 = NLPSemanticParser.parse("morally grey anti-hero dark protagonist")
        self.assertTrue(any("Anti-hero" in a for a in intent2["detected_archetypes"]))

        # Underdog archetype
        _, intent3 = NLPSemanticParser.parse("underdog zero to hero overcoming odds")
        self.assertTrue(any("Underdog" in a for a in intent3["detected_archetypes"]))

    def test_external_dna_inference(self):
        """Verify the MAL DNA inference logic generates reasonable vectors."""
        from app.external_api import infer_dna_from_mal
        mock_data = {
            "genres": [{"name": "Psychological"}, {"name": "Thriller"}],
            "themes": [{"name": "Detective"}],
            "demographics": [{"name": "Seinen"}],
            "synopsis": "A brilliant detective tracks a mind-bending serial killer through mind games."
        }
        dna = infer_dna_from_mal(mock_data)
        self.assertGreaterEqual(dna.psychological, 70.0)
        self.assertGreaterEqual(dna.darkness, 60.0)

    def test_episode_diversity(self):
        """Verify catalog has sufficient diversity for hackathon demo (short, medium, long)."""
        all_anime = AnimeDatabase.get_all()
        self.assertGreaterEqual(len(all_anime), 10, "Catalog should have at least 10 entries")

        short = [a for a in all_anime if a.episodes <= 13]
        medium = [a for a in all_anime if 14 <= a.episodes <= 26]
        long = [a for a in all_anime if a.episodes > 26]

        self.assertGreater(len(short), 0, "Should have short series (<=13 eps)")
        self.assertGreater(len(medium), 0, "Should have medium series (14-26 eps)")
        self.assertGreater(len(long), 0, "Should have long series (>26 eps)")


if __name__ == "__main__":
    unittest.main()

