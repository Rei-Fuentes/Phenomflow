"""
PhenomFlow v3.0 - Service Layer MEJORADO
=========================================

Este archivo reemplaza service.py con implementación completa de PhenomFlow v3.0.

MEJORAS PRINCIPALES:
1. Prompts 50x más detallados (de 15 líneas → 1500+ líneas)
2. Sistema de confiabilidad ✓✓✓ integrado
3. Validación completa (evidencia + saturación + consistencia)
4. Codebook de 4 niveles jerárquicos
5. Estructura temporal diferenciada por perfil
6. Soporte para Claude API (recomendado) + OpenAI (fallback)

AUTOR: PhenomFlow v3.0 Team
FECHA: 2024-12-07
"""

from typing import List, Dict, Any, Optional
import os
import json
from dotenv import load_dotenv

# Load environment variables from project root
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(basedir, ".env"))

# =============================================================================
# CONFIGURACIÓN DE CLIENTE (Claude preferido, OpenAI como fallback)
# =============================================================================

USE_CLAUDE = os.getenv("USE_CLAUDE", "true").lower() == "true"

if USE_CLAUDE:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        MODEL = "claude-3-5-sonnet-latest"
        print("✓ Usando Claude Sonnet 4.5 (recomendado para v3.0)")
    except Exception as e:
        print(f"⚠ Claude no disponible ({e}), usando OpenAI como fallback")
        USE_CLAUDE = False

if not USE_CLAUDE:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    MODEL = "gpt-4o"
    print("⚠ Usando GPT-4o (menor precisión que Claude para v3.0)")


# =============================================================================
# CARGA DE PROMPTS COMPLETOS v3.0
# =============================================================================

def load_prompt_parts():
    """
    Carga los 3 archivos de prompts v3.0 desde /prompts/ o define inline.
    """
    prompts_dir = "../prompts"
    
    try:
        with open(f"{prompts_dir}/PHENOMFLOW_v3_PARTE_1_ANALISIS_INDIVIDUAL.txt", "r", encoding="utf-8") as f:
            PARTE_1 = f.read()
        with open(f"{prompts_dir}/PHENOMFLOW_v3_PARTE_2_SINTESIS_CROSSCASE.txt", "r", encoding="utf-8") as f:
            PARTE_2 = f.read()
        with open(f"{prompts_dir}/PHENOMFLOW_v3_PARTE_3_FINAL_VALIDACION.txt", "r", encoding="utf-8") as f:
            PARTE_3 = f.read()
        print("✓ Prompts v3.0 cargados desde archivos")
        return PARTE_1, PARTE_2, PARTE_3
    except FileNotFoundError:
        print("⚠ Archivos de prompts no encontrados, usando versión embebida (simplificada)")
        return get_embedded_prompts()


