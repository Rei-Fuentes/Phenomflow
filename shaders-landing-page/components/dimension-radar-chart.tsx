"use client"

import {
    Radar,
    RadarChart,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    ResponsiveContainer,
    Legend,
    Tooltip
} from "recharts"

interface DimensionRadarChartProps {
    data: {
        [dimension: string]: {
            coverage_percentage: number
            dominant_codes: string[]
        }
    }
}

export function DimensionRadarChart({ data }: DimensionRadarChartProps) {
    if (!data || Object.keys(data).length === 0) {
        return (
            <div className="w-full h-[400px] bg-foreground/5 rounded-lg p-4 flex items-center justify-center">
                <p className="text-foreground/40 text-sm">No dimension data available</p>
            </div>
        )
    }

    // Transformar datos para el radar
    // Formato: [{ subject: "CORPORAL", coverage: 85, fullMark: 100 }, ...]
    const chartData = Object.entries(data).map(([dimension, info]) => ({
        subject: dimension,
        coverage: info.coverage_percentage,
        fullMark: 100
    }))

    // Custom label para mostrar porcentaje
    const renderPolarAngleAxis = ({ payload, x, y, cx, cy, ...rest }: any) => {
        return (
            <text
                {...rest}
                x={x}
                y={y}
                className="fill-foreground/80"
                fontSize={12}
                fontFamily="monospace"
                textAnchor={x > cx ? 'start' : 'end'}
            >
                {payload.value}
            </text>
        )
    }

    return (
        <div className="w-full h-[400px] bg-foreground/5 rounded-lg p-4">
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="70%" data={chartData}>
                    <PolarGrid stroke="#ffffff20" />

                    <PolarAngleAxis
                        dataKey="subject"
                        tick={renderPolarAngleAxis}
                    />

                    <PolarRadiusAxis
                        angle={30}
                        domain={[0, 100]}
                        tick={{ fill: '#ffffff40', fontSize: 10 }}
                        axisLine={false}
                    />

                    <Radar
                        name="Cobertura (%)"
                        dataKey="coverage"
                        stroke="#e19136"
                        fill="#e19136"
                        fillOpacity={0.5}
                        strokeWidth={2}
                    />

                    <Legend
                        wrapperStyle={{
                            color: '#fff',
                            fontSize: '12px',
                            fontFamily: 'monospace'
                        }}
                    />

                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#000',
                            border: '1px solid #333',
                            borderRadius: '8px',
                            fontFamily: 'monospace',
                            fontSize: '12px'
                        }}
                        itemStyle={{ color: '#e19136' }}
                        labelStyle={{ color: '#fff', fontWeight: 'bold' }}
                        formatter={(value: number) => [`${value}%`, 'Cobertura']}
                    />
                </RadarChart>
            </ResponsiveContainer>

            {/* Leyenda de códigos dominantes */}
            <div className="mt-4 space-y-2 max-h-32 overflow-y-auto custom-scrollbar">
                {Object.entries(data).map(([dim, info]) => (
                    <div key={dim} className="text-xs">
                        <span className="font-mono text-foreground/70">{dim}:</span>
                        <span className="text-foreground/50 ml-2">
                            {info.dominant_codes.slice(0, 2).join(", ")}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    )
}