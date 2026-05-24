"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import TrendChart from "@/components/TrendChart";
import LiveSignals from "@/components/LiveSignals";

export default function Home() {
  const [trends, setTrends] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/trends`)
      .then((res) => res.json())
      .then((data) => setTrends(data));
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-12">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-black tracking-tight text-slate-900">Intelligence Overview</h1>
          <p className="text-slate-500 font-medium italic mt-1">Cross-signal market detection active.</p>
        </div>
        <div className="text-right">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">System Status</p>
          <div className="flex items-center gap-2 text-green-500 font-bold">
            <div className="size-2 bg-green-500 rounded-full animate-pulse" />
            Live Ingestion
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <section className="lg:col-span-2 space-y-6">
          <h2 className="text-xl font-bold border-l-4 border-primary pl-4">Top Rising Trends</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {trends.slice(0, 4).map((trend: any) => (
              <Card key={trend.id} className="overflow-hidden border-none shadow-sm bg-white hover:ring-1 ring-primary/20 transition-all">
                <CardHeader className="pb-2">
                  <CardTitle className="text-md line-clamp-1">{trend.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-black text-slate-800">{Math.round(trend.trend_score)}%</p>
                  <TrendChart />
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-xl font-bold border-l-4 border-slate-400 pl-4">Real-time Signals</h2>
          <LiveSignals />
        </section>
      </div>
    </div>
  );
}
