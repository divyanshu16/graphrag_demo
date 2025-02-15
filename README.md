# Knowledge Graph RAG

## Problem Statement:
1. Knowledge Graph Generator:
Utilize the GraphRAG-SDK as the framework for generating the Knowledge
Graph.
Integrate the framework with the Unstructured-IO library to support PDF files.
Generate and store the Knowledge Graph on FalkorDB.
Ensure the process is efficient and scalable.
2. Demonstrate Functionality:
First, ingest 5 PDF files and generate a Knowledge Graph from them.
Then, ingest an additional 5 PDF files (totaling 10 files, including the initial 5) and
evolve the Knowledge Graph, updating the database based on the new data.
3. Containerization:
Containerize the entire solution that automatically builds containers.

## Folder Structure
```commandline

tree -I "venv|*.pdf|*pycache*|*.json"
.
├── Dockerfile
├── README.md
├── data
│   ├── additional_pdfs
│   └── initial_pdfs
├── docker-compose.yml
├── requirements.txt
├── src
│   ├── kg_gen.py
│   ├── main.py
│   └── pdf_utils.py
└── tests
    └── test_integration.py

6 directories, 8 files

```

This project processes PDF documents, extracts text, and generates a Knowledge Graph (KG)
that enables users to query information efficiently. 
It leverages machine learning models (e.g., gemini/gemini-2.0-flash-exp) 
and a graph database (FalkorDB) to structure and retrieve information.

For this assignment, initial pdfs to create a knowledge graph has been kept in data/initial_pdfs 
and then additional pdfs in data/additional_pdfs

## Flow of the program:
- run the docker compose command
  - `GEMINI_API_KEY=<GEMINI_API_KEY>  docker compose up --build`
- this will spawn 2 containers 
  - one is of falkordb to store the knowledge graph
  - second one is the application layer
- go inside application layer container
  - run `docker ps` to check 2 containers are running
  - pick the knowledge graph generator container id and then run `docker exec -it <CONTAINER_ID> bash`
  - once inside, run `python src/main.py`
- You will start seeing the logs of
  - finding text from pdf
  - creation of ontology from those texts
  - building knowledge graph
  - processing of texts
  - responses of the questions
- There are few questions mentioned in main.py : `eval_questions`
  - first 2 questions' answers are in the initial set of pdfs
  - last 2 questions' answers are in additional set of pdfs
  - this will give us a sense if adding pdfs later is working or not.
  - For production use case, we have to expand this eval questions.


Notes:
- GraphRag library also provides ability to handle pdf. 
  - Had tested it out. It was working fine.
  - Code in the repo though uses unstructured as it was mentioned in the task requirements.
  - Effectiveness Comparison between these 2 methods can be done in the future. 
- 