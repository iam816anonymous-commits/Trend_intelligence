"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import TrendChart from "@/components/TrendChart";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";

export default function TrendsPage() {
  const [trends, setTrends] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/trends`)
      .then((res) => res.json())
      .then((data) => setTrends(data));
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <h1 className="text-3xl font-black">Emerging Trends</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {trends.map((trend: any) => (
          <Dialog key={trend.id}>
            <DialogTrigger className="text-left w-full">
              <Card className="cursor-pointer hover:ring-2 ring-primary/20 transition-all border-none shadow-sm h-full">
                <CardHeader className="pb-2 flex flex-row justify-between items-center">
                  <CardTitle className="text-md line-clamp-1">{trend.name}</CardTitle>
                  <Badge variant="secondary">{trend.status}</Badge>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-black text-slate-800">{Math.round(trend.trend_score)}%</p>
                  <TrendChart />
                </CardContent>
              </Card>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>{trend.name}</DialogTitle>
                <div className="flex gap-2 mt-2">
                  <Badge>{trend.status}</Badge>
                  <Badge variant="outline">Confidence: {Math.round(trend.confidence * 100)}%</Badge>
                </div>
              </DialogHeader>
              <div className="py-4 space-y-6">
                <div>
                  <h4 className="text-sm font-bold text-slate-500 uppercase tracking-widest mb-2">Trend History</h4>
                  <div className="h-[200px]">
                    <TrendChart />
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-500 uppercase tracking-widest mb-2">Analysis</h4>
                  <p className="text-sm leading-relaxed text-slate-700">
                    This trend shows a sustained velocity across multiple sources. High signal density in Tier-2 regions suggests a shifting consumer preference.
                  </p>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        ))}
      </div>
    </div>
  );
}
