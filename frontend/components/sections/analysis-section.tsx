"use client"

import { useState } from "react"
import { MagneticButton } from "@/components/magnetic-button"
import { useReveal } from "@/hooks/use-reveal"

export function AnalysisSection() {
    const { ref, isVisible } = useReveal(0.3)
    const [inputText, setInputText] = useState("")
    const [result, setResult] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [uploadedFile, setUploadedFile] = useState<File | null>(null)
    const [documentStructure, setDocumentStructure] = useState<any>(null)

    const handleFileUpload = async (file: File) => {
        setIsLoading(true)
        setUploadedFile(file)
        try {
            const formData = new FormData()
            formData.append("file", file)

            const response = await fetch("http://localhost:8000/analyze/document", {
                method: "POST",
                body: formData,
            })
            const data = await response.json()

            setDocumentStructure(data.document_structure)
            setResult(JSON.stringify(data.analysis, null, 2))
        } catch (error) {
            console.error("Error uploading document:", error)
            setResult("Error occurred during document analysis.")
        } finally {
            setIsLoading(false)
        }
    }

    const handleAnalyze = async () => {
        if (!inputText) return
        setIsLoading(true)
        try {
            const response = await fetch("http://localhost:8000/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ text: inputText }),
            })
            const data = await response.json()
            setResult(data.result)
        } catch (error) {
            console.error("Error analyzing text:", error)
            setResult("Error occurred during analysis.")
        } finally {
            setIsLoading(false)
        }
    }

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault()
        const file = e.dataTransfer.files[0]
        if (file && (file.type === "application/pdf" || file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document")) {
            handleFileUpload(file)
        }
    }

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (file) {
            handleFileUpload(file)
        }
    }

    return (
        <section
            ref={ref}
            className="flex h-screen w-screen shrink-0 snap-start items-center px-4 pt-20 md:px-12 md:pt-0 lg:px-16"
        >
            <div className="mx-auto w-full max-w-7xl">
                <div className="grid gap-8 md:grid-cols-2 md:gap-16 lg:gap-24">
                    {/* Left side - Input */}
                    <div>
                        <div
                            className={`mb-6 transition-all duration-700 md:mb-12 ${isVisible ? "translate-y-0 opacity-100" : "-translate-y-12 opacity-0"
                                }`}
                        >
                            <h2 className="mb-3 font-sans text-3xl font-light leading-[1.1] tracking-tight text-foreground md:mb-4 md:text-6xl lg:text-7xl">
                                Phenomenological
                                <br />
                                <span className="text-foreground/40">Analysis</span>
                            </h2>
                        </div>

                        <div
                            className={`space-y-3 transition-all duration-700 md:space-y-4 ${isVisible ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
                                }`}
                            style={{ transitionDelay: "200ms" }}
                        >
                            {/* File Upload Area */}
                            <div
                                className="border-2 border-dashed border-foreground/20 rounded-lg p-6 text-center hover:border-foreground/40 transition-colors"
                                onDrop={handleDrop}
                                onDragOver={(e) => e.preventDefault()}
                            >
                                <input
                                    type="file"
                                    accept=".pdf,.docx,.doc"
                                    onChange={handleFileSelect}
                                    className="hidden"
                                    id="file-upload"
                                />
                                <label htmlFor="file-upload" className="cursor-pointer">
                                    <div className="font-mono text-sm text-foreground/60">
                                        {uploadedFile ? (
                                            <span className="text-foreground">📄 {uploadedFile.name}</span>
                                        ) : (
                                            <>
                                                <div>Drop PDF or Word file here</div>
                                                <div className="text-xs mt-1">or click to browse</div>
                                            </>
                                        )}
                                    </div>
                                </label>
                            </div>

                            <div className="text-center font-mono text-xs text-foreground/40">OR</div>

                            <textarea
                                className="w-full h-64 p-4 bg-foreground/5 text-foreground border border-foreground/10 rounded-lg focus:outline-none focus:border-foreground/30 resize-none font-mono text-sm"
                                placeholder="Paste interview text here..."
                                value={inputText}
                                onChange={(e) => setInputText(e.target.value)}
                            />

                            <div className="flex gap-4">
                                <MagneticButton size="lg" variant="primary" onClick={handleAnalyze}>
                                    {isLoading ? "Analyzing..." : "Analyze Text"}
                                </MagneticButton>
                            </div>

                            {documentStructure && (
                                <div className="mt-4 p-4 bg-foreground/5 rounded-lg">
                                    <div className="font-mono text-xs text-foreground/80">
                                        <div>📊 Document Structure Detected:</div>
                                        <div className="mt-2">
                                            {documentStructure.participant_code && (
                                                <div>• Participant: {documentStructure.participant_code}</div>
                                            )}
                                            <div>• Total turns: {documentStructure.total_turns}</div>
                                            <div>• Participant turns: {documentStructure.participant_turns}</div>
                                            <div>• Interviewer turns: {documentStructure.interviewer_turns}</div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Right side - Result */}
                    <div className="flex flex-col justify-center h-full">
                        <div
                            className={`h-full max-h-[70vh] overflow-y-auto p-6 bg-foreground/5 rounded-lg border border-foreground/10 transition-all duration-700 ${isVisible ? "translate-x-0 opacity-100" : "translate-x-16 opacity-0"
                                }`}
                            style={{ transitionDelay: "300ms" }}
                        >
                            {result ? (
                                <div className="prose prose-invert max-w-none">
                                    <h3 className="text-xl font-light mb-4">Analysis Result</h3>
                                    <div className="whitespace-pre-wrap font-mono text-sm text-foreground/80">
                                        {result}
                                    </div>
                                </div>
                            ) : (
                                <div className="h-full flex items-center justify-center text-foreground/40 font-mono text-sm">
                                    Analysis results will appear here
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}
