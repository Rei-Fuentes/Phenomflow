"use client"

import React, { useState } from "react"
import { X } from "lucide-react"

interface BodyMapProps {
    data: any // Expecting body_map_data from backend
}

export function BodyMap({ data }: BodyMapProps) {
    const [hoveredPart, setHoveredPart] = useState<string | null>(null)
    const [selectedPart, setSelectedPart] = useState<string | null>(null)

    // If no data provided, return empty or placeholder
    if (!data) return null

    const getOpacity = (zone: string) => {
        const count = data[zone]?.count || 0
        return count > 0 ? 0.4 + Math.min(count * 0.1, 0.6) : 0.1
    }

    const getColor = (zone: string) => {
        const count = data[zone]?.count || 0
        return count > 0 ? "#e19136" : "#ffffff"
    }

    const handlePartClick = (zone: string) => {
        if (data[zone]?.count > 0) {
            setSelectedPart(zone)
        }
    }

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

    return (
        <div className="flex flex-col md:flex-row gap-8 w-full">
            {/* Map Container */}
            <div className="relative w-full md:w-1/2 h-[500px] bg-foreground/5 rounded-lg p-4 flex flex-col items-center justify-center">
                <h4 className="absolute top-4 left-4 text-foreground/80 font-mono text-sm">Corporeal Resonance Map</h4>

                {/* Hover Tooltip */}
                {hoveredPart && data[hoveredPart] && (
                    <div className="absolute top-12 bg-black/80 text-white text-xs px-2 py-1 rounded pointer-events-none z-10">
                        {hoveredPart.replace("_", " ").toUpperCase()}: {data[hoveredPart].count} mentions
                    </div>
                )}

                <svg viewBox="0 0 200 400" className="h-full w-auto drop-shadow-2xl">
                    {/* Silhouette Outline */}
                    <path
                        d="M100,10 C120,10 130,25 130,45 C130,60 120,70 100,70 C80,70 70,60 70,45 C70,25 80,10 100,10 Z"
                        fill="none"
                        stroke="#ffffff30"
                        strokeWidth="2"
                    />
                    <path
                        d="M70,70 C50,80 40,100 30,150 L20,250 L40,260 L50,160 C50,160 60,200 60,250 L60,380 L90,380 L90,280 L110,280 L110,380 L140,380 L140,250 C140,200 150,160 150,160 L160,260 L180,250 L170,150 C160,100 150,80 130,70 Z"
                        fill="none"
                        stroke="#ffffff30"
                        strokeWidth="2"
                    />

                    {/* Interactive Zones */}
                    {renderPart("head", <circle cx="100" cy="40" r="25" fill={getColor("head")} fillOpacity={getOpacity("head")} />)}
                    {renderPart("chest", <ellipse cx="100" cy="100" rx="35" ry="25" fill={getColor("chest")} fillOpacity={getOpacity("chest")} />)}
                    {renderPart("solar_plexus", <circle cx="100" cy="140" r="15" fill={getColor("solar_plexus")} fillOpacity={getOpacity("solar_plexus")} />)}
                    {renderPart("abdomen", <ellipse cx="100" cy="180" rx="30" ry="20" fill={getColor("abdomen")} fillOpacity={getOpacity("abdomen")} />)}
                    {renderPart("pelvis", <path d="M70,210 Q100,240 130,210 L120,250 Q100,260 80,250 Z" fill={getColor("pelvis")} fillOpacity={getOpacity("pelvis")} />)}

                    {renderPart("extremities", (
                        <g fill={getColor("extremities")} fillOpacity={getOpacity("extremities")}>
                            <circle cx="30" cy="250" r="10" />
                            <circle cx="170" cy="250" r="10" />
                            <circle cx="75" cy="380" r="10" />
                            <circle cx="125" cy="380" r="10" />
                        </g>
                    ))}
                </svg>
            </div>

            {/* Quotes Panel (Side) */}
            <div className="w-full md:w-1/2 h-[500px] bg-foreground/5 rounded-lg p-6 overflow-hidden flex flex-col relative">
                {!selectedPart ? (
                    <div className="flex flex-col items-center justify-center h-full text-foreground/40 text-center">
                        <p>Click on a highlighted body part</p>
                        <p className="text-sm">to view associated quotes</p>
                    </div>
                ) : (
                    <>
                        <div className="flex justify-between items-center mb-6 border-b border-foreground/10 pb-4">
                            <h3 className="text-xl font-light text-[#e19136] capitalize">
                                {selectedPart.replace("_", " ")}
                            </h3>
                            <button
                                onClick={() => setSelectedPart(null)}
                                className="p-1 hover:bg-foreground/10 rounded-full transition-colors"
                            >
                                <X className="w-5 h-5 text-foreground/60" />
                            </button>
                        </div>

                        <div className="overflow-y-auto pr-2 space-y-4 flex-1 custom-scrollbar">
                            {data[selectedPart]?.quotes && data[selectedPart].quotes.length > 0 ? (
                                data[selectedPart].quotes.map((quote: string, i: number) => (
                                    <div key={i} className="bg-background/50 p-4 rounded border-l-2 border-[#e19136]">
                                        <p className="text-sm text-foreground/90 italic leading-relaxed">"{quote}"</p>
                                    </div>
                                ))
                            ) : (
                                <p className="text-foreground/40 text-sm">No quotes found for this section.</p>
                            )}
                        </div>
                    </>
                )}
            </div>
        </div>
    )
}
