# PhenomFlow - Phenomenological Analysis Assistant

This project is a ChatGPT-powered assistant for phenomenological analysis, designed with a high-end aesthetic interface.

## Structure

- **backend/**: FastAPI application handling the analysis logic and database.
- **shaders-landing-page/**: Next.js frontend with WebGL shaders.
- **data/**: Simulated interview data.
- **docker-compose.yml**: Orchestration for running the full stack.

## Setup

1.  Ensure you have Docker and Docker Compose installed.
2.  Ensure `.env` exists in the root with `OPENAI_API_KEY`.
3.  Run the application:
    ```bash
    docker-compose up --build
    ```
4.  Open [http://localhost:3000](http://localhost:3000) to view the application.
5.  The API is available at [http://localhost:8000](http://localhost:8000).

## Features

- **Phenomenological Analysis**: Uses GPT-4o to analyze interview transcripts based on the methodology from "Bridging consciousness and AI".
- **Interactive UI**: Beautiful, shader-powered landing page with a dedicated analysis section.
- **Database**: Stores all analyses in a SQLite database.
