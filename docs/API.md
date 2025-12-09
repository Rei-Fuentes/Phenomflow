# PhenomFlow API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required for local development.

---

## Endpoints

### Health Check

#### `GET /health`

Verifica el estado del servidor.

**Response:**
```json
{
  "status": "healthy",
  "model": "claude-sonnet-4-20250514",
  "use_claude": true,
  "timestamp": "2025-12-09T09:00:00.000000"
}
```

---

### Basic Analysis

#### `POST /analyze`

Análisis básico sin contexto de investigación.

**Request Body:**
```json
{
  "text": "U1: Participante: Sentí una presión en el pecho...",
  "participant_id": "P01"
}
```

**Response:**
```json
{
  "participant_id": "P01",
  "reliability_assessment": {...},
  "chronological_reconstruction": {...},
  "phenomenon_nucleus": "Síntesis narrativa...",
  "dimensional_statistics": {...},
  "markdown_table": "| Unidad | Cita | CORP | AFEC | COG | MOT | TEMP | REL |\n...",
  "dominant_trajectories": {...}
}
```

---

### Enhanced Analysis (PRINCIPAL)

#### `POST /analyze/enhanced`

Análisis con contexto de investigación completo.

**Request Body:**
```json
{
  "text": "U1: Participante: ...\nU2: Participante: ...",
  "context": {
    "research_question": "¿Cómo experimentan los participantes...?",
    "study_objective": "Comprender la estructura experiencial de...",
    "phenomenological_approach": "Giorgi",
    "participant_context": "Adultos jóvenes con experiencia de...",
    "interview_type": "Semi-estructurada",
    "interview_timing": "Post-experiencia inmediata"
  }
}
```

**Response:**
```json
{
  "codebook": {
    "CORPORAL": {
      "Sensaciones_Localizadas": {
        "Pecho": [
          {
            "code": "presion-pecho-alta-estatica",
            "participants": ["P01", "P02"],
            "evidence": ["Sentí una presión fuerte...", "..."],
            "count": 5
          }
        ]
      }
    },
    "AFECTIVA": {...},
    "COGNITIVA": {...},
    "MOTIVACIONAL": {...},
    "TEMPORAL": {...},
    "RELACIONAL": {...}
  },
  "temporal_structures": {
    "P01": {
      "participant_id": "P01",
      "phases": [
        {
          "phase_name": "Fase de Alarma Inicial",
          "temporal_segment": "0-5 segundos",
          "description": "Activación súbita...",
          "key_moments": ["Primer contacto", "Reconocimiento"]
        }
      ],
      "nuclear_metaphors": ["Como una banda apretando", "..."],
      "inflection_points": ["Momento de máxima intensidad", "..."]
    }
  },
  "clustering": {
    "structures": [
      {
        "structure_id": 1,
        "structure_name": "Estructura de Intensificación Progresiva",
        "participants": ["P01", "P03"],
        "description": "Caracterizada por escalada gradual...",
        "shared_patterns": ["Inicio súbito", "Pico de intensidad", "..."]
      }
    ],
    "dimensions": {
      "CORPORAL": {
        "coverage_percentage": 85,
        "dominant_codes": ["presion-pecho", "tension-hombros"]
      },
      "AFECTIVA": {
        "coverage_percentage": 92,
        "dominant_codes": ["ansiedad-alta", "miedo-intenso"]
      }
    }
  },
  "body_maps": {
    "structures": [
      {
        "structure_id": 1,
        "structure_name": "Estructura 1",
        "participants": ["P01"],
        "zones": {
          "chest": {
            "count": 5,
            "codes": [
              {
                "code": "presion-pecho-alta-estatica",
                "participant_id": "P01",
                "frequency": 3
              }
            ],
            "quotes": ["Sentí una presión fuerte en el pecho", "..."]
          },
          "head": {...},
          "extremities": {...}
        }
      }
    ]
  },
  "validation": {
    "saturation": {
      "achieved": false,
      "percentage": 45
    },
    "consistency_tests": {
      "intercoder": {
        "passed": false,
        "score": 0.0
      },
      "intracoder": {
        "passed": false,
        "score": 0.0
      }
    },
    "checklist_score": 0
  },
  "metadata": {
    "analysis_date": "2025-12-09T09:00:00.000000",
    "model": "claude-sonnet-4-20250514",
    "phenomflow_version": "3.0",
    "context_used": true,
    "text_length": 1234
  }
}
```

---

### Document Analysis

#### `POST /analyze/document`

Análisis de documentos PDF/DOCX.

**Status:** ❌ No implementado (retorna 501)

**Planned Request:**
```
Content-Type: multipart/form-data

files: [File, File, ...]
protocol: File (opcional)
context: JSON string
```

---

## Data Models

### ResearchContext
```typescript
{
  research_question?: string
  study_objective?: string
  phenomenological_approach?: string
  participant_context?: string
  interview_type?: string
  interview_timing?: string
}
```

### BodyMapZone
```typescript
{
  count: number
  codes: Array<{
    code: string
    participant_id: string
    frequency: number
  }>
  quotes: string[]
}
```

### ValidationResult
```typescript
{
  saturation: {
    achieved: boolean
    percentage: number
  }
  consistency_tests: {
    intercoder: { passed: boolean; score: number }
    intracoder: { passed: boolean; score: number }
  }
  checklist_score: number  // 0-45
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing 'text' field"
}
```

### 500 Internal Server Error
```json
{
  "error": "Error message details"
}
```

### 501 Not Implemented
```json
{
  "error": "Not implemented yet"
}
```

---

## Rate Limiting

El backend implementa retry automático con exponential backoff para manejar rate limits de Anthropic:
- Máximo 5 reintentos
- Delay inicial: 10 segundos
- Multiplicador: 2x + jitter aleatorio

---

## CORS

CORS habilitado para todos los orígenes (`*`) en desarrollo.

**Producción**: Configurar para dominio específico.

---

## Notes

- Análisis puede tardar 5-15 minutos dependiendo de la longitud del texto
- Modelo Claude tiene límite de 8k tokens por minuto
- JSON responses pueden incluir markdown code blocks que se limpian automáticamente
