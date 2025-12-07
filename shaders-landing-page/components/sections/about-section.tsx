"use client"

import { MagneticButton } from "@/components/magnetic-button"
import { useReveal } from "@/hooks/use-reveal"

interface AboutSectionProps {
  scrollToSection: (index: number) => void
}

export function AboutSection({ scrollToSection }: AboutSectionProps) {
  const { ref, isVisible } = useReveal(0.3)

  return (
    <section
      ref={ref}
      className="flex min-h-screen w-screen shrink-0 flex-col justify-center px-6 md:px-12"
    >
      <div className="max-w-6xl mx-auto w-full">
        <h2 className={`mb-8 text-4xl font-light leading-tight text-foreground transition-all duration-700 md:text-5xl lg:text-6xl ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
          Construyendo el futuro de la fenomenología
        </h2>

        <div className={`grid gap-12 transition-all duration-700 delay-200 md:grid-cols-2 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
          <div className="space-y-6">
            <p className="text-lg leading-relaxed text-foreground/80">
              Somos expertos en psicología, fenomenología y ciencia de datos e inteligencia artificial, movidos por combinar rigurosidad, curiosidad e innovación en las fronteras de la investigación cualitativa.
            </p>
            <div className="flex gap-4">
              <MagneticButton variant="primary" onClick={() => window.location.href = "mailto:reinerfuentes7@gmail.com"}>
                Hablemos
              </MagneticButton>
            </div>
          </div>

          <div className="space-y-8">
            {/* Contact info removed as requested */}
          </div>
        </div>
      </div>
    </section>
  )
}
