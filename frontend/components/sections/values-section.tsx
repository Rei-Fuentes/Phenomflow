"use client"

import { useReveal } from "@/hooks/use-reveal"

interface ValuesSectionProps {
    t: any
}

export function ValuesSection({ t }: ValuesSectionProps) {
    const { ref, isVisible } = useReveal(0.2)

    return (
        <section
            ref={ref}
            className="flex min-h-screen w-screen shrink-0 flex-col justify-center px-6 md:px-12"
        >
            <div className="max-w-6xl mx-auto w-full">
                <h2 className={`mb-16 text-4xl font-light text-foreground transition-all duration-700 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
                    {t.title}
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {t.items.map((item: any, i: number) => (
                        <div
                            key={i}
                            className={`p-6 border-l border-foreground/20 transition-all duration-700 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
                            style={{ transitionDelay: `${i * 150}ms` }}
                        >
                            <h3 className="text-xl font-medium text-foreground mb-4">{item.title}</h3>
                            <p className="text-sm text-foreground/70 leading-relaxed">{item.desc}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}
