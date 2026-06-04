# Tabletop Sherpa

A RAG-powered rules assistant for tabletop wargames. Ask rules questions in plain English, resolve disputes at the table, or get guided through a game as a new player.

Currently supports Warhammer 40,000 10th Edition, with 11th Edition and additional game systems planned.

> **Powered by [Wahapedia](https://wahapedia.ru)** — structured game data is sourced from Wahapedia's community export. This project would not be possible without their work. Hats off to you guys

---

## Features

- **Rules Assistant** — precise answers grounded in official rules with no hallucinated content, 
    beginner friendly explanations without assuming prior knowledge *(in development)*
- **Hybrid search** — combines semantic vector search with exact name matching for accurate retrieval
- **Hallucination reduction** — keyword-based collection routing constrains the model to only relevant data
- Covers unit datasheets, stratagems, faction abilities, detachments, and core rules

---

## Tech Stack

- **Python** — backend and data pipeline
- **FastAPI** — REST API layer
- **ChromaDB** — local vector database
- **Ollama** — local LLM inference
- **Qwen2.5 / Mistral** — generation models (with transition to cloud-based models still being considered)
- **nomic-embed-text** — embedding model
- **pandas** — data ingestion and transformation
- **React** — frontend *(in development)*

---

## Data

Game data is sourced individually from community exports and official publications. Structured unit, stratagem, ability, and detachment data is provided by [Wahapedia](https://wahapedia.ru). Core rules are sourced from official Games Workshop publications.

This project is a fan-made tool and is not affiliated with or endorsed by Games Workshop or Wahapedia. All Warhammer 40,000 content and intellectual property belongs to Games Workshop Ltd.

---

## Project Status

Active development. Current state:

- [x] Data ingestion pipeline (units, stratagems, abilities, detachments)
- [x] Hybrid search with exact name matching
- [x] Keyword-based collection routing
- [x] Local LLM integration via Ollama
- [ ] FastAPI backend
- [ ] React frontend
- [ ] Dice probability calculator
- [ ] Warhammer 40,000 11th Edition support
- [ ] Additional game systems

---

## Getting Started

### Prerequisites

- Python 3.13+
- [Ollama](https://ollama.com) installed and running
- Required models pulled:

```
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

### Installation

```bash
git clone https://github.com/IezziS/TabletopSherpa
cd TabletopSherpa
uv sync
```

### Data Setup

Game data must be sourced independently due to licensing restrictions. Instructions to come in the future

Once data files are in place:

```bash
uv run -m backend.ingestion.ingest_all
```

### Running the App

```bash
uv run uvicorn backend.api:app --reload
```

---

## Disclaimer

Tabletop Sherpa is a fan-made community tool. It is not affiliated with, endorsed by, or connected to Games Workshop or Wahapedia. All game content, rules, and intellectual property referenced in this project belong to their respective owners.
