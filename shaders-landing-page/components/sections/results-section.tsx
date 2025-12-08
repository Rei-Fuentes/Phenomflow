"use client"

import { useState } from "react"
import { useReveal } from "@/hooks/use-reveal"
import { MermaidDiagram } from "@/components/mermaid-diagram"
import { DimensionRadarChart } from "@/components/dimension-radar-chart"
import { BodyMap } from "@/components/body-map"
import { Table, Activity, FileText } from "lucide-react"

interface ResultsSectionProps {
    result: any
    t: any
}

export function ResultsSection({ result, t }: ResultsSectionProps) {
    const { ref, isVisible } = useReveal(0.3)
    const [activeTab, setActiveTab] = useState<"codes" | "visuals" | "synthesis">("codes")

    const renderTabs = () => (
        <div className="flex justify-center mb-12">
            <div className="flex bg-foreground/5 p-1 rounded-full backdrop-blur-sm border border-foreground/10">
                <button
                    onClick={() => setActiveTab("codes")}
                    className={`flex items-center gap-2 px-6 py-2 rounded-full text-sm font-medium transition-all duration-300 ${activeTab === "codes"
                        ? "bg-[#e19136] text-white shadow-lg"
                        : "text-foreground/60 hover:text-foreground hover:bg-foreground/5"
                        }`}
                >
                    <Table className="w-4 h-4" />
                    Detailed Codes
                </button>
                <button
                    onClick={() => setActiveTab("visuals")}
                    className={`flex items-center gap-2 px-6 py-2 rounded-full text-sm font-medium transition-all duration-300 ${activeTab === "visuals"
                        ? "bg-[#e19136] text-white shadow-lg"
                        : "text-foreground/60 hover:text-foreground hover:bg-foreground/5"
                        }`}
                >
                    <Activity className="w-4 h-4" />
                    Visual Analysis
                </button>
                <button
                    onClick={() => setActiveTab("synthesis")}
                    className={`flex items-center gap-2 px-6 py-2 rounded-full text-sm font-medium transition-all duration-300 ${activeTab === "synthesis"
                        ? "bg-[#e19136] text-white shadow-lg"
                        : "text-foreground/60 hover:text-foreground hover:bg-foreground/5"
                        }`}
                >
                    <FileText className="w-4 h-4" />
                    Synthesis
                </button>
            </div>
        </div>
    )

    const renderCodesTab = () => {
        if (!result?.phase1_codes?.codes) return null
        return (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                <h3 className="text-2xl font-light mb-6 text-foreground">Detailed Phenomenological Codes</h3>
                <div className="overflow-x-auto bg-foreground/5 rounded-lg border border-foreground/10">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="border-b border-foreground/10 bg-foreground/5">
                                <th className="p-4 font-mono text-xs text-foreground/60 uppercase tracking-wider">Dimension</th>
                                <th className="p-4 font-mono text-xs text-foreground/60 uppercase tracking-wider">Category</th>
                                <th className="p-4 font-mono text-xs text-foreground/60 uppercase tracking-wider">Code</th>
                                <th className="p-4 font-mono text-xs text-foreground/60 uppercase tracking-wider">Verbatim Evidence</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-foreground/5">
                            {result.phase1_codes.codes.map((code: any, i: number) => (
                                <tr key={i} className="hover:bg-foreground/5 transition-colors">
                                    <td className="p-4">
                                        <span className="inline-block px-2 py-1 rounded text-xs font-medium bg-[#e19136]/10 text-[#e19136]">
                                            {code.dimension}
                                        </span>
                                    </td>
                                    <td className="p-4 text-sm text-foreground/80">{code.category}</td>
                                    <td className="p-4 text-sm font-medium text-foreground">{code.sub_category || code.code || "-"}</td>
                                    <td className="p-4 text-sm text-foreground/60 italic max-w-md">"{code.verbatim}"</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }

    const renderVisualsTab = () => {
        if (!result?.phase3_synchronic) return null
        return (
            <div className="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-500">

                {/* Body Map Section */}
                <div>
                    <h3 className="text-2xl font-light mb-6 text-foreground">Corporeal Resonance</h3>
                    <BodyMap data={result.phase3_synchronic.body_map_data} />
                </div>

                {/* Radar Chart Section */}
                <div>
                    <h3 className="text-2xl font-light mb-6 text-foreground">Dimensional Configuration</h3>
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div className="lg:col-span-1">
                            <DimensionRadarChart data={result.phase3_synchronic.synchronic_configurations} />
                        </div>
                        <div className="lg:col-span-2 bg-foreground/5 rounded-lg p-6">
                            <h4 className="text-sm font-mono text-foreground/60 mb-4">Phase Intensity Heatmap</h4>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="border-b border-foreground/10">
                                            <th className="text-left p-2 font-mono text-xs text-foreground/50">Phase</th>
                                            {Object.keys(result.phase3_synchronic.synchronic_configurations[0]?.active_dimensions || {}).map(dim => (
                                                <th key={dim} className="text-left p-2 font-mono text-xs text-foreground/50">{dim}</th>
                                            ))}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {result.phase3_synchronic.synchronic_configurations.map((config: any, i: number) => (
                                            <tr key={i} className="border-b border-foreground/5">
                                                <td className="p-2 font-mono text-xs text-foreground">{config.phase_name}</td>
                                                {Object.keys(config.active_dimensions || {}).map(dim => {
                                                    const intensity = config.active_dimensions[dim]?.intensity || 0
                                                    return (
                                                        <td key={dim} className="p-2">
                                                            <div
                                                                className="h-6 w-full rounded flex items-center justify-center text-[10px] font-bold transition-all"
                                                                style={{
                                                                    backgroundColor: `rgba(225, 145, 54, ${intensity / 10})`,
                                                                    color: intensity > 5 ? 'white' : 'rgba(255,255,255,0.5)'
                                                                }}
                                                            >
                                                                {intensity}
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
                </div>
            </div>
        )
    }

    const renderSynthesisTab = () => {
        return (
            <div className="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
                {/* Diachronic Structure */}
                {result?.phase2_diachronic?.phases && (
                    <div>
                        <h3 className="text-2xl font-light mb-6 text-foreground">Diachronic Structure (Timeline)</h3>
                        <div className="relative border-l-2 border-[#e19136]/30 ml-4 space-y-8 py-2">
                            {result.phase2_diachronic.phases.map((phase: any, i: number) => (
                                <div key={i} className="relative pl-8 group">
                                    <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-[#e19136] border-4 border-background transition-transform group-hover:scale-125" />
                                    <div className="bg-foreground/5 p-6 rounded-lg border border-foreground/10 hover:border-[#e19136]/30 transition-colors">
                                        <div className="flex justify-between items-start mb-2">
                                            <h4 className="text-lg font-medium text-foreground">{phase.phase_name}</h4>
                                            <span className="text-xs font-mono text-foreground/40">{phase.temporal_segment}</span>
                                        </div>
                                        <p className="text-sm text-foreground/80 mb-4 leading-relaxed">{phase.description}</p>
                                        <div className="flex flex-wrap gap-2">
                                            {phase.dominant_codes.map((code: string, j: number) => (
                                                <span key={j} className="text-xs font-mono bg-foreground/10 px-2 py-1 rounded text-foreground/60">
                                                    {code}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Flow Diagram */}
                {result?.phase5_visualizations?.mermaid_diagram && (
                    <div>
                        <h3 className="text-2xl font-light mb-6 text-foreground">Experiential Flow</h3>
                        <div className="bg-white/5 p-4 rounded-lg">
                            <MermaidDiagram chart={result.phase5_visualizations.mermaid_diagram} />
                        </div>
                    </div>
                )}

                {/* Invariants */}
                {result?.phase4_invariants?.invariants && (
                    <div>
                        <h3 className="text-2xl font-light mb-6 text-foreground">Structural Invariants</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {result.phase4_invariants.invariants.map((inv: any, i: number) => (
                                <div key={i} className="bg-foreground/5 p-6 rounded-lg border-l-4 border-[#e19136]">
                                    <h4 className="text-lg font-medium text-foreground mb-2">{inv.name || inv.invariant_name}</h4>
                                    <p className="text-sm text-foreground/80 mb-4">{inv.description}</p>
                                    <div className="bg-black/20 p-3 rounded text-xs font-mono text-foreground/60 italic">
                                        "{inv.evidence}"
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Integration Text */}
                {result?.phase6_integration?.interpretative_text && (
                    <div>
                        <h3 className="text-2xl font-light mb-6 text-foreground">Interpretative Integration</h3>
                        <div className="prose prose-invert max-w-none bg-foreground/5 p-8 rounded-lg border border-foreground/10">
                            <div className="whitespace-pre-wrap font-sans text-sm text-foreground/90 leading-relaxed">
                                {result.phase6_integration.interpretative_text}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        )
    }

    return (
        <section
            ref={ref}
            className="flex min-h-screen w-screen shrink-0 flex-col justify-start px-6 md:px-12 pt-24 overflow-y-auto"
        >
            <div className="max-w-7xl mx-auto w-full pb-24">
                <h2 className={`mb-8 text-4xl font-light text-foreground transition-all duration-700 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
                    {t.nav.results}
                </h2>

                {!result ? (
                    <div className="flex flex-col items-center justify-center h-96 border border-dashed border-foreground/20 rounded-xl bg-foreground/5">
                        <Activity className="w-12 h-12 text-foreground/20 mb-4" />
                        <p className="text-foreground/40 text-lg font-light">Waiting for analysis...</p>
                        <p className="text-foreground/30 text-sm mt-2">Upload materials and click Analyze to see results.</p>
                    </div>
                ) : (
                    <div className={`transition-all duration-700 delay-200 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
                        {renderTabs()}

                        <div className="min-h-[600px]">
                            {activeTab === "codes" && renderCodesTab()}
                            {activeTab === "visuals" && renderVisualsTab()}
                            {activeTab === "synthesis" && renderSynthesisTab()}
                        </div>
                    </div>
                )}
            </div>
        </section>
    )
}
