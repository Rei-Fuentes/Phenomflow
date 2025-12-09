# PhenomFlow Backend

Flask API para análisis fenomenológico con Claude Sonnet 4.

## Estructura

```
backend/
├── service.py           # API Flask principal
├── main.py              # FastAPI (legacy, no usado)
├── database.py          # Modelos SQLAlchemy
├── models.py            # Schemas Pydantic
├── document_parser.py   # Parser PDF/DOCX
├── qdpx_parser.py       # Parser Atlas.ti
├── requirements.txt     # Dependencias
└── prompts/             # Prompts v3.0
    ├── PHENOMFLOW_v3_PARTE_1_ANALISIS_INDIVIDUAL.txt
    ├── PHENOMFLOW_v3_PARTE_2_SINTESIS_CODEBOOK.txt
    └── PHENOMFLOW_v3_PARTE_3_FINAL_VALIDACION.txt
```

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Crear `.env` en la raíz del proyecto:

```env
ANTHROPIC_API_KEY=sk-ant-api03-...
USE_CLAUDE=true
```

## Ejecutar

```bash
python3 service.py
```

Servidor disponible en `http://localhost:8000`

## Endpoints

### `GET /health`
Health check del servidor.

**Response:**
```json
{
  "status": "healthy",
  "model": "claude-sonnet-4-20250514",
  "use_claude": true,
  "timestamp": "2025-12-09T09:00:00"
}
```

### `POST /analyze`
Análisis básico sin contexto.

**Request:**
```json
{
  "text": "U1: Participante: ...",
  "participant_id": "P01"
}
```

### `POST /analyze/enhanced`
Análisis con contexto de investigación (PRINCIPAL).

**Request:**
```json
{
  "text": "U1: Participante: ...",
  "context": {
    "research_question": "...",
    "study_objective": "...",
    "phenomenological_approach": "Giorgi",
    "participant_context": "...",
    "interview_type": "Semi-estructurada",
    "interview_timing": "Post-experiencia"
  }
}
```

**Response:**
```json
{
  "codebook": {...},
  "temporal_structures": {...},
  "clustering": {...},
  "body_maps": {...},
  "validation": {...},
  "metadata": {...}
}
```

### `POST /analyze/document`
Análisis de documentos PDF/DOCX (no implementado).

## Funciones Principales

### `analyze_individual_interview(text, participant_id)`
Análisis individual con prompt v3.0.

### `perform_cross_case_synthesis(analyses)`
Síntesis cross-case de múltiples participantes.

### `perform_validation(synthesis_result, individual_results)`
Validación científica (saturación, consistencia).

### `generate_body_maps(codebook, clustering)`
Generación de mapas corporales por estructura.

## Modelo de IA

Por defecto: `claude-sonnet-4-20250514`

Para cambiar, editar línea 37 en `service.py`:
```python
MODEL = "claude-sonnet-4-20250514"
```

## Prompts

Los prompts v3.0 están embebidos en `service.py` (líneas 70-340).

Opcionalmente, pueden cargarse desde archivos en `prompts/`:
- `PHENOMFLOW_v3_PARTE_1_ANALISIS_INDIVIDUAL.txt`
- `PHENOMFLOW_v3_PARTE_2_SINTESIS_CODEBOOK.txt`
- `PHENOMFLOW_v3_PARTE_3_FINAL_VALIDACION.txt`

## Desarrollo

### Tests
```bash
cd ..
python3 tests/unit/test_body_map.py
```

### Debug
```bash
python3 tests/debug/debug_anthropic.py
```
