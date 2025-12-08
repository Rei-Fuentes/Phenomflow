"use client"

import { useState } from "react"
import { MagneticButton } from "@/components/magnetic-button"
import { useReveal } from "@/hooks/use-reveal"
import { MermaidDiagram } from "@/components/mermaid-diagram"
import { DimensionRadarChart } from "@/components/dimension-radar-chart"
import { BodyMap } from "@/components/body-map"
import { ResearchContextForm } from "@/components/research-context-form"

// ============================================================================
// TIPOS - Compatible con PhenomFlow v3.0
// ============================================================================

interface PhenomFlowAnalysis {
    codebook: {
        [category: string]: {
            [subcategory: string]: {
                [specification: string]: Array<{
                    code: string
                    participants: string[]
                    evidence: string[]
                    count: number
                }>
            }
        }
    }
    temporal_structures: {
        [pid: string]: {
            participant_id: string
            phases: Array<{
                phase_name: string
                temporal_segment: string
                description: string
                key_moments: string[]
            }>
            nuclear_metaphors: string[]
            inflection_points: string[]
        }
    }
    clustering: {
        structures: Array<{
            structure_id: number
            structure_name: string
            participants: string[]
            description: string
            shared_patterns: string[]
        }>
        dimensions: {
            [dimension: string]: {
                coverage_percentage: number
                dominant_codes: string[]
            }
        }
    }
    body_maps: {
        structures: Array<{
            structure_id: number
            structure_name: string
            participants: string[]
            zones: {
                [zone: string]: {
                    count: number
                    codes: Array<{
                        code: string
                        participant_id: string
                        frequency: number
                    }>
                    quotes: string[]
                }
            }
        }>
    }
    validation: {
        saturation: {
            achieved: boolean
            percentage: number
        }
        consistency_tests: {
            intercoder: { passed: boolean; score: number }
            intracoder: { passed: boolean; score: number }
        }
        checklist_score: number
    }
    metadata: {
        analysis_date: string
        model: string
        phenomflow_version: string
        context_used: boolean
        text_length: number
    }
}

