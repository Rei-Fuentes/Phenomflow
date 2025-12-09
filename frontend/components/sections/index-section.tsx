"use client"

import { useReveal } from "@/hooks/use-reveal"

interface IndexSectionProps {
    t: any
    onNavigate: (index: number) => void
}

export function IndexSection({ t, onNavigate }: IndexSectionProps) {
    const { ref, isVisible } = useReveal(0.2)

    return (
        <section
            ref={ref}
            className="flex min-h-screen w-screen shrink-0 flex-col justify-center px-6 md:px-12"
        >
            <div className="max-w-4xl mx-auto w-full">
                <h2 className={`mb-12 text-4xl font-light text-foreground transition-all duration-700 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
                    {t.title}
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {t.sections.map((section: any, i: number) => (
                        <button
                            key={i}
                            onClick={() => onNavigate(section.id)}
                            className={`group text-left p-6 rounded-xl border border-foreground/10 bg-foreground/5 hover:bg-foreground/10 transition-all duration-500 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
                            style={{ transitionDelay: `${i * 100}ms` }}
                        >
                            <div className="flex justify-between items-start mb-2">
                                <span className="font-mono text-xs text-foreground/40">0{section.id}</span>
                                <span className="text-foreground/40 group-hover:text-foreground transition-colors">→</span>
                            </div>
                            <h3 className="text-xl font-medium text-foreground mb-2">{section.title}</h3>
                            <p className="text-sm text-foreground/60">{section.desc}</p>
                        </button>
                    ))}
                </div>
            </div>
        </section>
    )
}
