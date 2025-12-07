"use client"

import { useState, useRef } from "react"
import { Upload, FileText, CheckCircle, AlertCircle } from "lucide-react"
import { MagneticButton } from "@/components/magnetic-button"
import { useReveal } from "@/hooks/use-reveal"

interface MaterialsSectionProps {
    onAnalyze: (text: string, isFile: boolean, file?: File) => void
    isLoading: boolean
    t: any
}

export function MaterialsSection({ onAnalyze, isLoading, t }: MaterialsSectionProps) {
    const { ref, isVisible } = useReveal(0.3)
    const [inputText, setInputText] = useState("")
    const [dragActive, setDragActive] = useState(false)
    const [files, setFiles] = useState<File[]>([])
    const fileInputRef = useRef<HTMLInputElement>(null)

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true)
        } else if (e.type === "dragleave") {
            setDragActive(false)
        }
    }

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault()
        e.stopPropagation()
        setDragActive(false)
        if (e.dataTransfer.files) {
            handleFiles(Array.from(e.dataTransfer.files))
        }
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault()
        if (e.target.files) {
            handleFiles(Array.from(e.target.files))
        }
    }

    const handleFiles = (newFiles: File[]) => {
        const validFiles = newFiles.filter(file => {
            const ext = file.name.split('.').pop()?.toLowerCase()
            return ext === 'pdf' || ext === 'docx' || ext === 'doc'
        })

        if (validFiles.length !== newFiles.length) {
            alert("Some files were skipped. Only PDF and Word documents are supported.")
        }

        setFiles(prev => [...prev, ...validFiles])
        setInputText("") // Clear text if files are selected
    }

    const removeFile = (index: number) => {
        setFiles(prev => prev.filter((_, i) => i !== index))
    }

    const handleSubmit = () => {
        if (files.length > 0) {
            // Pass the array of files. The parent needs to handle this.
            // We'll modify the signature of onAnalyze in the parent to accept File[]
            // For now, we cast to any to bypass strict type check until parent is updated
            onAnalyze("", true, files as any)
        } else if (inputText) {
            onAnalyze(inputText, false)
        }
    }

    return (
        <section
            ref={ref}
            className="flex min-h-screen w-screen shrink-0 flex-col justify-center px-6 md:px-12"
        >
            <div className="max-w-4xl mx-auto w-full">
                <h2 className={`mb-8 text-3xl font-light text-foreground transition-all duration-700 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
                    {t.nav.materials}
                </h2>

                <div className={`grid grid-cols-1 md:grid-cols-2 gap-8 transition-all duration-700 delay-200 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>

                    {/* File Upload */}
                    <div
                        className={`relative border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-start text-center transition-colors min-h-[300px] ${dragActive ? "border-foreground bg-foreground/10" : "border-foreground/20 bg-foreground/5"}`}
                        onDragEnter={handleDrag}
                        onDragLeave={handleDrag}
                        onDragOver={handleDrag}
                        onDrop={handleDrop}
                    >
                        <input
                            ref={fileInputRef}
                            type="file"
                            className="hidden"
                            onChange={handleChange}
                            accept=".pdf,.docx,.doc"
                            multiple
                        />

                        {files.length > 0 ? (
                            <div className="w-full space-y-2 max-h-[250px] overflow-y-auto pr-2">
                                {files.map((file, i) => (
                                    <div key={i} className="flex items-center justify-between bg-foreground/10 p-3 rounded-lg">
                                        <div className="flex items-center gap-3 overflow-hidden">
                                            <div className="text-green-500 shrink-0">
                                                <CheckCircle size={16} />
                                            </div>
                                            <div className="text-left overflow-hidden">
                                                <p className="font-medium text-foreground text-xs truncate max-w-[150px]">{file.name}</p>
                                                <p className="text-[10px] text-foreground/60">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                                            </div>
                                        </div>
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation()
                                                removeFile(i)
                                            }}
                                            className="text-foreground/40 hover:text-red-400 transition-colors p-1"
                                        >
                                            <AlertCircle size={16} className="rotate-45" />
                                        </button>
                                    </div>
                                ))}
                                <button
                                    onClick={() => fileInputRef.current?.click()}
                                    className="text-xs text-foreground/60 hover:text-foreground underline mt-2"
                                >
                                    + Add more files
                                </button>
                            </div>
                        ) : (
                            <div className="space-y-4 my-auto">
                                <div className="w-16 h-16 bg-foreground/10 rounded-full flex items-center justify-center mx-auto text-foreground/60">
                                    <Upload size={32} />
                                </div>
                                <div>
                                    <p className="font-medium text-foreground">Drag & Drop Files</p>
                                    <p className="text-xs text-foreground/60">PDF or Word (.docx)</p>
                                </div>
                                <MagneticButton size="sm" variant="secondary" onClick={() => fileInputRef.current?.click()}>
                                    Browse Files
                                </MagneticButton>
                            </div>
                        )}
                    </div>

                    {/* Text Input */}
                    <div className="flex flex-col h-full">
                        <textarea
                            className="flex-1 w-full p-4 bg-foreground/5 text-foreground border border-foreground/10 rounded-xl focus:outline-none focus:border-foreground/30 resize-none font-mono text-sm min-h-[300px]"
                            placeholder="Or paste interview transcript here..."
                            value={inputText}
                            onChange={(e) => {
                                setInputText(e.target.value)
                                setFiles([])
                            }}
                        />
                    </div>
                </div>

                <div className={`mt-8 flex justify-end transition-all duration-700 delay-300 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
                    <MagneticButton
                        size="lg"
                        variant="primary"
                        onClick={handleSubmit}
                    >
                        {isLoading ? "Analyzing..." : `Start Analysis (${files.length > 0 ? files.length + ' files' : 'Text'})`}
                    </MagneticButton>
                </div>
            </div>
        </section>
    )
}