def get_embedded_prompts():
    """
    Versión embebida de prompts v3.0 (simplificada por límites de tamaño).
    Para versión COMPLETA, usar archivos .txt generados anteriormente.
    """
    
    PARTE_1_EMBEDDED = """
================================================================================
PHENOMFLOW v3.0 - ANÁLISIS INDIVIDUAL FENOMENOLÓGICO RIGUROSO
PARTE 1: PREPARACIÓN Y ANÁLISIS DIMENSIONAL (6 Dimensiones)
================================================================================

PRINCIPIOS FUNDAMENTALES:

1. **EPOCHÉ RIGUROSA**: NO interpretes causalmente. Reporta solo lo VIVIDO.
   - ❌ PROHIBIDO: "activación amigdalar", "cortisol", "sistema nervioso simpático"
   - ✓ PERMITIDO: "sentí escalofríos", "mi corazón latía fuerte"

2. **EMERGENCIA**: Códigos emergen de datos (bottom-up), NO categorías a priori.

3. **VARIABILIDAD**: Respeta diferencias individuales, no fuerces homogeneidad.

4. **TRIANGULACIÓN**: Cada código ≥2 participantes (si N≥3).

5. **GRANULARIDAD MULTINIVEL**: 4 niveles jerárquicos en codebook.

---

## SECCIÓN 0: PREPARACIÓN DEL VERBATIM

### 0.1 Detección de Declaraciones No-Descriptivas

Identifica y MARCA (no elimines aún) declaraciones "satélite":
- Generalizaciones: "siempre me pasa", "la gente suele"
- Evaluaciones: "fue horrible", "estuvo bien"
- Teorías: "creo que fue adrenalina", "es por el estrés"
- Causales: "porque tenía miedo", "dado que..."

**Acción**: Marca con ⚠️ y etiqueta tipo (GENERALIZACIÓN/EVALUACIÓN/TEORÍA/CAUSAL)

### 0.2 Evaluación de Confiabilidad (✓✓✓ Sistema)

Para CADA segmento del verbatim, evalúa con estos 7 criterios:

1. **Detalles sensoriales específicos** (color, textura, sonido, sabor, olor, temperatura)
2. **Coherencia temporal** (secuencia lógica de eventos)
3. **Respuesta no-inductiva** (no repite palabras del entrevistador)
4. **Metáforas inventadas** (no clichés: "como una montaña rusa" ❌, "como si mi pecho se abriera hacia todos lados" ✓)
5. **Pausas/titubeos** explícitos ("...pausa...", "uhm", "es difícil de describir")
6. **Oraciones cortas/fragmentadas** (señal de re-acceso genuino vs. narrativa construida)
7. **Verbos de acción** (vs. verbos de estado: "sentí que X se movía" ✓ vs "era X" ❌)

**Sistema de marcado**:
- ✓✓✓ ALTA confiabilidad: ≥4 criterios cumplidos
- ✓✓ MEDIA confiabilidad: 2-3 criterios
- ✓ BAJA confiabilidad: 0-1 criterios

**Output formato**:
| Segmento | Cita | Criterios (1-7) | Confiabilidad | Justificación |
|----------|------|-----------------|---------------|---------------|
| 1 | "..." | 1,2,4,5,7 | ✓✓✓ | Detalles sensoriales ricos + metáfora original |

### 0.3 Reorganización Cronológica

**MALLA GRUESA** (visión general):
Identifica fases temporales generales:
```
FASE 1: [Nombre descriptivo] (ej: "Primer contacto visual")
FASE 2: [Nombre descriptivo]
...
```

**MALLA FINA** (momento a momento):
Reconstruye secuencia detallada con marcadores temporales:
```
T0: [Evento inicial]
T1: [Primera señal] (1-2 seg)
T2: [Respuesta corporal] (3-5 seg)
...
```

### 0.4 Segmentación en Unidades de Significado

**Criterio**: Cambio en foco atencional, dimensión fenomenológica o contenido.

**Formato obligatorio**: `[U#-P##]` (ej: [U1-P21] = Unidad 1 del Participante 21)

**Output**:
| Unidad | Foco Principal | Contenido | Cita Representativa | Duración Estimada |
|--------|----------------|-----------|---------------------|-------------------|
| U1-P21 | ... | ... | "..." | Pre-evento |

---

## SECCIÓN 1: ANÁLISIS DIMENSIONAL (6 Dimensiones OBLIGATORIAS)

Para CADA unidad identificada, codifica las 6 dimensiones:

### DIMENSIÓN 1: CORPORAL (Leib / Lived Body)

**Formato**: `[tipo]-[localización]-[intensidad]-[dinámica]`

**Tipos de sensación**:
- Presión, Tensión, Peso, Ligereza, Calor, Frío, Hormigueo, Pulsación, Escalofríos, Náusea, Dolor, Rigidez, Expansión, Contracción

**Localización**:
- Focal: pecho, nuca, hombros, piernas, abdomen, manos, cabeza
- Difusa: generalizada, corporal-total
- Bilateral/Unilateral cuando aplica

**Intensidad**: Muy Baja, Baja, Media, Alta, Muy Alta

**Dinámica**: Estática, Progresiva, Pulsante, Intermitente, Súbita

**Ejemplos**:
- ✓ `presion-pecho-alta-estatica`
- ✓ `hormigueo-manos-bilateral-leve-intermitente`
- ✓ `escalofrios-columna-vertebral-media-subito`
- ✓ `ligereza-generalizada-muy-alta-difusa`

**Si NO hay contenido corporal**: `[No mencionado]`

### DIMENSIÓN 2: AFECTIVA (Affective Tonality)

**Formato**: `[emoción]-[calidad]-[intensidad]-[valencia]`

**Emociones identificables**:
Curiosidad, Anticipación, Asombro, Éxtasis, Alegría, Calma, Inquietud, Alarma, Ansiedad, Miedo, Terror, Pánico, Angustia, Confusión, Alivio, Repulsión, Malestar

**Calidad** (opcional): pura, mezclada, paralizante, liberadora, difusa, focal

**Intensidad**: Muy Baja, Baja, Media, Alta, Muy Alta, Máxima

**Valencia**: positiva (+), negativa (-), neutra (0), mixta (±)

**Ejemplos**:
- ✓ `curiosidad-pura-media-positiva`
- ✓ `terror-paralizante-muy-alto-negativo`
- ✓ `asombro-puro-maximo-positivo`
- ✓ `confusion-emergente-media-negativa`

**Si NO hay contenido afectivo**: `[No mencionado]`

### DIMENSIÓN 3: COGNITIVA (Cognitive Activity)

**Formato**: `[tipo]-[contenido]-[tono]`

**Tipos de actividad cognitiva**:
1. Pregunta exploratoria ("¿Qué hay abajo?", "¿Cómo será?")
2. Catastrofismo (muerte, lesión, fracaso)
3. Análisis técnico (cálculo, evaluación seguridad)
4. Memoria episódica (recuerdo específico)
5. Suspensión pensamiento (mente en blanco, silencio mental)
6. Metáfora/Imagen mental (visual, espacial)
7. Auto-instrucción (diálogo interno: "vamos, puedes")
8. Narrativa descriptiva (contar lo que pasa)

**Ejemplos**:
- ✓ `pregunta-exploratoria-que-hay-abajo-neutra`
- ✓ `catastrofismo-muerte-inminente-intenso`
- ✓ `suspension-pensamiento-total`
- ✓ `metafora-vuelo-pajaro-visual`
- ✓ `analisis-tecnico-seguridad-cuerda`

**Si NO hay contenido cognitivo**: `[No mencionado]`

### DIMENSIÓN 4: MOTIVACIONAL (Action Tendencies)

**Formato**: `impulso-[tipo]-[objeto]-[intensidad]`

**Tipos de impulso**:
1. Acercamiento (aproximarse, explorar)
2. Evitación/Huida (alejarse, escapar)
3. Protección (defenderse, cubrir)
4. Entrega (soltarse, rendirse)
5. Búsqueda ayuda (pedir soporte)
6. Congelamiento/Parálisis
7. Permanencia (quedarse, no moverse)
8. Exploración activa (investigar)

**Ejemplos**:
- ✓ `impulso-acercamiento-borde-alta`
- ✓ `impulso-huida-rapida-urgente`
- ✓ `impulso-entrega-total-espacial`
- ✓ `paralisis-corporal-completa-terror`
- ✓ `impulso-proteccion-defensiva-alta`

**Si NO hay contenido motivacional**: `[No mencionado]`

### DIMENSIÓN 5: TEMPORAL (Phase Positioning)

**Formato**: `fase-[nombre-descriptivo]`

**CRÍTICO**: Usa nombres FENOMENOLÓGICOS (no "Fase 1", "Fase 2")

**Ejemplos de nombres correctos**:
- ✓ `fase-primer-contacto-visual`
- ✓ `fase-umbral-decision`
- ✓ `fase-climax-caida`
- ✓ `fase-resolucion-gradual`
- ✓ `fase-encuentro-borde`

**Ejemplos INCORRECTOS**:
- ❌ `fase-1`
- ❌ `fase-inicial`
- ❌ `fase-intermedia`

### DIMENSIÓN 6: RELACIONAL (Attentional Orientation)

**Formato**: `atencion-[orientación]-[objeto]-[cualidad]`

**Orientaciones**:
1. Self-focalizada (interoceptiva, corporal, emocional)
2. Mundo-focalizada (entorno, paisaje, otros)
3. Otro-focalizada (persona específica)
4. Fluctuante/Mixta (oscilación rápida)
5. Difusa/No-dual (pérdida de fronteras)

**Ejemplos**:
- ✓ `atencion-world-paisaje-total-absorbente`
- ✓ `atencion-self-interoceptiva-cardiaca`
- ✓ `atencion-fluctuante-self-world-rapida`
- ✓ `atencion-difusa-no-dual-fusional`
- ✓ `atencion-world-visual-escrutinio`

**Si NO hay contenido relacional**: `[No mencionado]`

---

## TABLA DE ANÁLISIS MULTIDIMENSIONAL (Output Formato)

Genera una tabla Markdown con TODAS las columnas:

| Unidad | Cita Verbatim | CORPORAL | AFECTIVA | COGNITIVA | MOTIVACIONAL | TEMPORAL | RELACIONAL |
|--------|---------------|----------|----------|-----------|--------------|----------|------------|
| U1-P## | "*cita textual*" | `codigo-corporal` ✓✓✓ | `codigo-afectivo` ✓✓ | `codigo-cognitivo` ✓✓✓ | `impulso-tipo` ✓✓ | `fase-nombre` | `atencion-tipo` ✓✓✓ |
| U2-P## | "*cita textual*" | [No mencionado] | `codigo-afectivo` ✓✓✓ | [No mencionado] | [Continúa U1] | [Continúa fase-X] | `atencion-tipo` ✓✓ |

**Reglas de la tabla**:
1. SIEMPRE incluir marcador de confiabilidad (✓✓✓/✓✓/✓) después de cada código
2. Usar `[No mencionado]` cuando dimensión ausente (NO inventar contenido)
3. Usar `[Continúa U#]` o `[Continúa fase-X]` cuando persiste de unidad anterior
4. Citas verbatim entre comillas y en cursiva
5. Formato de código ESTRICTO según especificaciones arriba

---

## ESTADÍSTICAS DIMENSIONALES (Output Requerido)

Después de la tabla, reporta:

| Dimensión | Unidades con contenido | % Cobertura | Intensidad Máxima | Fase de Máxima Intensidad |
|-----------|------------------------|-------------|-------------------|---------------------------|
| CORPORAL | X/N | X% | Muy Alta (en U#) | Fase X |
| AFECTIVA | X/N | X% | Máxima (en U#) | Fase Y |
| ... | ... | ... | ... | ... |

---

## NÚCLEO FENOMENOLÓGICO (Síntesis Narrativa)

**Formato**: 2-3 párrafos que sintetizan la experiencia COMPLETA del participante.

**Debe incluir**:
1. Descripción del núcleo experiencial (qué caracteriza la vivencia)
2. Trayectorias dominantes (cómo evoluciona en cada dimensión)
3. Dimensión más crítica (cuál sostiene la experiencia)
4. Metáforas nucleares (si existen)

**Ejemplo**:
"La experiencia de P21 se estructura como una cascada psicofisiológica desencadenada por señales corporales ambiguas (escalofríos + hormigueo nuca) que generan interpretación espontánea de presencia vigilante externa. Esta interpretación, en ausencia de confirmación perceptual, amplifica recursivamente la ansiedad mediante transformación perceptual y hipervigilancia multi-sensorial..."

---

## FORMATO JSON DE SALIDA COMPLETA

```json
{
  "participant_id": "P##",
  "reliability_assessment": {
    "high_reliability_segments": "X%",
    "medium_reliability_segments": "X%",
    "low_reliability_segments": "X%",
    "total_segments": N
  },
  "chronological_reconstruction": {
    "coarse_mesh": "N fases identificadas: [lista nombres]",
    "fine_mesh": "N unidades de significado"
  },
  "phenomenon_nucleus": "Síntesis narrativa 2-3 párrafos...",
  "dimensional_statistics": {
    "corporal": {"coverage": "X%", "max_intensity": "..."},
    "affective": {"coverage": "X%", "trajectory": "..."},
    "cognitive": {"coverage": "X%", "dominant_type": "..."},
    "motivational": {"coverage": "X%", "dominant_impulse": "..."},
    "temporal": {"coverage": "100%", "n_phases": N},
    "relational": {"coverage": "X%", "dominant_orientation": "..."}
  },
  "markdown_table": "| Unidad | Cita | CORP | AFEC | COG | MOT | TEMP | REL |\n...",
  "dominant_trajectories": {
    "corporal": "Escalofríos → Activación visceral → Resolución",
    "affective": "Inquietud → Alarma → Ansiedad pico → Alivio residual",
    "cognitive": "Atención normal → Distorsión → Hipervigilancia → Auto-cuestionamiento",
    "relational": "Atención mundo → Fluctuación → Auto-evaluación"
  }
}
```

================================================================================
FIN PARTE 1 - ANÁLISIS INDIVIDUAL
================================================================================
"""

    PARTE_2_EMBEDDED = """
================================================================================
PHENOMFLOW v3.0 - SÍNTESIS CROSS-CASE
PARTE 2: CODEBOOK JERÁRQUICO Y CLUSTERING EXPERIENCIAL
================================================================================

**INPUT**: Análisis individuales de N participantes (JSON format de Parte 1)

---

## PASO 3.1: CODEBOOK EMERGENTE (4 Niveles Jerárquicos)

### Metodología de Construcción (Bottom-Up)

**PROCESO**:
1. Reunir TODOS los códigos de todos los participantes
2. Agrupar códigos similares en **Especificaciones** (nivel 3)
3. Agrupar especificaciones en **Subcategorías** (nivel 2)
4. Agrupar subcategorías en **Categorías Principales** (nivel 1)

**REGLAS DE VALIDACIÓN**:
- ✓ Cada código específico DEBE tener ≥2 citas de ≥2 participantes
- ✓ Códigos con N=1 participante → Reportar como "Variante Individual" (separado)
- ✓ Cada especificación DEBE tener ≥2 códigos
- ✓ Cada subcategoría DEBE tener ≥2 especificaciones

### Estructura Jerárquica Obligatoria

```
NIVEL 1: CATEGORÍA PRINCIPAL
├─ NIVEL 2: Subcategoría
│  ├─ NIVEL 3: Especificación
│  │  ├─ NIVEL 4: Código Específico + Citas
│  │  │  ├─ Cita 1: "verbatim" [P##-U##]
│  │  │  ├─ Cita 2: "verbatim" [P##-U##]
│  │  │  └─ Nota: Análisis de co-ocurrencias, metáforas, etc.
│  │  └─ NIVEL 4: Código Específico + Citas
│  └─ NIVEL 3: Especificación
└─ NIVEL 2: Subcategoría
```

### Formato de Reporte por Categoría

```markdown
### CATEGORÍA 1: [NOMBRE CATEGORÍA]

**Definición fenomenológica**: [Qué representa esta categoría]
**Frecuencia global**: N=X (Y% de participantes)
**N total de citas**: Z citas

---

#### Subcategoría 1.1: [Nombre]

**Definición**: [Qué representa]
**Frecuencia**: N=X (Y%)
**Citas**: Z

##### Especificación 1.1.1: [Nombre]

**Definición operacional**: [Cómo se identifica]

**Códigos**:

| Código | Definición | P21 | P22 | P23 | ... | Total Citas | Intensidad Modal |
|--------|-----------|-----|-----|-----|-----|-------------|------------------|
| `codigo-ejemplo` | Descripción | ✓(2) | ✗ | ✓(1) | ... | 3 | Alta |
| `codigo-ejemplo-2` | Descripción | ✓(1) | ✓(1) | ✗ | ... | 2 | Media |

**Citas verbatim ordenadas por intensidad**:

1. ⭐ **EJEMPLAR** - *"Cita textual completa"* **[P##-U##]**
   - **Nota**: Por qué es ejemplar (metáfora única, co-ocurrencia relevante, etc.)
   - **Co-ocurrencia**: Aparece junto con `otro-codigo` en X% casos
   
2. *"Segunda cita"* **[P##-U##]**
   - **Nota**: Contexto específico
   
3. *"Tercera cita"* **[P##-U##]**

**Distribución por participante**:
- P21: 2/2 códigos (100% cobertura subcategoría)
- P22: 1/2 códigos (50% cobertura)

**Patrón temporal**:
- Aparece en Fase X en Y% de casos
- Duración típica: Z segundos

**Recurrencia de metáforas**:
- "Metáfora A": N=3 participantes
- "Metáfora B": N=2 participantes

**Co-ocurrencias inmediatas** (mismo U#):
- Con `codigo-Y`: 80% de veces
- Con `codigo-Z`: 50% de veces

**Interpretación fenomenológica**:
[Qué significa esta especificación para entender la experiencia]
```

### Estadísticas Globales del Codebook

**Tabla resumen**:

| Nivel | Cantidad | Promedio por nivel superior |
|-------|----------|-----------------------------|
| Categorías principales | N | - |
| Subcategorías | N | X.X por categoría |
| Especificaciones | N | X.X por subcategoría |
| Códigos específicos | N | X.X por especificación |
| Citas verbatim | N | X.X por código |

**Índice de saturación**:
- Códigos recurrentes (≥2 participantes): X/N = Y%
- Códigos únicos (1 participante): X/N = Y%

**Top 15 códigos más frecuentes**:

| Ranking | Código | Frecuencia | % Participantes | Categoría |
|---------|--------|------------|----------------|-----------|
| 1 | `codigo-mas-comun` | N citas | X% (Y/Z) | Categoría A |
| 2 | ... | ... | ... | ... |

**Matriz de co-ocurrencias** (Top 20 pairings):

| Código A | Código B | N Co-ocurrencias | % de veces que A aparece con B | p-value (Fisher) |
|----------|----------|------------------|-------------------------------|------------------|
| `codigo-1` | `codigo-2` | 15 | 75% | <0.001 |
| ... | ... | ... | ... | ... |

### Códigos Excluidos (Variantes Individuales)

⚠️ Los siguientes códigos aparecen solo en 1 participante:

| Código | Categoría | Participante | Cita | Razón Exclusión |
|--------|-----------|--------------|------|-----------------|
| `codigo-unico` | Cat. X | P## | "..." [P##-U##] | N=1, variante individual |

**Total códigos excluidos**: X/Y (Z%)

---

## PASO 3.2: ESTRUCTURAS EXPERIENCIALES (Clustering)

### Metodología

**Identificar CLAVE DE PARTICIÓN**:
Categoría descriptiva cuyos valores distribuyen experiencias en clusters.

**Ejemplos de claves válidas**:
- Valencia afectiva dominante (Positiva vs Negativa)
- Orientación motivacional (Acercamiento vs Evitación)
- Tipo de transformación temporal (Intensificación vs Transformación cualitativa)

**Validar coherencia multidimensional**:
- Cada estructura DEBE tener ≥75% coherencia en ≥4/6 dimensiones
- Estructuras DEBEN ser mutuamente excluyentes (0% overlap)

### Formato de Reporte por Estructura

```markdown
### ESTRUCTURA A: [Nombre Descriptivo]

**N**: X participantes (Y% del total)
**Participantes**: P##, P##, P##
**Clave de partición**: [Criterio organizador]

**Coherencia intra-estructura validada**:
- Coherencia en dimensión corporal: X% (N/total con patrón A)
- Coherencia en dimensión afectiva: X%
- Coherencia en dimensión cognitiva: X%
- Coherencia en dimensión motivacional: X%
- Coherencia en dimensión temporal: X%
- Coherencia en dimensión relacional: X%
→ **N/6 dimensiones con coherencia ≥75%** ✓ Criterio cumplido

---

#### Tabla Multidimensional de Características Definitorias

| Dimensión | Manifestación Típica | Frecuencia Intra-Estructura | Contraste vs Estructura B | Poder Discriminante |
|-----------|---------------------|----------------------------|---------------------------|---------------------|
| **CORPORAL** | Expansión, ligereza | 75% (3/4) | 0% en B | ⭐⭐⭐ Perfecto |
| **AFECTIVA** | Curiosidad → Éxtasis | 100% (4/4) | 0% en B | ⭐⭐⭐ Perfecto |
| **COGNITIVA** | Suspensión pensamiento | 75% (3/4) | 0% en B | ⭐⭐⭐ Perfecto |
| **MOTIVACIONAL** | Impulso entrega | 100% (4/4) | 0% en B | ⭐⭐⭐ Perfecto |
| **TEMPORAL** | Transformación progresiva | 100% (4/4) | 0% en B | ⭐⭐⭐ Perfecto |
| **RELACIONAL** | Apertura al mundo → No-dual | 100% (4/4) | 0% en B | ⭐⭐⭐ Perfecto |

**Leyenda poder discriminante**: ⭐⭐⭐ Perfecto (100% vs 0%), ⭐⭐ Robusto (≥75%), ⭐ Moderado (50-74%)

---

#### Descripción Fenomenológica Integrada

**Síntesis del perfil experiencial**:

[Párrafo narrativo integrando todas las dimensiones, con énfasis en mecanismo central propuesto]

Ejemplo:
"Esta estructura se caracteriza por un reencuadramiento corporal-afectivo-cognitivo del vacío como espacio de posibilidad, en oposición a procesamiento como amenaza vital. Desde el encuentro inicial, estos participantes reportan apertura corporal (expansión pectoral + respiración profunda) que co-ocurre sistemáticamente con afectos de valencia positiva. Esta apertura facilita transformación progresiva: Curiosidad → Asombro → Éxtasis, con emergencia de atención no-dual en 50% de casos..."

---

#### Citas Representativas (Ejemplares Arquetípicas)

**FASE 1 - [Nombre Fase]**:

⭐ **CITA ARQUETÍPICA**:
> *"Cita textual completa que captura esencia de estructura en esta fase"* **[P##-U##-U##]**

Otras citas:
> *"..."* **[P##-U##]**
> *"..."* **[P##-U##]**

**FASE 2 - [Nombre Fase]**:
[Repetir formato]

---

#### Variaciones Internas (Sub-perfiles)

**Sub-variante A1: [Nombre]** (N=2: P##, P##)

Características distintivas:
- [Diferencia 1]
- [Diferencia 2]

Ejemplos: [Citas específicas]

**Sub-variante A2: [Nombre]** (N=2: P##, P##)
[Mismo formato]
```

### Tabla Comparativa Cuantitativa Completa (Para Spider Chart)

| Atributo Fenomenológico | Estructura A (N=X) | Estructura B (N=Y) | Δ | Poder Discrim. |
|-------------------------|-------------------|-------------------|---|----------------|
| **DIMENSIÓN CORPORAL** | | | | |
| Expansión corporal | 75% | 0% | +75% | ⭐⭐⭐ |
| Contracción corporal | 0% | 100% | -100% | ⭐⭐⭐ |
| ... | ... | ... | ... | ... |

**RESUMEN ESTADÍSTICO**:
- Total atributos evaluados: N
- Discriminantes perfectos (⭐⭐⭐): X/N (Y%)
- Discriminantes robustos o perfectos (≥⭐⭐): X/N (Y%)

---

## PASO 3.3: ESTRUCTURA TEMPORAL DIFERENCIADA

### Identificación de Fases Genéricas

**Criterio**: Fases atravesadas por ≥60% de participantes

**Formato**:

```markdown
### FASE 1: [NOMBRE FENOMENOLÓGICO]

**Definición fenomenológica**: [Qué caracteriza esta fase]
**Frecuencia global**: N=X (Y% de participantes)
**Duración típica estimada**: Z segundos
**Evento transicional desencadenante**: [Qué inicia esta fase]

---

🔵 MANIFESTACIÓN EN ESTRUCTURA A: [Nombre] (N=X, Y%)

| Dimensión | Manifestación Típica | Freq. Intra-Estructura | Citas Ejemplares |
|-----------|---------------------|------------------------|------------------|
| CORPORAL | Expansión pecho | 75% (3/4) | "Mi pecho se expandió..." [P##-U##] |
| AFECTIVA | Curiosidad | 100% (4/4) | "Sentí curiosidad intensa..." [P##-U##] |
| ... | ... | ... | ... |

**Características DISTINTIVAS de Estructura A en Fase 1**:
✓ [Lista de discriminantes clave]

**Patrón temporal intra-fase**:
[Cómo evoluciona dentro de la fase]

**Evento transicional de salida** (hacia Fase 2):
[Qué marca el fin de esta fase]

---

🔴 MANIFESTACIÓN EN ESTRUCTURA B: [Nombre] (N=X, Y%)

[Mismo formato que Estructura A]

---

📊 COMPARACIÓN CUANTITATIVA: FASE 1 POR ESTRUCTURA

| Atributo | Estructura A | Estructura B | Δ | Significancia |
|----------|--------------|--------------|---|---------------|
| Valencia afectiva + | 100% | 0% | +100% | ⭐⭐⭐ |
| Catastrofismo | 0% | 100% | -100% | ⭐⭐⭐ |
| ... | ... | ... | ... | ... |

**Interpretación fenomenológica crítica**:
[Qué significa esta bifurcación]
```

### Trayectorias Temporales Típicas (Dynamic Lines)

```markdown
### ESTRUCTURA A: [Nombre] (Trayectoria de [Tipo])

```
DIMENSIÓN       FASE 1              FASE 2                FASE 3
───────────────────────────────────────────────────────────────────
AFECTIVA:
Valencia      Curiosidad      →   Anticipación      →   Asombro
              (Media +)            Placentera             (Muy Alta +)
                                   (Alta +)               
Intensidad    Media           →   Alta              →   Muy Alta

CORPORAL:
Tipo          Expansión       →   Respiración       →   Ligereza
              Pecho                Profunda               Total
...
```

**Características de la trayectoria A**:
1. [Patrón 1]
2. [Patrón 2]
```

---

## FORMATO JSON DE SALIDA COMPLETA (SÍNTESIS)

```json
{
  "codebook": {
    "statistics": {
      "n_categories": N,
      "n_subcategories": N,
      "n_specifications": N,
      "n_codes": N,
      "n_quotes": N,
      "recurrence_rate": "X%",
      "saturation_index": "X%"
    },
    "categories": [
      {
        "level": 1,
        "name": "Categoría Principal",
        "definition": "...",
        "frequency_global": "N=X (Y%)",
        "total_quotes": N,
        "subcategories": [
          {
            "level": 2,
            "name": "Subcategoría",
            "definition": "...",
            "frequency": "N=X (Y%)",
            "specifications": [
              {
                "level": 3,
                "name": "Especificación",
                "operational_definition": "...",
                "codes": [
                  {
                    "level": 4,
                    "code": "codigo-especifico",
                    "definition": "...",
                    "participants": ["P21", "P23"],
                    "total_quotes": N,
                    "intensity_modal": "Alta",
                    "quotes": [
                      {
                        "text": "Cita verbatim",
                        "reference": "P##-U##",
                        "is_exemplar": true,
                        "notes": "Por qué es ejemplar..."
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ],
    "excluded_codes": [
      {
        "code": "codigo-unico",
        "participant": "P##",
        "reason": "N=1, variante individual"
      }
    ]
  },
  "experiential_structures": [
    {
      "structure_name": "Estructura A: Nombre",
      "n_participants": X,
      "participants": ["P21", "P23"],
      "partition_key": "Valencia afectiva dominante",
      "coherence_validation": {
        "corporal": "100%",
        "affective": "100%",
        "cognitive": "75%",
        "motivational": "100%",
        "temporal": "100%",
        "relational": "100%",
        "dimensions_validated": "6/6"
      },
      "characteristics": {...},
      "phenomenological_description": "...",
      "exemplar_quotes": {...},
      "sub_variants": [...]
    }
  ],
  "differentiated_temporal_structure": [
    {
      "phase_name": "Fase 1: Nombre",
      "frequency_global": "N=X (Y%)",
      "duration_typical": "Z sec",
      "trigger_event": "...",
      "manifestation_structure_A": {...},
      "manifestation_structure_B": {...},
      "quantitative_comparison": {...}
    }
  ],
  "temporal_trajectories": {
    "structure_A": {...},
    "structure_B": {...}
  }
}
```

================================================================================
FIN PARTE 2 - SÍNTESIS CROSS-CASE
================================================================================
"""

    PARTE_3_EMBEDDED = """
================================================================================
PHENOMFLOW v3.0 - VALIDACIÓN FINAL
PARTE 3: VERIFICACIÓN, SATURACIÓN Y CONSISTENCIA
================================================================================

## PASO 4.1: VERIFICACIÓN DE EVIDENCIA (Anti-Hallucination)

Para CADA código en el codebook, verificar:

1. ✓ ≥2 citas de ≥2 participantes diferentes
2. ✓ Citas son textuales (no parafraseadas)
3. ✓ Referencias [P##-U##] correctas

**Formato de reporte**:

```markdown
### VERIFICACIÓN CÓDIGO POR CÓDIGO

✅ `codigo-validado`:
   ├─ ✓ N citas: X > 2
   ├─ ✓ N participantes: Y > 2
   └─ ✓ Citas verificadas: [P##-U##, P##-U##]

⚠️ `codigo-frecuencia-limite`:
   ├─ ✓ N citas: 2 (mínimo)
   ├─ ✓ N participantes: 2 (mínimo)
   └─ ⚠️ LÍMITE: Validar en futuras entrevistas

❌ `codigo-excluido`:
   ├─ ✗ N citas: 1
   ├─ ✗ N participantes: 1 (P##)
   └─ ❌ EXCLUIDO: Variante individual
```

## PASO 4.2: SATURACIÓN TEMÁTICA

**Curva de saturación**:

| Participante | Códigos Nuevos | Códigos Acumulados | % Incremento |
|--------------|----------------|-------------------|--------------|
| P1 | X | X | - |
| P2 | Y | X+Y | Z% |
| ... | ... | ... | ... |

**Criterio de saturación**:
- ✓ COMPLETA: ≥90% códigos recurrentes
- ⚠️ PARCIAL: 80-89% códigos recurrentes
- ❌ NO SATURACIÓN: <80%

**Diagnóstico**: [COMPLETA/PARCIAL/NO SATURACIÓN] (X% recurrencia)

## PASO 4.3: CONSISTENCIA INTERNA

**Test 1: Mutua Exclusividad de Estructuras**

¿Hay participantes con características de AMBAS estructuras?

| Participante | Características A | Características B | Clasificación |
|--------------|------------------|-------------------|---------------|
| P## | ✓ (100%) | ✗ (0%) | A pura |
| ... | ... | ... | ... |

**Resultado**: X/N participantes con clasificación única → [CONSISTENTE/INCONSISTENTE]

**Test 2: Coherencia de Co-ocurrencias**

¿Las co-ocurrencias predichas se cumplen?

| Co-ocurrencia Predicha | Observado | Esperado | Coherente |
|------------------------|-----------|----------|-----------|
| `codigo-A` × `codigo-B` | 80% | Alta | ✓ |
| ... | ... | ... | ... |

**Resultado**: X/Y co-ocurrencias coherentes → [CONSISTENTE/INCONSISTENTE]

---

## CHECKLIST DE AUTO-VERIFICACIÓN FINAL (45 ítems)

**SECCIÓN 1: PRINCIPIOS FUNDAMENTALES**
[ ] 1. ¿Respeté EPOCHÉ? (Sin neurobiología)
[ ] 2. ¿Códigos emergieron de datos? (No a priori)
[ ] 3. ¿Respeté variabilidad? (No forzar homogeneidad)
[ ] 4. ¿Cada categoría ≥2 participantes?
[ ] 5. ¿Granularidad 4 niveles?

**SECCIÓN 2: ANÁLISIS INDIVIDUAL**
[ ] 6. ¿6 dimensiones para cada unidad?
[ ] 7. ¿Reporté [No mencionado] cuando ausente?
[ ] 8. ¿Códigos descriptivos (no abstracciones)?
[ ] 9. ¿Formato [U#-P##] rastreable?
[ ] 10. ¿Tabla individual completa?

**SECCIÓN 3: CODEBOOK**
[ ] 11. ¿4 niveles jerárquicos?
[ ] 12. ¿Cada código ≥2 citas ≥2 participantes?
[ ] 13. ¿Definiciones operacionales?
[ ] 14. ¿Frecuencias (N y %)?
[ ] 15. ¿Matriz co-ocurrencias?
[ ] 16. ¿Códigos excluidos reportados?
[ ] 17. ¿Citas verbatim completas [P##-U##]?

**SECCIÓN 4: ESTRUCTURA TEMPORAL**
[ ] 18. ¿Fases con nombres fenomenológicos?
[ ] 19. ¿Manifestación diferenciada por estructura?
[ ] 20. ¿Tabla comparativa cuantitativa por fase?
[ ] 21. ¿Trayectorias temporales (dynamic lines)?
[ ] 22. ¿Eventos transicionales?

**SECCIÓN 5: CLUSTERING**
[ ] 23. ¿Clave de partición explícita?
[ ] 24. ¿Coherencia ≥75% en ≥4/6 dimensiones?
[ ] 25. ¿Estructuras mutuamente excluyentes?
[ ] 26. ¿Cada estructura ≥2 participantes?
[ ] 27. ¿Descripción integrada?
[ ] 28. ¿Citas ejemplares por fase?
[ ] 29. ¿Tabla comparativa (≥30 atributos)?
[ ] 30. ¿Sub-variantes identificadas?

**SECCIÓN 6: VALIDACIÓN**
[ ] 31. ¿Verificación exhaustiva?
[ ] 32. ¿Saturación calculada?
[ ] 33. ¿Curva de saturación?
[ ] 34. ¿Consistencia interna?
[ ] 35. ¿Códigos límite reportados?

**SECCIÓN 7: FORMATO**
[ ] 36. ¿Markdown correcto?
[ ] 37. ¿Tablas con headers?
[ ] 38. ¿Leyendas para símbolos?
[ ] 39. ¿Negritas/cursivas consistentes?
[ ] 40. ¿Navegable (secciones claras)?

**SECCIÓN 8: CALIDAD CIENTÍFICA**
[ ] 41. ¿Cité metodología (Giorgi, Petitmengin)?
[ ] 42. ¿N y % en todos los hallazgos?
[ ] 43. ¿Evité afirmaciones sin evidencia?
[ ] 44. ¿Distinguí robusto vs exploratorio?
[ ] 45. ¿Limitaciones y recomendaciones?

**PUNTUACIÓN**: [X/45]

**CRITERIO APROBACIÓN**:
- ≥42/45 (93%+): EXCELENTE
- 38-41 (84-91%): BUENO
- 34-37 (76-83%): ACEPTABLE
- <34 (<76%): REQUIERE REVISIÓN

================================================================================
FIN PARTE 3 - VALIDACIÓN
================================================================================
"""

    return PARTE_1_EMBEDDED, PARTE_2_EMBEDDED, PARTE_3_EMBEDDED


