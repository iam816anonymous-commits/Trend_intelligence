"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import OpportunityCard from "@/components/OpportunityCard";

export default function Home() {
  const [trends, setTrends] = useState([]);
  const [opportunities, setOpportunities] = useState([]);

  useEffect(() => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    fetch(`${apiBase}/trends`)
      .then((res) => res.json())
      .then((data) => setTrends(data))
      .catch(err => console.error(err));

    fetch(`${apiBase}/opportunities`)
      .then((res) => res.json())
      .then((data) => setOpportunities(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-8 font-sans max-w-7xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-extrabold tracking-tight mb-2">TrendPulse AI</h1>
        <p className="text-muted-foreground italic">India's Predictive Market Intelligence OS</p>
      </header>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Hot Trends</h2>
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
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Opportunity Finder</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {opportunities.map((opp: any, idx) => (
            <OpportunityCard key={idx} opportunity={opp} />
          ))}
        </div>
      </section>
    </div>
  );
}
