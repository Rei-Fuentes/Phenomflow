import json
import os
from typing import List, Dict, Any

# Mock Data for Individual Analysis (v3 Format)
def get_mock_individual_analysis(participant_id: str, profile_type: str) -> Dict[str, Any]:
    """
    Returns a mock v3 individual analysis result.
    """
    
    # Define profile characteristics
    if profile_type == "Structure A":
        nucleus = "Experiencia de apertura lúdica ante el vacío, caracterizada por expansión torácica y transformación del miedo en curiosidad."
        table_rows = [
            f"| U1 | \"Cuando vi el borde, sentí curiosidad.\" | `hormigueo-manos-leve-estatico` | `curiosidad-positiva-media` | `pregunta-exploratoria` | `impulso-acercamiento` | `fase-encuentro` | `atencion-world` |",
            f"| U2 | \"Mi pecho se abrió al respirar.\" | `expansion-pecho-alta-progresiva` | `anticipacion-placentera-alta` | [No men.] | `impulso-entrega` | `fase-umbral` | `atencion-self-corporal` |",
            f"| U3 | \"Soy un pájaro, volando libre.\" | `ligereza-total-muy-alta` | `extasis-maxima` | `metafora-vuelo` | `deseo-permanencia` | `fase-climax` | `atencion-no-dual` |"
        ]
    else: # Structure B
        nucleus = "Experiencia de colapso defensivo, caracterizada por contracción corporal, terror paralizante y repliegue atencional."
        table_rows = [
            f"| U1 | \"Sentí terror al ver abajo.\" | `tension-hombros-alta-estatica` | `terror-negativa-alta` | `catastrofismo-muerte` | `impulso-proteccion` | `fase-encuentro` | `atencion-self-sintoma` |",
            f"| U2 | \"Me congelé, no podía moverme.\" | `rigidez-piernas-muy-alta` | `panico-negativa-muy-alta` | `bloqueo-mental` | `paralisis-total` | `fase-umbral` | `atencion-self-miedo` |",
            f"| U3 | \"Sentí que iba a morir.\" | `nausea-abdominal-media` | `angustia-maxima` | `idea-muerte-inminente` | `impulso-huida` | `fase-climax` | `atencion-self-colapso` |"
        ]

    markdown_table = "| Unidad | Cita Verbatim | Corporal | Afectiva | Cognitiva | Motivacional | Temporal | Relacional |\n|---|---|---|---|---|---|---|---|\n" + "\n".join(table_rows)

    return {
        "participant_id": participant_id,
        "cleaned_text": f"Texto reorganizado de {participant_id}...",
        "phenomenon_nucleus": nucleus,
        "markdown_table": markdown_table,
        "analysis_summary": f"Patrón dominante de {profile_type}."
    }

# Mock Data for Synthesis (v3 Format)
def get_mock_synthesis() -> Dict[str, Any]:
    return {
        "codebook": {
            "main_categories": [
                {
                    "name": "Resonancia Corporal",
                    "subcategories": [
                        {
                            "name": "Expansión Torácica",
                            "frequency": "N=4 (57%)",
                            "examples": ["Mi pecho se abrió (P21)", "Sentí espacio (P23)"]
                        },
                        {
                            "name": "Contracción Defensiva",
                            "frequency": "N=3 (43%)",
                            "examples": ["Tensión hombros (P22)", "Rigidez (P24)"]
                        }
                    ]
                }
            ]
        },
        "experiential_structures": [
            {
                "structure_name": "Estructura A: Apertura Lúdica",
                "participants": ["P21", "P23", "P25", "P27"],
                "description": "Reencuadramiento del vacío como oportunidad de juego y expansión.",
                "characteristics": {
                    "corporal": "Expansión, ligereza",
                    "affective": "Curiosidad -> Éxtasis",
                    "motivational": "Acercamiento, Entrega"
                }
            },
            {
                "structure_name": "Estructura B: Colapso Defensivo",
                "participants": ["P22", "P24", "P26"],
                "description": "Vivencia del vacío como amenaza vital inminente.",
                "characteristics": {
                    "corporal": "Contracción, Peso",
                    "affective": "Terror -> Pánico",
                    "motivational": "Protección, Huida"
                }
            }
        ],
        "differentiated_temporal_structure": [
            {
                "phase_name": "Fase 1: Encuentro con el Borde",
                "manifestation_structure_A": "Curiosidad visual, activación corporal expansiva (preparación).",
                "manifestation_structure_B": "Terror visual, contracción corporal defensiva (retroceso)."
            },
            {
                "phase_name": "Fase 2: Clímax de la Caída",
                "manifestation_structure_A": "Éxtasis, sensación de vuelo, no-dualidad.",
                "manifestation_structure_B": "Vértigo, náusea, catastrofismo de muerte."
            }
        ],
        "synthesis_summary": "La experiencia se bifurca radicalmente en dos estructuras opuestas (Apertura vs Colapso)."
    }

def generate_report_v3(individual_results, synthesis_result):
    report = "# PHENOMFLOW v3.0 - FINAL REPORT\n\n"
    
    # 1. Synthesis Section
    report += "## 1. Cross-Case Synthesis\n\n"
    
    report += "### 1.1 Experiential Structures (Profiles)\n"
    for struct in synthesis_result["experiential_structures"]:
        report += f"#### {struct['structure_name']}\n"
        report += f"**Participants**: {', '.join(struct['participants'])}\n"
        report += f"**Description**: {struct['description']}\n"
        report += "**Characteristics**:\n"
        for k, v in struct["characteristics"].items():
            report += f"- **{k.capitalize()}**: {v}\n"
        report += "\n"

    report += "### 1.2 Differentiated Temporal Structure\n"
    for phase in synthesis_result["differentiated_temporal_structure"]:
        report += f"#### {phase['phase_name']}\n"
        report += f"- **Structure A**: {phase['manifestation_structure_A']}\n"
        report += f"- **Structure B**: {phase['manifestation_structure_B']}\n\n"

    report += "### 1.3 Hierarchical Codebook\n"
    for cat in synthesis_result["codebook"]["main_categories"]:
        report += f"#### Category: {cat['name']}\n"
        for sub in cat["subcategories"]:
            report += f"- **{sub['name']}** ({sub['frequency']}): {', '.join(sub['examples'])}\n"
    
    report += "\n---\n\n"
    
    # 2. Individual Analysis Section
    report += "## 2. Individual Analyses (Evidence)\n\n"
    for res in individual_results:
        report += f"### Participant {res['participant_id']}\n"
        report += f"**Phenomenon Nucleus**: {res['phenomenon_nucleus']}\n\n"
        report += "**Analysis Table**:\n"
        report += res["markdown_table"] + "\n\n"
        report += "---\n\n"

    return report

def main():
    # Simulate 7 participants
    participants = [
        ("P21", "Structure A"), ("P22", "Structure B"), ("P23", "Structure A"),
        ("P24", "Structure B"), ("P25", "Structure A"), ("P26", "Structure B"),
        ("P27", "Structure A")
    ]
    
    individual_results = []
    for pid, ptype in participants:
        individual_results.append(get_mock_individual_analysis(pid, ptype))
        
    synthesis_result = get_mock_synthesis()
    
    report_content = generate_report_v3(individual_results, synthesis_result)
    
    output_path = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/analysis_results/report_v3_final.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(report_content)
        
    print(f"Report generated at: {output_path}")

if __name__ == "__main__":
    main()
