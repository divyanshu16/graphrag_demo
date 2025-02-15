from loguru import logger
import traceback
import json
import time
from dotenv import load_dotenv
from graphrag_sdk import KnowledgeGraph, KnowledgeGraphModelConfig
from graphrag_sdk.ontology import Ontology
from graphrag_sdk.models.litellm import LiteModel
from graphrag_sdk.source import Source, Source_FromRawText
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()


def get_timestamp():
    return time.strftime("%Y%m%d-%H%M%S")


class KnowledgeGraphGen:
    def __init__(self, kg_name, sources, model_name, db_host, db_port):
        self.sources = [Source_FromRawText(_) for _ in sources]
        self.model_name = model_name
        self.model = LiteModel(model_name=self.model_name)

        logger.info("Creating ontology...")
        self.ontology: Ontology = Ontology.from_sources(
            sources=self.sources,
            model=self.model,
        )

        ontology_file = f"ontology_{get_timestamp()}.json"
        with open(ontology_file, "w", encoding="utf-8") as file:
            json.dump(self.ontology.to_json(), file, indent=2)
        logger.info(f"Saved ontology to {ontology_file}")

        logger.info("Initializing Knowledge Graph...")
        self.kg = KnowledgeGraph(
            name=kg_name,
            model_config=KnowledgeGraphModelConfig.with_model(self.model),
            ontology=self.ontology,
            host=db_host,
            port=db_port,
        )

        self.add_sources(self.sources)

    @retry(
        stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=2, max=10)
    )
    def add_sources(self, sources_):
        logger.info("Adding sources to Knowledge Graph...")
        sources_ = [Source_FromRawText(_) if type(_) is str else _ for _ in sources_]
        self.kg.process_sources(sources_)
        logger.info("Sources added successfully!")

    def ask_questions(self, questions):
        if isinstance(questions, str):
            questions = [questions]

        assert all(isinstance(q, str) for q in questions), "Questions must be strings!"

        chat_session = self.kg.chat_session()
        answers = []

        for each_q in questions:
            logger.info(f"Asking: {each_q}")
            try:
                response = chat_session.send_message(each_q)
            except Exception as e:
                logger.error(
                    f"Error in query '{each_q}': {str(e)}\n{traceback.format_exc()}"
                )
                response = "Error: Unable to answer"
            answers.append(response)

        return answers