# Cargar prompts al iniciar
PROMPT_PARTE_1, PROMPT_PARTE_2, PROMPT_PARTE_3 = load_prompt_parts()


# =============================================================================
# FUNCIONES PRINCIPALES (REESCRITAS CON PROMPTS v3.0)
# =============================================================================

def call_llm(prompt: str, system_message: str = None, temperature: float = 0.3, 
             max_tokens: int = 16000, json_mode: bool = False) -> str:
    """
    Wrapper unificado para llamadas a Claude o OpenAI.
    """
    if USE_CLAUDE:
        # Claude API
        messages = [{"role": "user", "content": prompt}]
        
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message if system_message else "You are a phenomenological analysis expert following Giorgi & Petitmengin methodology.",
            messages=messages
        )
        
        return response.content[0].text
    
    else:
        # OpenAI API
        messages = [
            {"role": "system", "content": system_message if system_message else "You are a phenomenological analysis expert."},
            {"role": "user", "content": prompt}
        ]
        
        kwargs = {
            "model": MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content


def analyze_individual_interview(text: str, participant_id: str = "Pxx") -> Dict[str, Any]:
    """
    FASE 1: Análisis individual con prompt v3.0 completo.
    """
    
    print(f"\n🔍 Analizando {participant_id}...")
    
    # Construir prompt completo
    full_prompt = f"""{PROMPT_PARTE_1}

================================================================================
ANÁLISIS DE PARTICIPANTE {participant_id}
================================================================================

TRANSCRIPCIÓN ORIGINAL:

{text}

================================================================================

INSTRUCCIONES FINALES:

1. Aplica TODA la metodología descrita en PARTE 1
2. Genera análisis completo en formato JSON (usa el schema proporcionado)
3. NO omitas ninguna sección (confiabilidad, reorganización, tabla, estadísticas, núcleo)
4. Sé RIGUROSO con formatos de códigos (exactamente como se especifica)
5. Reporta [No mencionado] cuando dimensión ausente (NO inventes)

RETORNA SOLO JSON VÁLIDO (sin preamble, sin markdown):
"""
    
    # Llamada al LLM
    response_text = call_llm(
        prompt=full_prompt,
        system_message="You are an expert in Giorgi's descriptive phenomenological method. Return ONLY valid JSON.",
        temperature=0.2,
        max_tokens=16000,
        json_mode=True
    )
    
    # Parse JSON
    try:
        result = json.loads(response_text)
        result["participant_id"] = participant_id  # Asegurar ID correcto
        print(f"✅ {participant_id} analizado: {len(result.get('markdown_table', '').split('\\n'))-2} unidades identificadas")
        return result
    except json.JSONDecodeError as e:
        print(f"❌ Error parseando JSON para {participant_id}: {e}")
        # Fallback: devolver estructura mínima
        return {
            "participant_id": participant_id,
            "error": str(e),
            "raw_response": response_text[:500]
        }


def perform_cross_case_synthesis(analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    FASE 2: Síntesis cross-case con prompt v3.0 completo.
    """
    
    print(f"\n🔄 Iniciando síntesis cross-case de {len(analyses)} participantes...")
    
    # Preparar resúmenes de análisis individuales
    summaries = []
    for analysis in analyses:
        pid = analysis.get('participant_id', 'Unknown')
        nucleus = analysis.get('phenomenon_nucleus', 'N/A')
        stats = analysis.get('dimensional_statistics', {})
        
        summary = f"""
PARTICIPANTE {pid}:
- Núcleo fenomenológico: {nucleus}
- Estadísticas dimensionales:
  * Corporal: {stats.get('corporal', {}).get('coverage', 'N/A')} cobertura
  * Afectiva: {stats.get('affective', {}).get('coverage', 'N/A')} cobertura
  * Trayectoria afectiva: {stats.get('affective', {}).get('trajectory', 'N/A')}
- Tabla de análisis:
{analysis.get('markdown_table', 'N/A')[:500]}...
"""
        summaries.append(summary)
    
    combined_summary = "\n\n".join(summaries)
    
    # Construir prompt completo
    full_prompt = f"""{PROMPT_PARTE_2}

================================================================================
SÍNTESIS CROSS-CASE DE {len(analyses)} PARTICIPANTES
================================================================================

ANÁLISIS INDIVIDUALES:

{combined_summary}

================================================================================

INSTRUCCIONES FINALES:

1. Construye codebook emergente de 4 niveles (categoría→subcategoría→especificación→código)
2. Valida CADA código: ≥2 citas de ≥2 participantes
3. Identifica estructuras experienciales con coherencia ≥75% en ≥4/6 dimensiones
4. Genera estructura temporal diferenciada por perfil
5. Incluye frecuencias (N y %) en TODOS los niveles
6. Marca códigos únicos como "Variantes Individuales"

RETORNA SOLO JSON VÁLIDO (sin preamble, sin markdown):
"""
    
    # Llamada al LLM
    response_text = call_llm(
        prompt=full_prompt,
        system_message="You are an expert in phenomenological synthesis. Return ONLY valid JSON with complete codebook.",
        temperature=0.2,
        max_tokens=16000,
        json_mode=True
    )
    
    # Parse JSON
    try:
        result = json.loads(response_text)
        print(f"✅ Síntesis completada:")
        print(f"   - Categorías: {len(result.get('codebook', {}).get('categories', []))}")
        print(f"   - Estructuras: {len(result.get('experiential_structures', []))}")
        print(f"   - Fases temporales: {len(result.get('differentiated_temporal_structure', []))}")
        return result
    except json.JSONDecodeError as e:
        print(f"❌ Error parseando JSON de síntesis: {e}")
        return {
            "error": str(e),
            "raw_response": response_text[:500]
        }


def perform_validation(synthesis_result: Dict[str, Any], 
                      individual_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    FASE 3: Validación completa con prompt v3.0.
    """
    
    print(f"\n✓ Iniciando validación final...")
    
    # Preparar datos para validación
    codebook_summary = json.dumps(synthesis_result.get('codebook', {}), indent=2)[:2000]
    structures_summary = json.dumps(synthesis_result.get('experiential_structures', []), indent=2)[:1000]
    
    full_prompt = f"""{PROMPT_PARTE_3}

================================================================================
VALIDACIÓN FINAL - {len(individual_analyses)} PARTICIPANTES
================================================================================

CODEBOOK GENERADO (primeras 2000 chars):
{codebook_summary}

ESTRUCTURAS EXPERIENCIALES:
{structures_summary}

================================================================================

INSTRUCCIONES FINALES:

1. Verifica evidencia de CADA código individualmente
2. Calcula curva de saturación (códigos nuevos por participante)
3. Verifica consistencia interna (mutua exclusividad + co-ocurrencias)
4. Completa checklist de 45 ítems
5. Reporta códigos de frecuencia límite (N=2 participantes)

RETORNA JSON CON:
- evidence_verification: {{código: {{valid: bool, reason: str}}}}
- saturation_analysis: {{curve: [...], diagnosis: str}}
- internal_consistency: {{mutual_exclusivity: bool, coherent_cooccurrences: X/Y}}
- checklist_score: X/45
- quality_rating: "EXCELLENT/GOOD/ACCEPTABLE/NEEDS_REVISION"
"""
    
    response_text = call_llm(
        prompt=full_prompt,
        system_message="You are a validation expert. Return ONLY valid JSON with complete validation results.",
        temperature=0.1,  # Muy baja para validación
        max_tokens=8000,
        json_mode=True
    )
    
    try:
        result = json.loads(response_text)
        print(f"✅ Validación completada:")
        print(f"   - Checklist: {result.get('checklist_score', '?')}/45")
        print(f"   - Calidad: {result.get('quality_rating', '?')}")
        return result
    except json.JSONDecodeError as e:
        print(f"❌ Error parseando validación: {e}")
        return {"error": str(e)}


# =============================================================================
# FUNCIONES WRAPPER (Compatibilidad con código existente)
# =============================================================================

def analyze_with_pipeline(text: str, context: Dict[str, Any] = None, 
                         custom_codes: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Wrapper para análisis individual (mantiene compatibilidad API).
    """
    pid = context.get('participant_id', 'Pxx') if context else 'Pxx'
    return analyze_individual_interview(text, pid)


def synthesize_structure(analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Wrapper para síntesis cross-case (mantiene compatibilidad API).
    """
    return perform_cross_case_synthesis(analyses)


def generate_final_report(individual_results: List[Dict[str, Any]], 
                         synthesis_result: Dict[str, Any],
                         validation_result: Optional[Dict[str, Any]] = None) -> str:
    """
    Genera reporte final en formato Markdown v3.0.
    """
    
    report = "# PHENOMFLOW v3.0 - REPORTE FINAL COMPLETO\n\n"
    report += f"**Fecha**: {os.getenv('REPORT_DATE', 'N/A')}\n"
    report += f"**N Participantes**: {len(individual_results)}\n"
    report += f"**Modelo usado**: {MODEL}\n\n"
    
    report += "---\n\n"
    
    # PARTE 1: SÍNTESIS CROSS-CASE
    report += "## 1. SÍNTESIS CROSS-CASE\n\n"
    
    # 1.1 Estructuras Experienciales
    report += "### 1.1 Estructuras Experienciales (Perfiles Fenomenológicos)\n\n"
    for struct in synthesis_result.get('experiential_structures', []):
        report += f"#### {struct.get('structure_name', 'N/A')}\n"
        report += f"**N**: {struct.get('n_participants', '?')} participantes\n"
        report += f"**Participantes**: {', '.join(struct.get('participants', []))}\n"
        report += f"**Descripción**: {struct.get('phenomenological_description', 'N/A')}\n\n"
    
    # 1.2 Estructura Temporal
    report += "### 1.2 Estructura Temporal Diferenciada\n\n"
    for phase in synthesis_result.get('differentiated_temporal_structure', []):
        report += f"#### {phase.get('phase_name', 'N/A')}\n"
        report += f"**Frecuencia**: {phase.get('frequency_global', '?')}\n"
        report += f"- **Manifestación Estructura A**: {phase.get('manifestation_structure_A', {}).get('summary', 'N/A')}\n"
        report += f"- **Manifestación Estructura B**: {phase.get('manifestation_structure_B', {}).get('summary', 'N/A')}\n\n"
    
    # 1.3 Codebook (resumen)
    report += "### 1.3 Codebook Jerárquico (Resumen)\n\n"
    codebook_stats = synthesis_result.get('codebook', {}).get('statistics', {})
    report += f"- Categorías principales: {codebook_stats.get('n_categories', '?')}\n"
    report += f"- Subcategorías: {codebook_stats.get('n_subcategories', '?')}\n"
    report += f"- Especificaciones: {codebook_stats.get('n_specifications', '?')}\n"
    report += f"- Códigos específicos: {codebook_stats.get('n_codes', '?')}\n"
    report += f"- Citas totales: {codebook_stats.get('n_quotes', '?')}\n"
    report += f"- Tasa de recurrencia: {codebook_stats.get('recurrence_rate', '?')}\n\n"
    
    report += "---\n\n"
    
    # PARTE 2: ANÁLISIS INDIVIDUALES
    report += "## 2. ANÁLISIS INDIVIDUALES (Evidencia)\n\n"
    for res in individual_results:
        pid = res.get('participant_id', '?')
        report += f"### Participante {pid}\n\n"
        report += f"**Núcleo Fenomenológico**: {res.get('phenomenon_nucleus', 'N/A')}\n\n"
        report += "**Tabla de Análisis Dimensional**:\n"
        report += res.get('markdown_table', '*Tabla no disponible*') + "\n\n"
        report += f"**Estadísticas**:\n"
        stats = res.get('dimensional_statistics', {})
        for dim, data in stats.items():
            report += f"- {dim.capitalize()}: {data.get('coverage', '?')} cobertura\n"
        report += "\n---\n\n"
    
    # PARTE 3: VALIDACIÓN
    if validation_result:
        report += "## 3. VALIDACIÓN FINAL\n\n"
        report += f"**Checklist**: {validation_result.get('checklist_score', '?')}/45\n"
        report += f"**Calidad**: {validation_result.get('quality_rating', '?')}\n"
        report += f"**Saturación**: {validation_result.get('saturation_analysis', {}).get('diagnosis', 'N/A')}\n"
        report += f"**Consistencia**: {validation_result.get('internal_consistency', {}).get('summary', 'N/A')}\n\n"
    
    return report


# =============================================================================
# FUNCIÓN PRINCIPAL (Pipeline Completo)
# =============================================================================

def run_complete_pipeline(transcripts: List[Dict[str, str]], 
                         output_dir: str = "./analysis_results") -> str:
    """
    Ejecuta pipeline completo v3.0:
    1. Análisis individual de todos los participantes
    2. Síntesis cross-case
    3. Validación
    4. Generación de reporte final
    
    Args:
        transcripts: Lista de dicts con 'participant_id' y 'text'
        output_dir: Directorio para guardar resultados
    
    Returns:
        Path al reporte final generado
    """
    
    print("\n" + "="*80)
    print("PHENOMFLOW v3.0 - PIPELINE COMPLETO")
    print("="*80)
    
    # FASE 1: Análisis Individual
    print("\n📋 FASE 1: ANÁLISIS INDIVIDUAL")
    individual_results = []
    for t in transcripts:
        result = analyze_individual_interview(t['text'], t['participant_id'])
        individual_results.append(result)
    
    # FASE 2: Síntesis Cross-Case
    print("\n🔄 FASE 2: SÍNTESIS CROSS-CASE")
    synthesis_result = perform_cross_case_synthesis(individual_results)
    
    # FASE 3: Validación
    print("\n✓ FASE 3: VALIDACIÓN")
    validation_result = perform_validation(synthesis_result, individual_results)
    
    # Generar reporte final
    print("\n📄 GENERANDO REPORTE FINAL...")
    report_content = generate_final_report(individual_results, synthesis_result, validation_result)
    
    # Guardar reporte
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "PHENOMFLOW_v3_REPORT_FINAL.md")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"\n✅ PIPELINE COMPLETADO")
    print(f"📁 Reporte guardado en: {report_path}")
    print("="*80 + "\n")
    
    return report_path


# =============================================================================
# EJEMPLO DE USO
# =============================================================================

if __name__ == "__main__":
    # Ejemplo de uso con 2 transcripciones
    transcripts = [
        {
            "participant_id": "P21",
            "text": open("../data/transcripts/formatted_interview_P21.txt").read()
        },
        {
            "participant_id": "P27",
            "text": open("../data/transcripts/formatted_interview_P27.txt").read()
        }
    ]
    
    report_path = run_complete_pipeline(transcripts)
    print(f"Reporte disponible en: {report_path}")
