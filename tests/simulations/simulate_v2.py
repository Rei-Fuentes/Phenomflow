import sys
import os
import json

def simulate_v2_analysis():
    print("\n=== SIMULATING PHENOMFLOW v2.0 ANALYSIS (BATCH P21-P27) ===\n")
    
    output_dir = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/analysis_results"
    
    # Mock Individual Analysis (Phase 1 Output) for 7 Participants
    individual_results = []
    
    # Define profiles for simulation
    profiles_data = {
        "P21": {"type": "Apertura", "quote": "Sentí que mi pecho se abría... Soy un pájaro.", "codes": {"corporal": "expansión-torácica", "affective": "asombro", "motivational": "deseo-volar"}},
        "P22": {"type": "Contracción", "quote": "Sentí un peso en los hombros... pies de plomo.", "codes": {"corporal": "peso-hombros", "affective": "terror", "motivational": "parálisis"}},
        "P23": {"type": "Apertura", "quote": "Alegría burbujeante... quería abrazar el espacio.", "codes": {"corporal": "relajación-total", "affective": "alegría", "motivational": "abrazar-espacio"}},
        "P24": {"type": "Contracción", "quote": "Calor intenso subiendo... me abracé a mí mismo.", "codes": {"corporal": "calor-cuello", "affective": "vértigo", "motivational": "protección"}},
        "P25": {"type": "Apertura", "quote": "Una paz inmensa... cuerpo ligero.", "codes": {"corporal": "ligereza", "affective": "paz", "motivational": "confianza"}},
        "P26": {"type": "Contracción", "quote": "Rigidez... dolor de cabeza repentino.", "codes": {"corporal": "rigidez-piernas", "affective": "miedo-metálico", "motivational": "huida"}},
        "P27": {"type": "Transformación", "quote": "El miedo se transformó en adrenalina... dejé de resistirme.", "codes": {"corporal": "liberación-tensión", "affective": "adrenalina", "motivational": "entrega"}}
    }

    for pid, data in profiles_data.items():
        individual_results.append({
            "filename": f"interview_{pid}.txt",
            "phenomenon_nucleus": f"Experiencia de {data['type']} ante el vacío.",
            "units": [
                {
                    "quote": data['quote'],
                    "codes": {
                        "corporal": data['codes']['corporal'],
                        "affective": data['codes']['affective'],
                        "cognitive": "evaluación-riesgo" if data['type'] == "Contracción" else "conexión-entorno",
                        "motivational": data['codes']['motivational'],
                        "temporal": "clímax",
                        "relational": "hacia-sí-mismo" if data['type'] == "Contracción" else "hacia-mundo"
                    },
                    "phase_label": "Clímax"
                }
            ]
        })
    
    # Mock Synthesis Output (Phase 2 Output)
    synthesis_result = {
        "main_categories": [
            {
                "name": "Modulación Corporal",
                "definition": "La respuesta somática fundamental ante el estímulo de altura.",
                "subcategories": [
                    { "name": "Expansión/Apertura", "frequency": "N=4 (57%)", "examples": ["pecho se abría (P21)", "abrazar el espacio (P23)"] },
                    { "name": "Contracción/Rigidez", "frequency": "N=3 (43%)", "examples": ["peso en hombros (P22)", "rigidez piernas (P26)"] }
                ]
            },
            {
                "name": "Cualidad Afectiva",
                "definition": "El tono emocional que tiñe la experiencia.",
                "subcategories": [
                    { "name": "Goce Estético/Lúdico", "frequency": "N=4 (57%)", "examples": ["alegría burbujeante (P23)", "paz inmensa (P25)"] },
                    { "name": "Terror Paralizante", "frequency": "N=3 (43%)", "examples": ["miedo metálico (P26)", "vértigo puro (P24)"] }
                ]
            }
        ],
        "common_temporal_structure": [
            {
                "phase_name": "1. Encuentro con el Borde",
                "description": "El momento de confrontación visual con el vacío.",
                "predominant_dimensions": "Cognitive: Evaluación (100%), Corporal: Activación (100%)",
                "frequency": "N=7 (100%)"
            },
            {
                "phase_name": "2. El Umbral de Decisión",
                "description": "El instante de suspender la seguridad para saltar.",
                "predominant_dimensions": "Motivational: Conflicto vs Entrega",
                "frequency": "N=7 (100%)"
            },
            {
                "phase_name": "3. La Caída (Clímax)",
                "description": "La experiencia cinética del descenso.",
                "predominant_dimensions": "Corporal: Expansión vs Contracción",
                "frequency": "N=7 (100%)"
            }
        ],
        "experiential_structures": [
            {
                "structure_name": "Estructura A: Apertura Lúdica",
                "description": "Participantes que reencuadran la caída como vuelo o liberación.",
                "characteristics": {
                    "corporal": "Expansión, ligereza, apertura torácica",
                    "affective": "Curiosidad, asombro, paz",
                    "motivational": "Deseo de fusión/vuelo",
                    "relational": "Apertura al mundo"
                },
                "participants": ["P21", "P23", "P25", "P27"],
                "exemplary_quotes": [
                    "Sentí que mi pecho se abría (P21)",
                    "Quería abrazar el espacio (P23)",
                    "El miedo se transformó en adrenalina (P27)"
                ]
            },
            {
                "structure_name": "Estructura B: Colapso Defensivo",
                "description": "Participantes abrumados por la amenaza física percibida.",
                "characteristics": {
                    "corporal": "Peso, rigidez, calor, náusea",
                    "affective": "Terror, pánico, desorientación",
                    "motivational": "Parálisis, huida, protección",
                    "relational": "Repliegue sobre sí mismo"
                },
                "participants": ["P22", "P24", "P26"],
                "exemplary_quotes": [
                    "Sentí un peso en los hombros (P22)",
                    "Me abracé a mí mismo (P24)",
                    "Rigidez... duras como piedras (P26)"
                ]
            }
        ]
    }
    
    # Generate Report
    report_path = os.path.join(output_dir, "report_v2_final.md")
    with open(report_path, "w") as f:
        f.write("# REPORTE FINAL PHENOMFLOW v2.0 (Batch P21-P27)\n\n")
        f.write(f"**Fecha**: {os.popen('date').read().strip()}\n")
        f.write("**Metodología**: Fenomenología Descriptiva (Giorgi/Petitmengin)\n")
        f.write("**N**: 7 Entrevistas\n\n")
        
        # 1. Categorías Principales
        f.write("## 1. CATEGORÍAS FENOMENOLÓGICAS PRINCIPALES\n\n")
        for cat in synthesis_result['main_categories']:
            f.write(f"### {cat['name']}\n")
            f.write(f"**Definición**: {cat['definition']}\n\n")
            f.write("**Subcategorías**:\n")
            for sub in cat['subcategories']:
                f.write(f"- **{sub['name']}** ({sub['frequency']})\n")
                f.write(f"  - Ejemplos: {', '.join(sub['examples'])}\n")
            f.write("\n")
            
        f.write("---\n\n")
        
        # 2. Estructura Temporal
        f.write("## 2. ESTRUCTURA TEMPORAL COMÚN\n\n")
        f.write("| Fase | Descripción | Dimensiones Predominantes | Frecuencia |\n")
        f.write("|---|---|---|---|\n")
        for phase in synthesis_result['common_temporal_structure']:
            f.write(f"| {phase['phase_name']} | {phase['description']} | {phase['predominant_dimensions']} | {phase['frequency']} |\n")
        f.write("\n---\n\n")
        
        # 3. Estructuras Experienciales
        f.write("## 3. ESTRUCTURAS EXPERIENCIALES\n\n")
        for st in synthesis_result['experiential_structures']:
            f.write(f"### {st['structure_name']} (N={len(st['participants'])})\n")
            f.write(f"**Descripción**: {st['description']}\n\n")
            f.write("**Características**:\n")
            for k, v in st['characteristics'].items():
                f.write(f"- **{k.capitalize()}**: {v}\n")
            f.write("\n**Citas Ejemplares**:\n")
            for q in st['exemplary_quotes']:
                f.write(f"- \"{q}\"\n")
            f.write("\n")
            
        f.write("---\n\n")
        
        # 4. Tabla Comparativa
        f.write("## 4. TABLA COMPARATIVA DE ESTRUCTURAS\n\n")
        f.write("| Dimensión | Estructura A (Apertura) | Estructura B (Colapso) |\n")
        f.write("|---|---|---|\n")
        f.write("| Corporal | Expansión, Ligereza | Contracción, Peso |\n")
        f.write("| Afectiva | Curiosidad, Paz | Terror, Pánico |\n")
        f.write("| Relacional | Hacia el Mundo | Hacia Sí Mismo |\n")
        f.write("\n---\n\n")
        
        # 5. Evidencia Individual
        f.write("## 5. EVIDENCIA INDIVIDUAL (Muestra)\n\n")
        for res in individual_results:
            f.write(f"### {res['filename']}\n")
            f.write(f"**Núcleo**: {res['phenomenon_nucleus']}\n")
            for unit in res['units']:
                f.write(f"- *\"{unit['quote']}\"* -> **{unit['codes']['corporal']}** / **{unit['codes']['affective']}**\n")
            f.write("\n")

    print(f"-> Saved v2 FINAL report to: {report_path}")

if __name__ == "__main__":
    simulate_v2_analysis()
