"use client"

import React, { useState } from "react"
import { X } from "lucide-react"

// ============================================================================
// TIPOS - Compatible con backend PhenomFlow v3.0
// ============================================================================

interface CodeReference {
    code: string              // "opresion-pecho-intensa-negativa"
    participant_id: string    // "P21"
    frequency: number         // 5
}

interface ZoneData {
    count: number             // Total de códigos en esta zona
    codes: CodeReference[]    // Lista de códigos con frecuencias
    quotes: string[]          // Citas verbatim
}

interface StructureBodyMap {
    structure_id: number      // 1, 2, 3
    structure_name: string    // "Cascada Psicofisiológica"
    participants: string[]    // ["P30", "P19"]
    zones: {
        [zoneName: string]: ZoneData
    }
}

interface BodyMapProps {
    data: {
        structures?: StructureBodyMap[]  // Si viene del análisis estructural
        body_map_data?: any              // Fallback al formato antiguo
    }
}

// ============================================================================
// COMPONENTE PRINCIPAL
// ============================================================================

export function BodyMap({ data }: BodyMapProps) {
    const [selectedStructure, setSelectedStructure] = useState<number>(0)
    const [hoveredPart, setHoveredPart] = useState<string | null>(null)
    const [selectedPart, setSelectedPart] = useState<string | null>(null)

    // ========================================================================
    // COMPATIBILIDAD: Detectar formato de datos
    // ========================================================================

    const hasStructures = data?.structures && data.structures.length > 0
    const currentMap = hasStructures
        ? data.structures[selectedStructure]
        : null

    // Fallback al formato antiguo
    const legacyData = !hasStructures ? data?.body_map_data || data : null

    if (!hasStructures && !legacyData) {
        return (
            <div className="w-full h-[500px] bg-foreground/5 rounded-lg flex items-center justify-center">
                <p className="text-foreground/40">No body map data available</p>
            </div>
        )
    }

    // ========================================================================
    // FUNCIONES DE COLORACIÓN
    // ========================================================================

    const getColor = (zone: string) => {
        if (hasStructures && currentMap) {
            const count = currentMap.zones[zone]?.count || 0
            if (count === 0) return "#ffffff"
            if (count <= 2) return "#fbbf24"  // amarillo
            if (count <= 5) return "#f59e0b"  // naranja
            if (count <= 8) return "#ea580c"  // naranja oscuro
            return "#dc2626"                   // rojo intenso
        }
        // Formato legacy
        const count = legacyData?.[zone]?.count || 0
        return count > 0 ? "#e19136" : "#ffffff"
    }

    const getOpacity = (zone: string) => {
        const count = hasStructures
            ? (currentMap?.zones[zone]?.count || 0)
            : (legacyData?.[zone]?.count || 0)

        if (count === 0) return 0.1
        return 0.4 + Math.min(count * 0.08, 0.6)
    }

    // ========================================================================
    // HANDLERS
    // ========================================================================

    const handlePartClick = (zone: string) => {
        const hasData = hasStructures
            ? (currentMap?.zones[zone]?.count || 0) > 0
            : (legacyData?.[zone]?.count || 0) > 0

        if (hasData) {
            setSelectedPart(selectedPart === zone ? null : zone)
        }
    }

    // ========================================================================
    // RENDER DE ZONA CORPORAL
    // ========================================================================

    const renderPart = (id: string, element: React.ReactNode) => (
        <g
            onClick={() => handlePartClick(id)}
            onMouseEnter={() => setHoveredPart(id)}
            onMouseLeave={() => setHoveredPart(null)}
            className="cursor-pointer transition-all duration-300 hover:opacity-100"
            style={{ opacity: hoveredPart === id ? 1 : undefined }}
        >
            {element}
        </g>
    )

    // ========================================================================
    // TOOLTIP HOVER
    // ========================================================================

    const renderHoverTooltip = () => {
        if (!hoveredPart) return null

        const zoneData = hasStructures
            ? currentMap?.zones[hoveredPart]
            : legacyData?.[hoveredPart]

        if (!zoneData || zoneData.count === 0) return null

        return (
            <div className="absolute top-12 left-1/2 -translate-x-1/2 bg-black/90 text-white text-xs px-3 py-2 rounded-lg pointer-events-none z-20 shadow-lg max-w-sm">
                <div className="font-semibold text-[#e19136] mb-1">
                    {hoveredPart.replace(/_/g, " ").toUpperCase()}
                </div>
                <div className="text-foreground/80">
                    {zoneData.count} código{zoneData.count !== 1 ? 's' : ''}
                </div>
                {hasStructures && zoneData.codes && (
                    <div className="mt-1 space-y-0.5">
                        {zoneData.codes.slice(0, 2).map((ref: CodeReference, i: number) => (
                            <div key={i} className="text-[10px] text-foreground/60">
                                • {ref.code.split('-').slice(0, 2).join('-')}... ({ref.participant_id}: {ref.frequency}x)
                            </div>
                        ))}
                        {zoneData.codes.length > 2 && (
                            <div className="text-[10px] text-foreground/50">
                                + {zoneData.codes.length - 2} más
                            </div>
                        )}
                    </div>
                )}
            </div>
        )
    }

    // ========================================================================
    // PANEL DE CÓDIGOS DETALLADOS
    // ========================================================================

    const renderCodesPanel = () => {
        if (!selectedPart) {
            return (
                <div className="flex flex-col items-center justify-center h-full text-foreground/40 text-center">
                    <p className="text-sm">Haz clic en una zona del cuerpo</p>
                    <p className="text-xs mt-2">para ver códigos asociados</p>
                </div>
            )
        }

        const zoneData = hasStructures
            ? currentMap?.zones[selectedPart]
            : legacyData?.[selectedPart]

        if (!zoneData) return null

        return (
            <>
                <div className="flex justify-between items-center mb-4 border-b border-foreground/10 pb-3">
                    <div>
                        <h3 className="text-lg font-medium text-[#e19136] capitalize">
                            {selectedPart.replace(/_/g, " ")}
                        </h3>
                        <p className="text-xs text-foreground/50 mt-1">
                            {zoneData.count} código{zoneData.count !== 1 ? 's' : ''} identificado{zoneData.count !== 1 ? 's' : ''}
                        </p>
                    </div>
                    <button
                        onClick={() => setSelectedPart(null)}
                        className="p-1 hover:bg-foreground/10 rounded-full transition-colors"
                    >
                        <X className="w-4 h-4 text-foreground/60" />
                    </button>
                </div>

                <div className="overflow-y-auto pr-2 space-y-3 flex-1 custom-scrollbar">
                    {/* MODO NUEVO: Códigos con frecuencias */}
                    {hasStructures && zoneData.codes ? (
                        // Agrupar códigos por código base
                        Object.entries(
                            zoneData.codes.reduce((acc: any, ref: CodeReference) => {
                                if (!acc[ref.code]) {
                                    acc[ref.code] = []
                                }
                                acc[ref.code].push(ref)
                                return acc
                            }, {})
                        ).map(([code, refs]: [string, any], i: number) => {
                            const totalFreq = refs.reduce((sum: number, r: CodeReference) => sum + r.frequency, 0)

                            return (
                                <div key={i} className="bg-background/50 p-3 rounded-lg border-l-2 border-[#e19136]">
                                    <div className="flex justify-between items-start mb-2">
                                        <code className="text-xs text-[#e19136] font-mono flex-1 break-words">
                                            {code}
                                        </code>
                                        <span className="text-xs font-semibold text-foreground/60 ml-2 shrink-0">
                                            {totalFreq}x
                                        </span>
                                    </div>

                                    {/* Frecuencias por participante */}
                                    <div className="flex flex-wrap gap-1 mt-2">
                                        {refs.map((ref: CodeReference, j: number) => (
                                            <span
                                                key={j}
                                                className="text-[10px] bg-foreground/5 px-2 py-0.5 rounded"
                                            >
                                                {ref.participant_id}: {ref.frequency}x
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )
                        })
                    ) : (
                        // MODO LEGACY: Quotes
                        zoneData.quotes && zoneData.quotes.length > 0 ? (
                            zoneData.quotes.map((quote: string, i: number) => (
                                <div key={i} className="bg-background/50 p-4 rounded border-l-2 border-[#e19136]">
                                    <p className="text-sm text-foreground/90 italic leading-relaxed">
                                        "{quote}"
                                    </p>
                                </div>
                            ))
                        ) : (
                            <p className="text-foreground/40 text-sm">
                                No hay datos para esta zona
                            </p>
                        )
                    )}

                    {/* Quotes adicionales si existen */}
                    {hasStructures && zoneData.quotes && zoneData.quotes.length > 0 && (
                        <div className="mt-4 pt-4 border-t border-foreground/10">
                            <h4 className="text-xs font-semibold text-foreground/60 mb-2">
                                Citas verbatim
                            </h4>
                            {zoneData.quotes.slice(0, 3).map((quote: string, i: number) => (
                                <div key={i} className="bg-background/30 p-2 rounded text-xs text-foreground/70 italic mb-2">
                                    "{quote}"
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </>
        )
    }

    // ========================================================================
    // RENDER PRINCIPAL
    // ========================================================================

    return (
        <div className="w-full space-y-6">
            {/* Selector de Estructura (solo si hay múltiples) */}
            {hasStructures && data.structures!.length > 1 && (
                <div className="flex flex-col gap-3">
                    <h3 className="text-lg font-medium text-foreground/80">
                        Body Maps por Estructura Experiencial
                    </h3>

                    <div className="flex gap-2 flex-wrap">
                        {data.structures!.map((structure, idx) => (
                            <button
                                key={idx}
                                onClick={() => {
                                    setSelectedStructure(idx)
                                    setSelectedPart(null)
                                }}
                                className={`
                                    px-4 py-2 rounded-lg text-sm transition-all
                                    ${selectedStructure === idx
                                        ? 'bg-[#e19136] text-white shadow-lg'
                                        : 'bg-foreground/5 text-foreground/70 hover:bg-foreground/10'
                                    }
                                `}
                            >
                                <div className="font-medium">
                                    Estructura {structure.structure_id}
                                </div>
                                <div className="text-xs opacity-80 mt-1">
                                    {structure.structure_name}
                                </div>
                                <div className="text-xs opacity-60 mt-1">
                                    {structure.participants.join(", ")}
                                </div>
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Body Map + Panel */}
            <div className="flex flex-col md:flex-row gap-8 w-full">
                {/* SVG Body Map */}
                <div className="relative w-full md:w-1/2 h-[500px] bg-foreground/5 rounded-lg p-4 flex flex-col items-center justify-center">
                    <h4 className="absolute top-4 left-4 text-foreground/80 font-mono text-sm">
                        {hasStructures && currentMap
                            ? currentMap.structure_name
                            : "Corporeal Resonance Map"
                        }
                    </h4>

                    {renderHoverTooltip()}

                    <svg viewBox="0 0 200 400" className="h-full w-auto drop-shadow-2xl">
                        {/* Silueta base (outline) */}
                        <g opacity="0.3" stroke="#ffffff" strokeWidth="1.5" fill="none">
                            {/* Cabeza */}
                            <circle cx="100" cy="40" r="25" />
                            {/* Cuello */}
                            <path d="M90,63 L90,73 L110,73 L110,63" />
                            {/* Torso */}
                            <path d="M70,70 C50,80 40,100 30,150 L20,250 L40,260 L50,160 C50,160 60,200 60,250 L60,380 L90,380 L90,280 L110,280 L110,380 L140,380 L140,250 C140,200 150,160 150,160 L160,260 L180,250 L170,150 C160,100 150,80 130,70 Z" />
                            {/* Brazos */}
                            <path d="M70,80 L30,180 L40,185 L75,100" />
                            <path d="M130,80 L170,180 L160,185 L125,100" />
                        </g>

                        {/* Zonas interactivas */}
                        {renderPart("head",
                            <circle
                                cx="100"
                                cy="40"
                                r="25"
                                fill={getColor("head")}
                                fillOpacity={getOpacity("head")}
                                stroke={getOpacity("head") > 0.3 ? "#e19136" : "transparent"}
                                strokeWidth="2"
                            />
                        )}

                        {renderPart("neck",
                            <rect
                                x="88"
                                y="63"
                                width="24"
                                height="12"
                                rx="4"
                                fill={getColor("neck")}
                                fillOpacity={getOpacity("neck")}
                                stroke={getOpacity("neck") > 0.3 ? "#e19136" : "transparent"}
                                strokeWidth="2"
                            />
                        )}

                        {renderPart("chest",
                            <ellipse
                                cx="100"
                                cy="100"
                                rx="35"
                                ry="25"
                                fill={getColor("chest")}
                                fillOpacity={getOpacity("chest")}
                                stroke={getOpacity("chest") > 0.3 ? "#e19136" : "transparent"}
                                strokeWidth="2"
                            />
                        )}

                        {renderPart("solar_plexus",
                            <circle
                                cx="100"
                                cy="140"
                                r="15"
                                fill={getColor("solar_plexus")}
                                fillOpacity={getOpacity("solar_plexus")}
                                stroke={getOpacity("solar_plexus") > 0.3 ? "#e19136" : "transparent"}
                                strokeWidth="2"
                            />
                        )}

                        {renderPart("abdomen",
                            <ellipse
                                cx="100"
                                cy="180"
                                rx="30"
                                ry="20"
                                fill={getColor("abdomen")}
                                fillOpacity={getOpacity("abdomen")}
                                stroke={getOpacity("abdomen") > 0.3 ? "#e19136" : "transparent"}
                                strokeWidth="2"
                            />
                        )}

                        {renderPart("pelvis",
                            <path
                                d="M70,210 Q100,240 130,210 L120,250 Q100,260 80,250 Z"
                                fill={getColor("pelvis")}
                                fillOpacity={getOpacity("pelvis")}
                                stroke={getOpacity("pelvis") > 0.3 ? "#e19136" : "transparent"}
                                strokeWidth="2"
                            />
                        )}

                        {renderPart("extremities", (
                            <g
                                fill={getColor("extremities")}
                                fillOpacity={getOpacity("extremities")}
                                stroke={getOpacity("extremities") > 0.3 ? "#e19136" : "transparent"}
                                strokeWidth="2"
                            >
                                <circle cx="30" cy="180" r="10" />
                                <circle cx="170" cy="180" r="10" />
                                <circle cx="75" cy="380" r="10" />
                                <circle cx="125" cy="380" r="10" />
                            </g>
                        ))}
                    </svg>

                    {/* Leyenda de colores (solo en modo estructural) */}
                    {hasStructures && (
                        <div className="absolute bottom-4 right-4 bg-black/80 p-3 rounded-lg text-xs space-y-1">
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded" style={{ backgroundColor: "#fbbf24" }} />
                                <span className="text-white">1-2 códigos</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded" style={{ backgroundColor: "#f59e0b" }} />
                                <span className="text-white">3-5 códigos</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded" style={{ backgroundColor: "#ea580c" }} />
                                <span className="text-white">6-8 códigos</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded" style={{ backgroundColor: "#dc2626" }} />
                                <span className="text-white">9+ códigos</span>
                            </div>
                        </div>
                    )}
                </div>

                {/* Panel de códigos */}
                <div className="w-full md:w-1/2 h-[500px] bg-foreground/5 rounded-lg p-6 overflow-hidden flex flex-col">
                    {renderCodesPanel()}
                </div>
            </div>
        </div>
    )
}