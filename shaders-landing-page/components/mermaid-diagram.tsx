"use client"

import React, { useEffect, useRef, useState } from "react"
import mermaid from "mermaid"

interface MermaidDiagramProps {
    chart: string
}

export function MermaidDiagram({ chart }: MermaidDiagramProps) {
    const ref = useRef<HTMLDivElement>(null)
    const [svg, setSvg] = useState<string>("")
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        mermaid.initialize({
            startOnLoad: false,
            theme: "dark",
            securityLevel: "loose",
            fontFamily: "monospace",
        })
    }, [])

    useEffect(() => {
        const renderChart = async () => {
            if (!chart || !ref.current) return

            try {
                const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`
                const { svg } = await mermaid.render(id, chart)
                setSvg(svg)
                setError(null)
            } catch (err) {
                console.error("Mermaid render error:", err)
                setError("Failed to render diagram")
            }
        }

        renderChart()
    }, [chart])

    if (error) {
        return (
            <div className="p-4 border border-red-500/50 rounded bg-red-500/10 text-red-500 font-mono text-xs">
                {error}
                <pre className="mt-2 text-foreground/50">{chart}</pre>
            </div>
        )
    }

    return (
        <div
            ref={ref}
            className="w-full overflow-x-auto bg-foreground/5 p-4 rounded-lg flex justify-center"
            dangerouslySetInnerHTML={{ __html: svg }}
        />
    )
}