export function EnhancedAnalysisSection() {
    const { ref, isVisible } = useReveal(0.3)
    const [inputText, setInputText] = useState("")
    const [result, setResult] = useState<PhenomFlowAnalysis | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const [loadingStage, setLoadingStage] = useState("")
    const [contextData, setContextData] = useState<any>(null)
    const [showContextForm, setShowContextForm] = useState(true)
    const [error, setError] = useState<string | null>(null)

    const handleContextSubmit = (data: any) => {
        setContextData(data)
        setShowContextForm(false)
    }

    const handleAnalyze = async () => {
        if (!inputText) {
            setError("Por favor ingresa texto para analizar")
            return
        }

        setIsLoading(true)
        setError(null)
        setResult(null)

        try {
            setLoadingStage("Enviando texto al backend...")

            const response = await fetch("http://localhost:8000/analyze/enhanced", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: inputText,
                    context: contextData
                }),
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.error || "Error en el servidor")
            }

            setLoadingStage("Procesando análisis fenomenológico...")
            const data = await response.json()

            setResult(data)
            setLoadingStage("")
        } catch (error: any) {
            console.error("Error analyzing text:", error)
            setError(error.message || "Error al analizar. Verifica que el backend esté corriendo en http://localhost:8000")
        } finally {
            setIsLoading(false)
        }
    }

    // ========================================================================
    // RENDERIZADORES POR SECCIÓN
    // ========================================================================

    const renderCodebook = () => {
        if (!result?.codebook) return null

        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-4 text-foreground">
                    📖 Codebook Jerárquico
                </h3>

                <div className="space-y-6">
                    {Object.entries(result.codebook).map(([category, subcategories]) => (
                        <div key={category} className="bg-foreground/5 p-4 rounded-lg border-l-4 border-[#e19136]">
                            <h4 className="font-mono text-sm font-semibold text-[#e19136] mb-3">
                                {category}
                            </h4>

                            <div className="space-y-3 pl-4">
                                {Object.entries(subcategories).map(([subcat, specs]) => (
                                    <div key={subcat}>
                                        <div className="text-xs font-mono text-foreground/70 mb-2">
                                            {subcat}
                                        </div>

                                        <div className="space-y-2 pl-4">
                                            {Object.entries(specs).map(([spec, codes]) => (
                                                <div key={spec} className="text-xs">
                                                    <div className="text-foreground/50 mb-1">{spec}</div>
                                                    {codes.slice(0, 3).map((code: any, i: number) => (
                                                        <div key={i} className="bg-background/30 p-2 rounded mb-1">
                                                            <code className="text-[#e19136] text-[10px]">
                                                                {code.code}
                                                            </code>
                                                            <span className="text-foreground/40 ml-2 text-[10px]">
                                                                ({code.count}x)
                                                            </span>
                                                        </div>
                                                    ))}
                                                    {codes.length > 3 && (
                                                        <div className="text-foreground/30 text-[10px] ml-2">
                                                            + {codes.length - 3} más
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        )
    }

    const renderTemporalStructures = () => {
        if (!result?.temporal_structures) return null

        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-4 text-foreground">
                    ⏱️ Estructuras Temporales
                </h3>

                <div className="space-y-6">
                    {Object.entries(result.temporal_structures).map(([pid, structure]) => (
                        <div key={pid} className="bg-foreground/5 p-6 rounded-lg">
                            <h4 className="font-mono text-lg text-[#e19136] mb-4">
                                {structure.participant_id}
                            </h4>

                            {/* Fases temporales */}
                            <div className="space-y-3 mb-4">
                                {structure.phases.map((phase, i) => (
                                    <div key={i} className="border-l-2 border-foreground/30 pl-4">
                                        <div className="font-mono text-sm text-foreground font-semibold">
                                            {phase.phase_name}
                                        </div>
                                        <div className="font-mono text-xs text-foreground/50">
                                            {phase.temporal_segment}
                                        </div>
                                        <div className="text-sm text-foreground/80 mt-1">
                                            {phase.description}
                                        </div>
                                        {phase.key_moments && phase.key_moments.length > 0 && (
                                            <div className="mt-2 text-xs text-foreground/60">
                                                🔑 {phase.key_moments.join(" · ")}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>

                            {/* Metáforas nucleares */}
                            {structure.nuclear_metaphors && structure.nuclear_metaphors.length > 0 && (
                                <div className="bg-background/30 p-3 rounded mt-4">
                                    <div className="text-xs font-mono text-foreground/60 mb-2">
                                        METÁFORAS NUCLEARES
                                    </div>
                                    {structure.nuclear_metaphors.map((metaphor, i) => (
                                        <div key={i} className="text-sm text-foreground/80 italic">
                                            "{metaphor}"
                                        </div>
                                    ))}
                                </div>
                            )}

                            {/* Puntos de inflexión */}
                            {structure.inflection_points && structure.inflection_points.length > 0 && (
                                <div className="bg-background/30 p-3 rounded mt-3">
                                    <div className="text-xs font-mono text-foreground/60 mb-2">
                                        PUNTOS DE INFLEXIÓN
                                    </div>
                                    {structure.inflection_points.map((point, i) => (
                                        <div key={i} className="text-sm text-foreground/80">
                                            • {point}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        )
    }

    const renderClustering = () => {
        if (!result?.clustering) return null

        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-4 text-foreground">
                    🔬 Clustering Estructural
                </h3>

                {/* Estructuras experienciales */}
                <div className="space-y-4 mb-6">
                    {result.clustering.structures.map((struct) => (
                        <div key={struct.structure_id} className="bg-foreground/5 p-5 rounded-lg border-l-4 border-[#e19136]">
                            <div className="flex justify-between items-start mb-2">
                                <h4 className="font-mono text-lg text-[#e19136]">
                                    Estructura {struct.structure_id}: {struct.structure_name}
                                </h4>
                                <span className="text-xs font-mono text-foreground/50">
                                    {struct.participants.join(", ")}
                                </span>
                            </div>
                            <p className="text-sm text-foreground/80 mb-3">
                                {struct.description}
                            </p>
                            {struct.shared_patterns && struct.shared_patterns.length > 0 && (
                                <div className="space-y-1">
                                    <div className="text-xs font-mono text-foreground/60">
                                        PATRONES COMPARTIDOS:
                                    </div>
                                    {struct.shared_patterns.map((pattern, i) => (
                                        <div key={i} className="text-xs text-foreground/70 pl-3">
                                            • {pattern}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>

                {/* Radar de dimensiones */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                        <h4 className="text-lg font-mono text-foreground/80 mb-4">
                            Cobertura por Dimensión
                        </h4>
                        <DimensionRadarChart data={result.clustering.dimensions} />
                    </div>

                    <div>
                        <h4 className="text-lg font-mono text-foreground/80 mb-4">
                            Códigos Dominantes
                        </h4>
                        <div className="space-y-3">
                            {Object.entries(result.clustering.dimensions).map(([dim, data]) => (
                                <div key={dim} className="bg-background/30 p-3 rounded">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className="font-mono text-sm text-foreground">
                                            {dim}
                                        </span>
                                        <span className="text-xs text-[#e19136] font-semibold">
                                            {data.coverage_percentage}%
                                        </span>
                                    </div>
                                    <div className="space-y-1">
                                        {data.dominant_codes.slice(0, 2).map((code, i) => (
                                            <div key={i} className="text-xs text-foreground/60 font-mono">
                                                • {code}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    const renderBodyMaps = () => {
        if (!result?.body_maps) return null

        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-6 text-foreground">
                    🧍 Body Maps Corporales
                </h3>
                <BodyMap data={result.body_maps} />
            </div>
        )
    }

    const renderValidation = () => {
        if (!result?.validation) return null

        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-4 text-foreground">
                    ✓ Validación Científica
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Saturación */}
                    <div className="bg-foreground/5 p-4 rounded-lg text-center">
                        <div className="text-3xl font-bold mb-2">
                            {result.validation.saturation.achieved ? "✓" : "○"}
                        </div>
                        <div className="text-sm font-mono text-foreground/80">
                            Saturación
                        </div>
                        <div className="text-xs text-foreground/50 mt-1">
                            {result.validation.saturation.percentage}%
                        </div>
                    </div>

                    {/* Consistencia Intercoder */}
                    <div className="bg-foreground/5 p-4 rounded-lg text-center">
                        <div className="text-3xl font-bold mb-2">
                            {result.validation.consistency_tests.intercoder.passed ? "✓" : "○"}
                        </div>
                        <div className="text-sm font-mono text-foreground/80">
                            Intercoder
                        </div>
                        <div className="text-xs text-foreground/50 mt-1">
                            {(result.validation.consistency_tests.intercoder.score * 100).toFixed(0)}%
                        </div>
                    </div>

                    {/* Checklist */}
                    <div className="bg-foreground/5 p-4 rounded-lg text-center">
                        <div className="text-3xl font-bold text-[#e19136] mb-2">
                            {result.validation.checklist_score}/45
                        </div>
                        <div className="text-sm font-mono text-foreground/80">
                            Checklist
                        </div>
                        <div className="text-xs text-foreground/50 mt-1">
                            {((result.validation.checklist_score / 45) * 100).toFixed(0)}%
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    // ========================================================================
    // RENDER PRINCIPAL
    // ========================================================================

    return (
        <section
            ref={ref}
            className="flex min-h-screen w-screen shrink-0 snap-start items-center px-4 pt-20 md:px-12 md:pt-0 lg:px-16"
        >
            <div className="mx-auto w-full max-w-7xl">
                <div
                    className={`mb-6 transition-all duration-700 md:mb-12 ${isVisible ? "translate-y-0 opacity-100" : "-translate-y-12 opacity-0"
                        }`}
                >
                    <h2 className="mb-3 font-sans text-3xl font-light leading-[1.1] tracking-tight text-foreground md:mb-4 md:text-6xl lg:text-7xl">
                        PhenomFlow
                        <br />
                        <span className="text-foreground/40">v3.0</span>
                    </h2>
                    <p className="text-sm font-mono text-foreground/50">
                        Análisis Fenomenológico con IA · Claude Sonnet 4.5
                    </p>
                </div>

                <div
                    className={`space-y-6 transition-all duration-700 ${isVisible ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
                        }`}
                    style={{ transitionDelay: "200ms" }}
                >
                    {/* FASE 0: Contexto de investigación */}
                    {showContextForm ? (
                        <ResearchContextForm onSubmit={handleContextSubmit} />
                    ) : (
                        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                            {/* Header con info del contexto */}
                            <div className="flex justify-between items-center mb-4 bg-foreground/5 p-3 rounded-lg">
                                <div className="flex items-center gap-3">
                                    <div className="text-xs font-mono text-foreground/60">
                                        {contextData ? (
                                            <span className="text-green-500">✓ Contexto configurado</span>
                                        ) : (
                                            <span className="text-yellow-500">⚠️ Sin contexto (precisión -40%)</span>
                                        )}
                                    </div>
                                    {contextData?.phenomenological_approach && (
                                        <div className="text-xs text-foreground/40">
                                            | {contextData.phenomenological_approach}
                                        </div>
                                    )}
                                </div>
                                <button
                                    onClick={() => setShowContextForm(true)}
                                    className="text-xs text-[#e19136] hover:underline"
                                >
                                    Editar Contexto
                                </button>
                            </div>

                            {/* Área de input de texto */}
                            <textarea
                                className="w-full h-64 p-4 bg-foreground/5 text-foreground border border-foreground/10 rounded-lg focus:outline-none focus:border-[#e19136]/50 resize-none font-mono text-sm"
                                placeholder="U1: Entrevistador: ¿Podrías describirme...&#10;U2: Participante: Sentí que...&#10;U3: ...&#10;&#10;(Pega aquí tu transcripción de entrevista)"
                                value={inputText}
                                onChange={(e) => setInputText(e.target.value)}
                            />

                            {/* Botón de análisis */}
                            <div className="flex gap-4 mt-4 items-center">
                                <MagneticButton
                                    size="lg"
                                    variant="primary"
                                    onClick={handleAnalyze}
                                    disabled={isLoading}
                                >
                                    {isLoading ? `⏳ ${loadingStage || "Analizando..."}` : "🚀 Analizar con PhenomFlow v3.0"}
                                </MagneticButton>

                                {isLoading && (
                                    <div className="text-xs font-mono text-foreground/50">
                                        ⚠️ Esto puede tardar 5-15 minutos
                                    </div>
                                )}
                            </div>

                            {/* Error message */}
                            {error && (
                                <div className="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-sm text-red-500">
                                    ❌ {error}
                                </div>
                            )}
                        </div>
                    )}

                    {/* RESULTADOS DEL ANÁLISIS */}
                    {result && !showContextForm && (
                        <div className="mt-8 space-y-12">
                            {/* Metadata */}
                            <div className="bg-foreground/5 p-4 rounded-lg border-l-4 border-green-500">
                                <div className="flex justify-between items-center">
                                    <div className="text-xs font-mono text-foreground/70">
                                        ✓ Análisis completado
                                    </div>
                                    <div className="text-xs font-mono text-foreground/50">
                                        {result.metadata.analysis_date} · {result.metadata.model}
                                    </div>
                                </div>
                            </div>

                            {renderCodebook()}
                            {renderTemporalStructures()}
                            {renderClustering()}
                            {renderBodyMaps()}
                            {renderValidation()}
                        </div>
                    )}
                </div>
            </div>
        </section>
    )
}