"use client"

import { X } from "lucide-react"
import { useEffect, useState } from "react"

interface InstructionsModalProps {
    isOpen: boolean
    onClose: () => void
    t: any
}

export function InstructionsModal({ isOpen, onClose, t }: InstructionsModalProps) {
    const [visible, setVisible] = useState(false)

    useEffect(() => {
        if (isOpen) {
            setVisible(true)
            document.body.style.overflow = "hidden"
        } else {
            const timer = setTimeout(() => setVisible(false), 300)
            document.body.style.overflow = "unset"
            return () => clearTimeout(timer)
        }
    }, [isOpen])

    if (!visible && !isOpen) return null

    return (
        <div
            className={`fixed inset-0 z-[100] flex items-center justify-center p-4 transition-opacity duration-300 ${isOpen ? "opacity-100" : "opacity-0"}`}
        >
            <div
                className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                onClick={onClose}
            />
            <div
                className={`relative w-full max-w-lg bg-[#0a0a0a] border border-white/10 rounded-2xl p-8 shadow-2xl transform transition-all duration-300 ${isOpen ? "scale-100 translate-y-0" : "scale-95 translate-y-4"}`}
            >
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-white/50 hover:text-white transition-colors"
                >
                    <X size={20} />
                </button>

                <h2 className="text-2xl font-light text-white mb-6">{t.title}</h2>

                <div className="space-y-4">
                    {t.steps.map((step: string, i: number) => (
                        <div key={i} className="flex gap-4">
                            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-xs font-mono text-white/80">
                                {i + 1}
                            </div>
                            <p className="text-white/70 text-sm leading-relaxed">
                                {step}
                            </p>
                        </div>
                    ))}
                </div>

                <div className="mt-8 pt-6 border-t border-white/10 flex justify-end">
                    <button
                        onClick={onClose}
                        className="text-sm text-white/60 hover:text-white transition-colors"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    )
}
