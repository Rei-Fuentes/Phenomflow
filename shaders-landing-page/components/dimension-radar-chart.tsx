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
    data: any[]
}

export function DimensionRadarChart({ data }: DimensionRadarChartProps) {
    // Transform data for Radar Chart
    // We need to normalize data so each dimension is an axis
    // and each phase is a series (or we can just show one phase at a time, or average)

    // Let's create a dataset where axes are dimensions
    const allDimensions = new Set<string>()
    data.forEach(config => {
        Object.keys(config.active_dimensions || {}).forEach(dim => allDimensions.add(dim))
    })

    const dimensions = Array.from(allDimensions)

    // For simplicity and readability, let's chart the FIRST 3 phases max, or it gets messy
    const phases = data.slice(0, 3)

    const chartData = dimensions.map(dim => {
        const entry: any = { subject: dim, fullMark: 10 }
        phases.forEach(phase => {
            entry[phase.phase_name] = phase.active_dimensions?.[dim]?.intensity || 0
        })
        return entry
    })

    const colors = ["#e19136", "#36e1d6", "#e1365b", "#8884d8"]

    return (
        <div className="w-full h-[400px] bg-foreground/5 rounded-lg p-4">
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                    <PolarGrid stroke="#ffffff30" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#ffffff80', fontSize: 12 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 10]} tick={false} axisLine={false} />

                    {phases.map((phase, index) => (
                        <Radar
                            key={phase.phase_name}
                            name={phase.phase_name}
                            dataKey={phase.phase_name}
                            stroke={colors[index % colors.length]}
                            fill={colors[index % colors.length]}
                            fillOpacity={0.3}
                        />
                    ))}

                    <Legend wrapperStyle={{ color: '#fff' }} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#000', border: '1px solid #333' }}
                        itemStyle={{ color: '#fff' }}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    )
}
