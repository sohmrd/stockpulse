"use client";

import {
  Area,
  AreaChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { OHLCVDataPoint } from "@/types";
import { formatCurrency } from "@/lib/utils";

interface PriceChartProps {
  data: OHLCVDataPoint[];
  isPositive: boolean;
}

interface TooltipPayload {
  value: number;
  payload: { date: string };
}

function CustomTooltip({ active, payload }: { active?: boolean; payload?: TooltipPayload[] }) {
  if (!active || !payload?.length) return null;
  const item = payload[0];
  if (!item) return null;
  return (
    <div className="rounded-lg border border-border bg-background px-3 py-2 shadow-md text-sm">
      <p className="text-muted-foreground">{item.payload.date}</p>
      <p className="font-semibold">{formatCurrency(item.value)}</p>
    </div>
  );
}

export default function PriceChart({ data, isPositive }: PriceChartProps) {
  if (data.length === 0) {
    return (
      <div className="flex h-[400px] items-center justify-center">
        <p className="text-sm text-muted-foreground">No chart data available</p>
      </div>
    );
  }

  const color = isPositive ? "#22c55e" : "#ef4444";

  const chartData = data.map((d) => ({
    date: new Date(d.timestamp).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    close: d.close,
  }));

  const prices = data.map((d) => d.close);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const padding = (maxPrice - minPrice) * 0.05 || 1;

  // Show fewer x-axis labels for readability
  const tickInterval = Math.max(1, Math.floor(chartData.length / 6));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <AreaChart data={chartData} margin={{ top: 4, right: 4, left: 8, bottom: 0 }}>
        <defs>
          <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={color} stopOpacity={0.15} />
            <stop offset="95%" stopColor={color} stopOpacity={0} />
          </linearGradient>
        </defs>
        <XAxis
          dataKey="date"
          tick={{ fontSize: 11, fill: "#94a3b8" }}
          axisLine={false}
          tickLine={false}
          interval={tickInterval}
        />
        <YAxis
          domain={[minPrice - padding, maxPrice + padding]}
          tick={{ fontSize: 11, fill: "#94a3b8" }}
          axisLine={false}
          tickLine={false}
          tickFormatter={(v: number) => `$${v.toFixed(0)}`}
          width={55}
        />
        <Tooltip content={<CustomTooltip />} />
        <Area
          type="monotone"
          dataKey="close"
          stroke={color}
          strokeWidth={2}
          fill="url(#colorGradient)"
          dot={false}
          activeDot={{ r: 4, fill: color }}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
