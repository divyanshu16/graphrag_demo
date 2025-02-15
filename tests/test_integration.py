import os
import unittest
from loguru import logger
from src.kg_gen import KnowledgeGraphGen
from src.pdf_utils import process_pdfs


class KnowledgeGraphIntegrationTest(unittest.TestCase):
    additional_pdf_dir = None
    test_pdf_dir = None

    @classmethod
    def setUpClass(cls):
        """Set up the knowledge graph before running tests."""
        cls.test_pdf_dir = os.path.join(os.path.dirname(__file__), "test_pdfs")
        cls.additional_pdf_dir = os.path.join(
            os.path.dirname(__file__), "additional_test_pdfs"
        )

        logger.info("Creating KG from test pdfs")
        cls.kg = KnowledgeGraphGen(
            "test_kg_",
            sources=process_pdfs(cls.test_pdf_dir),
            model_name=os.getenv("MODEL_PROVIDER", "gemini/gemini-2.0-flash-exp"),
            db_host=os.getenv("FALKORDB_URL", "127.0.0.1"),
            db_port=int(os.getenv("FALKORDB_URL_PORT", 6379)),
        )

    def check_knowledge_graph_creation(self):
        """Test that the knowledge graph can process sources and answer queries."""
        eval_questions = [
            "Who is the director of The Matrix?",
            "When was the movie The Matrix released?",
        ]
        logger.info("Asking the test questions")
        responses = self.kg.ask_questions(eval_questions)
        logger.info(f"responses:\n{responses}")

        self.assertEqual(len(responses), len(eval_questions))
        for response in responses:
            self.assertIsInstance(response['response'], str)
            # self.assertNotEqual(response, "")

    def check_add_additional_sources(self):
        """Test adding additional PDFs and querying newly added data."""
        additional_texts = process_pdfs(self.additional_pdf_dir)

        self.kg.add_sources(additional_texts)

        eval_questions = [
            "Who directed the movie The Imitation Game?",
            "What is the release year of The Imitation Game?",
        ]
        responses = self.kg.ask_questions(eval_questions)
        logger.info(f"responses received: {responses}")

        self.assertEqual(len(responses), len(eval_questions))
        for response in responses:
            self.assertIsInstance(response, str)

    def test_integration(self):
        logger.info("Starting KG creation and adding initial pdfs")
        self.check_knowledge_graph_creation()
        logger.info("Adding additional pdfs and checking its working")
        self.check_add_additional_sources()


if __name__ == "__main__":
    unittest.main()
