"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Home() {
  const [trends, setTrends] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/trends`)
      .then((res) => res.json())
      .then((data) => setTrends(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-8 font-sans">
      <h1 className="text-3xl font-bold mb-8">India Trend Intelligence</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {trends.map((trend: any, idx) => (
          <Card key={idx}>
            <CardHeader>
              <CardTitle className="capitalize">{trend.trend}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{trend.growth}</div>
              <p className="text-sm text-muted-foreground">Strength: {trend.strength}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
