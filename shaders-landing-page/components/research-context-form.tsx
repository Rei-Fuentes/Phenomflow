"use client"

import { useState } from "react"
import { MagneticButton } from "@/components/magnetic-button"

interface ResearchContextData {
    research_question: string
    study_objective: string
    phenomenological_approach: string
    participant_context: string
    interview_type: string
    interview_timing: string
}

interface ResearchContextFormProps {
    onSubmit: (data: ResearchContextData | null) => void
}

export function ResearchContextForm({ onSubmit }: ResearchContextFormProps) {
    const [step, setStep] = useState(1)
    const [formData, setFormData] = useState<ResearchContextData>({
        research_question: "",
        study_objective: "",
        phenomenological_approach: "",
        participant_context: "",
        interview_type: "",
        interview_timing: "",
    })

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    const handleNext = () => setStep(step + 1)
    const handleBack = () => setStep(step - 1)

    const handleSubmit = () => {
        onSubmit(formData)
    }

    const handleSkip = () => {
        if (confirm("Are you sure? Analyzing without context may reduce precision by up to 40%.")) {
            onSubmit(null)
        }
    }

    return (
        <div className="w-full max-w-2xl mx-auto bg-foreground/5 p-8 rounded-lg border border-foreground/10">
            <div className="mb-8 flex justify-between items-center">
                <h3 className="text-xl font-light text-foreground">Phase 0: Research Context</h3>
                <span className="text-xs font-mono text-foreground/40">Step {step} of 3</span>
            </div>

            {step === 1 && (
                <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
                    <div>
                        <label className="block text-sm font-mono text-foreground/70 mb-2">
                            Research Question
                        </label>
                        <input
                            name="research_question"
                            value={formData.research_question}
                            onChange={handleChange}
                            placeholder="What phenomenon do you want to understand in depth?"
                            className="w-full p-3 bg-foreground/5 border border-foreground/10 rounded focus:outline-none focus:border-foreground/30 text-sm"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-mono text-foreground/70 mb-2">
                            Study Objective
                        </label>
                        <textarea
                            name="study_objective"
                            value={formData.study_objective}
                            onChange={handleChange}
                            placeholder="What do you aim to achieve in terms of phenomenological understanding?"
                            className="w-full p-3 bg-foreground/5 border border-foreground/10 rounded focus:outline-none focus:border-foreground/30 text-sm h-24 resize-none"
                        />
                    </div>
                    <div className="flex justify-between pt-4">
                        <button onClick={handleSkip} className="text-xs text-foreground/40 hover:text-foreground/60 underline">
                            Skip & Analyze without Context
                        </button>
                        <MagneticButton size="sm" variant="primary" onClick={handleNext}>
                            Next Step
                        </MagneticButton>
                    </div>
                </div>
            )}

            {step === 2 && (
                <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
                    <div>
                        <label className="block text-sm font-mono text-foreground/70 mb-2">
                            Phenomenological Approach
                        </label>
                        <select
                            name="phenomenological_approach"
                            value={formData.phenomenological_approach}
                            onChange={handleChange}
                            className="w-full p-3 bg-foreground/5 border border-foreground/10 rounded focus:outline-none focus:border-foreground/30 text-sm"
                        >
                            <option value="">Select an approach...</option>
                            <option value="Micro-phenomenology (Petitmengin)">Micro-phenomenology (Petitmengin)</option>
                            <option value="IPA (Interpretative Phenomenological Analysis)">IPA</option>
                            <option value="Descriptive Phenomenology (Husserl)">Descriptive Phenomenology (Husserl)</option>
                            <option value="Existential Phenomenology (Heidegger/Merleau-Ponty)">Existential Phenomenology</option>
                            <option value="Empirical Phenomenology">Empirical Phenomenology</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-mono text-foreground/70 mb-2">
                            Participant Context
                        </label>
                        <textarea
                            name="participant_context"
                            value={formData.participant_context}
                            onChange={handleChange}
                            placeholder="Age, population (clinical/general), inclusion/exclusion criteria..."
                            className="w-full p-3 bg-foreground/5 border border-foreground/10 rounded focus:outline-none focus:border-foreground/30 text-sm h-24 resize-none"
                        />
                    </div>
                    <div className="flex justify-between pt-4">
                        <MagneticButton size="sm" variant="secondary" onClick={handleBack}>
                            Back
                        </MagneticButton>
                        <MagneticButton size="sm" variant="primary" onClick={handleNext}>
                            Next Step
                        </MagneticButton>
                    </div>
                </div>
            )}

            {step === 3 && (
                <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
                    <div>
                        <label className="block text-sm font-mono text-foreground/70 mb-2">
                            Interview Type
                        </label>
                        <input
                            name="interview_type"
                            value={formData.interview_type}
                            onChange={handleChange}
                            placeholder="e.g., Semi-structured, Open-ended, Elicitation interview"
                            className="w-full p-3 bg-foreground/5 border border-foreground/10 rounded focus:outline-none focus:border-foreground/30 text-sm"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-mono text-foreground/70 mb-2">
                            Interview Protocol (Optional)
                        </label>
                        <div className="flex items-center gap-4">
                            <input
                                type="file"
                                id="protocol-upload"
                                className="hidden"
                                accept=".pdf,.docx,.doc"
                                onChange={(e) => {
                                    if (e.target.files && e.target.files[0]) {
                                        // Pass the file up via a separate handler or extend the formData type?
                                        // For simplicity, we'll just store it in local state and pass it on submit
                                        // But wait, the interface needs to change.
                                        // Let's assume the parent handles the file if we pass it.
                                        // Actually, we need to update the interface first.
                                        // For now, let's just use a callback prop for the file.
                                        const file = e.target.files[0]
                                        // We'll add a temporary field to formData for now or handle it in the parent
                                        // Let's update the onSubmit signature in the parent first.
                                        // HACK: We will attach it to the formData object as 'protocol_file' (any)
                                        setFormData({ ...formData, protocol_file: file } as any)
                                    }
                                }}
                            />
                            <MagneticButton size="sm" variant="secondary" onClick={() => document.getElementById('protocol-upload')?.click()}>
                                Upload Protocol
                            </MagneticButton>
                            {(formData as any).protocol_file && (
                                <span className="text-xs text-green-500">
                                    {(formData as any).protocol_file.name}
                                </span>
                            )}
                        </div>
                        <p className="text-xs text-foreground/40 mt-1">Upload your interview guide/protocol to help the AI understand your structure.</p>
                    </div>
                    <div>
                        <label className="block text-sm font-mono text-foreground/70 mb-2">
                            Timing relative to phenomenon
                        </label>
                        <select
                            name="interview_timing"
                            value={formData.interview_timing}
                            onChange={handleChange}
                            className="w-full p-3 bg-foreground/5 border border-foreground/10 rounded focus:outline-none focus:border-foreground/30 text-sm"
                        >
                            <option value="">Select timing...</option>
                            <option value="Immediate (during/right after)">Immediate (during/right after)</option>
                            <option value="Recent (days after)">Recent (days after)</option>
                            <option value="Retrospective (long term)">Retrospective (long term)</option>
                        </select>
                    </div>

                    <div className="bg-yellow-500/10 border border-yellow-500/20 p-4 rounded text-xs text-yellow-200/80 mt-4">
                        ℹ️ This context will be used to tailor the AI analysis to your specific research goals.
                    </div>

                    <div className="flex justify-between pt-4">
                        <MagneticButton size="sm" variant="secondary" onClick={handleBack}>
                            Back
                        </MagneticButton>
                        <MagneticButton size="sm" variant="primary" onClick={handleSubmit}>
                            Complete Setup & Start Analysis
                        </MagneticButton>
                    </div>
                </div>
            )}
        </div>
    )
}
