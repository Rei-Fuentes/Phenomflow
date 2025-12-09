"use client"

import { useReveal } from "@/hooks/use-reveal"
import { ResearchContextForm } from "@/components/research-context-form"

interface ContextSectionProps {
    onContextSubmit: (data: any) => void
    t: any
}

export function ContextSection({ onContextSubmit, t }: ContextSectionProps) {
    const { ref, isVisible } = useReveal(0.3)

    return (
        <section
            ref={ref}
            className="flex min-h-screen w-screen shrink-0 flex-col justify-center px-6 md:px-12"
        >
            <div className="max-w-4xl mx-auto w-full">
                <h2 className={`mb-8 text-3xl font-light text-foreground transition-all duration-700 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
                    {t.nav.context}
                </h2>
                <div className={`transition-all duration-700 delay-200 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
                    <ResearchContextForm onSubmit={onContextSubmit} />
                </div>
            </div>
        </section>
    )
}
