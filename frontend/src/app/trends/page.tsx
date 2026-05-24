"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import TrendChart from "@/components/TrendChart";

export default function TrendsPage() {
  const [trends, setTrends] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/trends`)
      .then((res) => res.json())
      .then((data) => setTrends(data));
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Emerging Trends</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {trends.map((trend: any) => (
          <Card key={trend.id}>
            <CardHeader>
              <CardTitle className="flex justify-between">
                <span>{trend.name}</span>
                <span className="text-xs px-2 py-1 bg-primary/10 rounded">{trend.status}</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{Math.round(trend.trend_score)}%</p>
              <TrendChart />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
