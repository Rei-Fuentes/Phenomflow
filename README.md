# PhenomFlow v3.0

**Análisis Fenomenológico con IA** - Sistema de análisis cualitativo basado en Claude Sonnet 4 siguiendo la metodología de Giorgi y Petitmengin.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)

---

## 🎯 Características

- **Análisis Fenomenológico v3.0**: Implementación rigurosa de metodología Giorgi con 6 dimensiones obligatorias
- **IA Avanzada**: Claude Sonnet 4 con prompts de 1500+ líneas para máxima precisión
- **Codebook Jerárquico**: 4 niveles de granularidad con validación automática
- **Clustering Experiencial**: Identificación de estructuras fenomenológicas compartidas
- **Body Maps**: Visualización de resonancias corporales por zona anatómica
- **Validación Científica**: Saturación temática, consistencia interna, checklist de 45 ítems
- **UI Premium**: Interfaz con shaders WebGL y efectos glassmorphism

---

## 📁 Estructura del Proyecto

```
PhenomFlow/
├── backend/              # Flask API + Lógica de análisis
│   ├── service.py        # API principal (Flask)
│   ├── prompts/          # Prompts v3.0 (Parte 1, 2, 3)
│   └── requirements.txt
│
├── frontend/             # Next.js + WebGL Shaders
│   ├── app/              # Pages y layouts
│   ├── components/       # Componentes React
│   └── package.json
│
├── data/                 # Datos de investigación
│   └── simulated_interviews/
│
├── tests/                # Tests organizados
│   ├── unit/             # Tests unitarios
│   ├── integration/      # Tests de integración
│   ├── debug/            # Scripts de debugging
│   └── simulations/      # Simulaciones v2/v3
│
├── scripts/              # Utilidades
│   ├── extract_pdf.py
│   └── parse_notebook.py
│
├── notebooks/            # Jupyter notebooks
│   └── Proyecto_Data_Engineering_vlc.ipynb
│
├── docs/                 # Documentación
│   ├── API.md
│   └── ARCHITECTURE.md
│
└── paper reference/      # Referencias académicas
```

---

## 🚀 Quick Start

### Prerrequisitos

- Python 3.11+
- Node.js 18+
- API Key de Anthropic

### 1. Configurar Variables de Entorno

```bash
cp .env.example .env
# Editar .env y agregar tu ANTHROPIC_API_KEY
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
python3 service.py
```

El servidor estará disponible en `http://localhost:8000`

### 3. Frontend

```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`

---

## 🔧 Configuración

### Variables de Entorno

```env
# API Keys
ANTHROPIC_API_KEY=sk-ant-api03-...
USE_CLAUDE=true

# Opcional
PORT=8000
```

### Modelo de IA

Por defecto usa `claude-sonnet-4-20250514`. Para cambiar el modelo, edita `backend/service.py`:

```python
MODEL = "claude-sonnet-4-20250514"  # Cambiar aquí
```

---

## 📖 Uso

### 1. Configurar Contexto de Investigación

En la interfaz web, completa el formulario de contexto:
- Pregunta de investigación
- Objetivo del estudio
- Enfoque fenomenológico (Giorgi, Petitmengin, etc.)
- Contexto de participantes
- Tipo de entrevista
- Momento de la entrevista

### 2. Cargar Transcripción

Pega tu transcripción en el formato:

```
U1: Entrevistador: ¿Podrías describirme...?
U2: Participante: Sentí que...
U3: Participante: Y luego...
```

### 3. Analizar

Haz clic en "Analizar con PhenomFlow v3.0" y espera 5-15 minutos.

### 4. Explorar Resultados

- **Codebook**: Códigos jerárquicos emergentes
- **Estructuras Temporales**: Fases fenomenológicas
- **Clustering**: Estructuras experienciales compartidas
- **Body Maps**: Resonancias corporales
- **Validación**: Métricas de calidad científica

---

## 🧪 Testing

```bash
# Tests unitarios
python3 tests/unit/test_body_map.py

# Simulaciones
python3 tests/simulations/simulate_v3.py

# Debug de Anthropic
python3 tests/debug/debug_anthropic.py
```

---

## 📚 Documentación

- [API Documentation](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Contributing](docs/CONTRIBUTING.md)

---

## 🎨 Tecnologías

### Backend
- **Flask** - API REST
- **Anthropic Claude** - Análisis fenomenológico
- **SQLAlchemy** - ORM
- **Pydantic** - Validación de datos

### Frontend
- **Next.js 15** - Framework React
- **WebGL Shaders** - Efectos visuales
- **Recharts** - Visualizaciones
- **TailwindCSS** - Estilos

---

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

---

## 🙏 Referencias

- Giorgi, A. (2009). *The Descriptive Phenomenological Method in Psychology*
- Petitmengin, C. (2006). *Describing one's subjective experience in the second person*
- Varela, F. J. (1996). *Neurophenomenology: A methodological remedy*

---

## 👥 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📧 Contacto: reinerfuentes7@gmail.com

Proyecto: [https://github.com/Rei-Fuentes/PhenomFlow](https://github.com/Rei-Fuentes/PhenomFlow)

---

**Desarrollado por Reiner Fuentes Ferrada
para la investigación fenomenológica**
