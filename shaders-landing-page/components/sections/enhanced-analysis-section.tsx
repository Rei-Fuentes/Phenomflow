"use client"

import { useState } from "react"
import { MagneticButton } from "@/components/magnetic-button"
import { useReveal } from "@/hooks/use-reveal"
import { MermaidDiagram } from "@/components/mermaid-diagram"
import { DimensionRadarChart } from "@/components/dimension-radar-chart"
import { BodyMap } from "@/components/body-map"
import { ResearchContextForm } from "@/components/research-context-form"

export function EnhancedAnalysisSection() {
    const { ref, isVisible } = useReveal(0.3)
    const [inputText, setInputText] = useState("")
    const [result, setResult] = useState<any>(null)
    const [isLoading, setIsLoading] = useState(false)
    const [contextData, setContextData] = useState<any>(null)
    const [showContextForm, setShowContextForm] = useState(true)

    const handleContextSubmit = (data: any) => {
        setContextData(data)
        setShowContextForm(false)
    }

    const handleAnalyze = async () => {
        if (!inputText) return
        setIsLoading(true)
        try {
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
            const data = await response.json()
            setResult(data)
        } catch (error) {
            console.error("Error analyzing text:", error)
            setResult({ error: "Error occurred during analysis." })
        } finally {
            setIsLoading(false)
        }
    }

    const renderPhase1 = () => {
        if (!result?.phase1_codes?.codes) return null
        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-4 text-foreground">Phase 1: Open Coding</h3>
                <div className="overflow-x-auto">
                    <table className="w-full border-collapse">
                        <thead>
                            <tr className="border-b border-foreground/20">
                                <th className="text-left p-2 font-mono text-sm">Dimension</th>
                                <th className="text-left p-2 font-mono text-sm">Category</th>
                                <th className="text-left p-2 font-mono text-sm">Verbatim</th>
                            </tr>
                        </thead>
                        <tbody>
                            {result.phase1_codes.codes.map((code: any, i: number) => (
                                <tr key={i} className="border-b border-foreground/10">
                                    <td className="p-2 font-mono text-xs text-foreground/80">{code.dimension}</td>
                                    <td className="p-2 font-mono text-xs text-foreground/80">{code.category}</td>
                                    <td className="p-2 font-mono text-xs text-foreground/60 italic">&quot;{code.verbatim}&quot;</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }

    const renderPhase2 = () => {
        if (!result?.phase2_diachronic?.phases) return null
        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-4 text-foreground">Phase 2: Diachronic Structure</h3>
                <div className="space-y-4">
                    {result.phase2_diachronic.phases.map((phase: any, i: number) => (
                        <div key={i} className="border-l-2 border-foreground/30 pl-4">
                            <div className="font-mono text-sm text-foreground">{phase.phase_name}</div>
                            <div className="font-mono text-xs text-foreground/60">{phase.temporal_segment}</div>
                            <div className="text-sm text-foreground/80 mt-1">{phase.description}</div>
                        </div>
                    ))}
                </div>
            </div>
        )
    }

    const renderPhase3 = () => {
        if (!result?.phase3_synchronic?.synchronic_configurations) return null

        const allDimensions = new Set<string>()
        result.phase3_synchronic.synchronic_configurations.forEach((config: any) => {
            Object.keys(config.active_dimensions || {}).forEach(dim => allDimensions.add(dim))
        })

        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-4 text-foreground">Phase 3: Synchronic Structure (Heatmap & Radar)</h3>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-6">
                    <div className="col-span-1">
                        <DimensionRadarChart data={result.phase3_synchronic.synchronic_configurations} />
                    </div>
                    <div className="col-span-1">
                        <BodyMap codes={result.phase1_codes.codes} />
                    </div>

                    <div className="col-span-1 md:col-span-2 lg:col-span-1 overflow-x-auto">
                        <table className="w-full border-collapse">
                            <thead>
                                <tr className="border-b border-foreground/20">
                                    <th className="text-left p-2 font-mono text-sm">Phase</th>
                                    {Array.from(allDimensions).map(dim => (
                                        <th key={dim} className="text-left p-2 font-mono text-xs">{dim}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {result.phase3_synchronic.synchronic_configurations.map((config: any, i: number) => (
                                    <tr key={i} className="border-b border-foreground/10">
                                        <td className="p-2 font-mono text-xs text-foreground">{config.phase_name}</td>
                                        {Array.from(allDimensions).map(dim => {
                                            const intensity = config.active_dimensions?.[dim]?.intensity || 0
                                            const opacity = intensity / 10
                                            return (
                                                <td key={dim} className="p-2">
                                                    <div
                                                        className="h-8 flex items-center justify-center font-mono text-xs"
                                                        style={{
                                                            backgroundColor: `rgba(225, 145, 54, ${opacity})`,
                                                            color: opacity > 0.5 ? '#000' : '#fff'
                                                        }}
                                                    >
                                                        {intensity > 0 ? intensity : '-'}
                                                    </div>
                                                </td>
                                            )
                                        })}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        )
    }

    const renderPhase4 = () => {
        if (!result?.phase4_invariants?.invariants) return null
        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-4 text-foreground">Phase 4: Invariants</h3>
                <div className="space-y-3">
                    {result.phase4_invariants.invariants.map((inv: any, i: number) => (
                        <div key={i} className="bg-foreground/5 p-4 rounded-lg">
                            <div className="font-mono text-sm text-foreground mb-1">{inv.name}</div>
                            <div className="text-sm text-foreground/70">{inv.description}</div>
                        </div>
                    ))}
                </div>
            </div>
        )
    }

    const renderPhase5 = () => {
        if (!result?.phase5_visualizations?.mermaid_diagram) return null
        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-4 text-foreground">Phase 5: Flow Diagram</h3>
                <MermaidDiagram chart={result.phase5_visualizations.mermaid_diagram} />
            </div>
        )
    }

    const renderPhase6 = () => {
        if (!result?.phase6_integration?.interpretative_text) return null
        return (
            <div className="mb-8">
                <h3 className="text-2xl font-light mb-4 text-foreground">Phase 6: Interpretative Integration</h3>
                <div className="prose prose-invert max-w-none bg-foreground/5 p-6 rounded-lg">
                    <div className="whitespace-pre-wrap font-sans text-sm text-foreground/90 leading-relaxed">
                        {result.phase6_integration.interpretative_text}
                    </div>
                </div>
            </div>
        )
    }

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
                        Enhanced
                        <br />
                        <span className="text-foreground/40">Analysis</span>
                    </h2>
                </div>

                <div
                    className={`space-y-6 transition-all duration-700 ${isVisible ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
                        }`}
                    style={{ transitionDelay: "200ms" }}
                >
                    {showContextForm ? (
                        <ResearchContextForm onSubmit={handleContextSubmit} />
                    ) : (
                        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <div className="flex justify-between items-center mb-4">
                                <div className="text-xs font-mono text-foreground/40">
                                    {contextData ? "✅ Context Configured" : "⚠️ No Context"}
                                </div>
                                <button
                                    onClick={() => setShowContextForm(true)}
                                    className="text-xs text-foreground/60 hover:text-foreground underline"
                                >
                                    Edit Context
                                </button>
                            </div>

                            <textarea
                                className="w-full h-48 p-4 bg-foreground/5 text-foreground border border-foreground/10 rounded-lg focus:outline-none focus:border-foreground/30 resize-none font-mono text-sm"
                                placeholder="Paste interview text here..."
                                value={inputText}
                                onChange={(e) => setInputText(e.target.value)}
                            />

                            <div className="flex gap-4 mt-4">
                                <MagneticButton size="lg" variant="primary" onClick={handleAnalyze}>
                                    {isLoading ? "Analyzing..." : "Analyze (5-Phase Pipeline)"}
                                </MagneticButton>
                            </div>
                        </div>
                    )}

                    {result && !result.error && !showContextForm && (
                        <div className="mt-8 space-y-8">
                            {renderPhase1()}
                            {renderPhase2()}
                            {renderPhase3()}
                            {renderPhase4()}
                            {renderPhase5()}
                            {renderPhase6()}
                        </div>
                    )}

                    {result?.error && (
                        <div className="text-red-500 font-mono text-sm">{result.error}</div>
                    )}
                </div>
            </div>
        </section>
    )
}
