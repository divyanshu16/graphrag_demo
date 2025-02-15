import os
import json
from loguru import logger
from src.pdf_utils import process_pdfs
from src.kg_gen import KnowledgeGraphGen

eval_questions = [
    "Who is the director of the movie The Matrix?",
    "How is this director connected to Keanu Reeves?",
    "Who directed the movie The Imitation Game?",
    "Who acted in the movie The Revenant (2015)?",
]

if __name__ == "__main__":
    logger.info("Initializing Knowledge Graph Generation...")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    initial_pdf_dir = os.path.join(parent_dir, "data", "initial_pdfs")
    additional_pdf_dir = os.path.join(parent_dir, "data", "additional_pdfs")

    initial_texts = process_pdfs(initial_pdf_dir)

    kg_obj = KnowledgeGraphGen(
        "kg_movies",
        sources=initial_texts,
        model_name=os.getenv("MODEL_PROVIDER", "gemini/gemini-2.0-flash-exp"),
        db_host=os.getenv("FALKORDB_URL", "127.0.0.1"),
        db_port=int(os.getenv("FALKORDB_URL_PORT", 6379)),
    )

    eval_responses_initial = kg_obj.ask_questions(eval_questions)
    with open("eval_responses_initial.json", "w") as f:
        json.dump(eval_responses_initial, f, indent=2)
    logger.info("Saved initial evaluation responses.")

    additional_texts = process_pdfs(additional_pdf_dir)
    kg_obj.add_sources(additional_texts)

    eval_responses_additional = kg_obj.ask_questions(eval_questions)
    with open("eval_responses_additional.json", "w") as f:
        json.dump(eval_responses_additional, f, indent=2)
    logger.info("Saved evaluation responses after adding additional sources.")

    input("Press Enter to exit...")
