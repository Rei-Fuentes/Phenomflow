# PhenomFlow Frontend

Interfaz web con Next.js 15 y WebGL shaders para análisis fenomenológico.

## Estructura

```
frontend/
├── app/                 # Pages y layouts
│   ├── page.tsx         # Página principal
│   └── layout.tsx       # Layout global
├── components/          # Componentes React
│   ├── sections/        # Secciones de la landing
│   │   ├── results-section.tsx
│   │   ├── context-section.tsx
│   │   └── materials-section.tsx
│   ├── body-map.tsx     # Visualización corporal
│   ├── dimension-radar-chart.tsx
│   └── research-context-form.tsx
├── hooks/               # Custom hooks
├── lib/                 # Utilidades
└── public/              # Assets estáticos
```

## Instalación

```bash
npm install --legacy-peer-deps
```

## Desarrollo

```bash
npm run dev
```

Aplicación disponible en `http://localhost:3000`

## Build

```bash
npm run build
npm start
```

## Características

### Shaders WebGL
Efectos visuales con `shaders/react`:
- **Swirl**: Remolinos de color
- **ChromaFlow**: Flujo cromático interactivo

### Componentes Principales

#### `ResultsSection`
Visualización de resultados con tabs:
- Codebook jerárquico
- Estructuras temporales
- Clustering experiencial
- Body maps corporales
- Validación científica

#### `BodyMap`
Mapa corporal interactivo:
- Hover para ver menciones
- Click para ver citas
- Zonas: head, chest, solar_plexus, abdomen, pelvis, extremities

#### `DimensionRadarChart`
Radar de cobertura dimensional:
- 6 dimensiones fenomenológicas
- Porcentajes de cobertura
- Códigos dominantes

#### `ResearchContextForm`
Formulario de contexto de investigación:
- Pregunta de investigación
- Objetivo del estudio
- Enfoque fenomenológico
- Contexto de participantes
- Tipo de entrevista
- Momento de la entrevista

### Integración con Backend

```typescript
// Endpoint principal
const response = await fetch("http://localhost:8000/analyze/enhanced", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    text: inputText,
    context: contextData
  })
})
```

## Estilos

- **Framework**: TailwindCSS
- **Colores**: `#e19136` (naranja), `#1275d8` (azul)
- **Efectos**: Glassmorphism, blur, gradientes
- **Tipografía**: Sans-serif (títulos), Mono (código)

## Configuración

### Cambiar Puerto del Backend

Editar en `components/sections/enhanced-analysis-section.tsx`:

```typescript
const response = await fetch("http://localhost:8000/analyze/enhanced", ...)
//                                        ^^^^
//                                        Cambiar puerto aquí
```

### Personalizar Colores

Editar en `app/page.tsx`:

```tsx
<Swirl
  colorA="#1275d8"  // Azul
  colorB="#e19136"  // Naranja
  ...
/>
```

## Troubleshooting

### Error: Cannot find module 'shaders/react'
```bash
npm install --legacy-peer-deps
```

### Error: CORS
Verificar que el backend tenga CORS habilitado para `*` o `http://localhost:3000`.

### Shader no se muestra
Verificar que WebGL esté habilitado en el navegador.
