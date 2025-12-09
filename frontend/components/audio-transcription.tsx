"use client"

import { useState, useRef } from "react"
import { Upload, FileAudio, CheckCircle, AlertCircle, Download, Loader2, Mic } from "lucide-react"
import { MagneticButton } from "@/components/magnetic-button"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface AudioFile {
    file: File
    status: 'pending' | 'transcribing' | 'completed' | 'error'
    transcription?: string
    error?: string
    duration?: number
}

interface AudioTranscriptionProps {
    t: any
    onTranscriptionComplete?: (transcriptions: { filename: string; text: string }[]) => void
}

export function AudioTranscription({ t, onTranscriptionComplete }: AudioTranscriptionProps) {
    const [audioFiles, setAudioFiles] = useState<AudioFile[]>([])
    const [dragActive, setDragActive] = useState(false)
    const [isTranscribing, setIsTranscribing] = useState(false)
    const [progress, setProgress] = useState(0)
    const fileInputRef = useRef<HTMLInputElement>(null)

    const SUPPORTED_FORMATS = [
        'mp3', 'wav', 'ogg', 'm4a', 'flac', 'aac', 'wma', 'webm'
    ]

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
            return ext && SUPPORTED_FORMATS.includes(ext)
        })

        if (validFiles.length !== newFiles.length) {
            alert(t.transcription?.invalidFormat || "Some files were skipped. Only audio files are supported.")
        }

        const audioFileObjects: AudioFile[] = validFiles.map(file => ({
            file,
            status: 'pending'
        }))

        setAudioFiles(prev => [...prev, ...audioFileObjects])
    }

    const removeFile = (index: number) => {
        setAudioFiles(prev => prev.filter((_, i) => i !== index))
    }

    const transcribeAll = async () => {
        setIsTranscribing(true)
        setProgress(0)

        const formData = new FormData()
        audioFiles.forEach(({ file }) => {
            formData.append('files', file)
        })
        formData.append('language', 'es')
        formData.append('model_size', 'base')

        try {
            const response = await fetch('http://localhost:8000/transcribe', {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

            const data = await response.json()

            // Update audio files with transcriptions
            setAudioFiles(prev => prev.map((audioFile, index) => ({
                ...audioFile,
                status: 'completed',
                transcription: data.transcriptions[index]?.text || '',
                duration: data.transcriptions[index]?.duration
            })))

            setProgress(100)

            // Notify parent component
            if (onTranscriptionComplete) {
                const transcriptions = data.transcriptions.map((t: any) => ({
                    filename: t.filename,
                    text: t.text
                }))
                onTranscriptionComplete(transcriptions)
            }

        } catch (error) {
            console.error('Transcription error:', error)
            setAudioFiles(prev => prev.map(audioFile => ({
                ...audioFile,
                status: 'error',
                error: error instanceof Error ? error.message : 'Unknown error'
            })))
        } finally {
            setIsTranscribing(false)
        }
    }

    const downloadTranscription = (audioFile: AudioFile, format: 'txt' | 'pdf' | 'docx') => {
        if (!audioFile.transcription) return

        const filename = audioFile.file.name.replace(/\.[^/.]+$/, "")

        if (format === 'txt') {
            // Download as TXT
            const blob = new Blob([audioFile.transcription], { type: 'text/plain' })
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `${filename}_transcription.txt`
            a.click()
            URL.revokeObjectURL(url)
        } else if (format === 'pdf') {
            // For PDF, we need to use a library or backend endpoint
            // For now, we'll create a simple text file
            // TODO: Implement proper PDF generation
            alert('PDF generation coming soon! Using TXT for now.')
            downloadTranscription(audioFile, 'txt')
        } else if (format === 'docx') {
            // For DOCX, we need to use a library or backend endpoint
            // TODO: Implement proper DOCX generation
            alert('DOCX generation coming soon! Using TXT for now.')
            downloadTranscription(audioFile, 'txt')
        }
    }

    const downloadAllTranscriptions = () => {
        const completedFiles = audioFiles.filter(f => f.status === 'completed' && f.transcription)

        if (completedFiles.length === 0) return

        const combinedText = completedFiles.map((audioFile, index) => {
            return `\n${'='.repeat(80)}\nFILE ${index + 1}: ${audioFile.file.name}\n${'='.repeat(80)}\n\n${audioFile.transcription}\n`
        }).join('\n')

        const blob = new Blob([combinedText], { type: 'text/plain' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `all_transcriptions_${new Date().toISOString().split('T')[0]}.txt`
        a.click()
        URL.revokeObjectURL(url)
    }

    return (
        <div className="space-y-6">
            {/* Upload Area */}
            <div
                className={`relative border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center transition-colors min-h-[200px] ${dragActive
                        ? "border-foreground bg-foreground/10"
                        : "border-foreground/20 bg-foreground/5"
                    }`}
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
                    accept={SUPPORTED_FORMATS.map(f => `.${f}`).join(',')}
                    multiple
                />

                {audioFiles.length === 0 ? (
                    <div className="space-y-4">
                        <div className="w-16 h-16 bg-foreground/10 rounded-full flex items-center justify-center mx-auto text-foreground/60">
                            <Mic size={32} />
                        </div>
                        <div>
                            <p className="font-medium text-foreground">
                                {t.transcription?.dragDrop || "Drag & Drop Audio Files"}
                            </p>
                            <p className="text-xs text-foreground/60 mt-1">
                                {t.transcription?.supportedFormats || "Supported: MP3, WAV, M4A, FLAC, OGG, AAC"}
                            </p>
                        </div>
                        <MagneticButton
                            size="sm"
                            variant="secondary"
                            onClick={() => fileInputRef.current?.click()}
                        >
                            {t.transcription?.browseFiles || "Browse Audio Files"}
                        </MagneticButton>
                    </div>
                ) : (
                    <div className="w-full">
                        <button
                            onClick={() => fileInputRef.current?.click()}
                            className="text-xs text-foreground/60 hover:text-foreground underline"
                        >
                            + {t.transcription?.addMore || "Add more audio files"}
                        </button>
                    </div>
                )}
            </div>

            {/* Audio Files List */}
            {audioFiles.length > 0 && (
                <div className="space-y-3">
                    <div className="flex items-center justify-between">
                        <h3 className="text-sm font-medium text-foreground">
                            {t.transcription?.audioFiles || "Audio Files"} ({audioFiles.length})
                        </h3>
                        {audioFiles.some(f => f.status === 'completed') && (
                            <Button
                                size="sm"
                                variant="outline"
                                onClick={downloadAllTranscriptions}
                                className="text-xs"
                            >
                                <Download size={14} className="mr-1" />
                                {t.transcription?.downloadAll || "Download All"}
                            </Button>
                        )}
                    </div>

                    <div className="space-y-2 max-h-[400px] overflow-y-auto pr-2">
                        {audioFiles.map((audioFile, index) => (
                            <Card key={index} className="p-4">
                                <div className="flex items-start justify-between gap-3">
                                    <div className="flex items-start gap-3 flex-1 overflow-hidden">
                                        <div className="shrink-0 mt-1">
                                            {audioFile.status === 'pending' && (
                                                <FileAudio size={20} className="text-foreground/40" />
                                            )}
                                            {audioFile.status === 'transcribing' && (
                                                <Loader2 size={20} className="text-blue-500 animate-spin" />
                                            )}
                                            {audioFile.status === 'completed' && (
                                                <CheckCircle size={20} className="text-green-500" />
                                            )}
                                            {audioFile.status === 'error' && (
                                                <AlertCircle size={20} className="text-red-500" />
                                            )}
                                        </div>

                                        <div className="flex-1 overflow-hidden">
                                            <p className="font-medium text-sm text-foreground truncate">
                                                {audioFile.file.name}
                                            </p>
                                            <p className="text-xs text-foreground/60">
                                                {(audioFile.file.size / 1024 / 1024).toFixed(2)} MB
                                                {audioFile.duration && ` • ${audioFile.duration.toFixed(1)}s`}
                                            </p>

                                            {audioFile.status === 'completed' && audioFile.transcription && (
                                                <div className="mt-2 p-2 bg-foreground/5 rounded text-xs text-foreground/80 max-h-20 overflow-y-auto">
                                                    {audioFile.transcription.substring(0, 200)}
                                                    {audioFile.transcription.length > 200 && '...'}
                                                </div>
                                            )}

                                            {audioFile.status === 'error' && (
                                                <p className="mt-1 text-xs text-red-500">
                                                    {audioFile.error}
                                                </p>
                                            )}
                                        </div>
                                    </div>

                                    <div className="flex items-center gap-2 shrink-0">
                                        {audioFile.status === 'completed' && (
                                            <div className="flex gap-1">
                                                <Button
                                                    size="sm"
                                                    variant="ghost"
                                                    onClick={() => downloadTranscription(audioFile, 'txt')}
                                                    className="h-7 px-2"
                                                >
                                                    <Download size={14} />
                                                </Button>
                                            </div>
                                        )}

                                        {audioFile.status === 'pending' && (
                                            <button
                                                onClick={() => removeFile(index)}
                                                className="text-foreground/40 hover:text-red-400 transition-colors p-1"
                                            >
                                                <AlertCircle size={16} className="rotate-45" />
                                            </button>
                                        )}
                                    </div>
                                </div>
                            </Card>
                        ))}
                    </div>

                    {/* Progress Bar */}
                    {isTranscribing && (
                        <div className="space-y-2">
                            <Progress value={progress} className="h-2" />
                            <p className="text-xs text-center text-foreground/60">
                                {t.transcription?.transcribing || "Transcribing audio files..."}
                            </p>
                        </div>
                    )}

                    {/* Transcribe Button */}
                    {audioFiles.some(f => f.status === 'pending') && (
                        <MagneticButton
                            size="lg"
                            variant="primary"
                            onClick={transcribeAll}
                            disabled={isTranscribing}
                            className="w-full"
                        >
                            {isTranscribing ? (
                                <>
                                    <Loader2 size={16} className="mr-2 animate-spin" />
                                    {t.transcription?.transcribing || "Transcribing..."}
                                </>
                            ) : (
                                <>
                                    <Mic size={16} className="mr-2" />
                                    {t.transcription?.startTranscription || `Transcribe ${audioFiles.filter(f => f.status === 'pending').length} file(s)`}
                                </>
                            )}
                        </MagneticButton>
                    )}
                </div>
            )}
        </div>
    )
}
