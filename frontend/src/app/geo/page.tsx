"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function GeoPage() {
  const [geoData, setGeoData] = useState<any>({});

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/geo/pulse`)
      .then((res) => res.json())
      .then((data) => setGeoData(data));
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Geo Pulse: Tier-2/3 India</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Object.entries(geoData).map(([city, stats]: [string, any]) => (
          <Card key={city}>
            <CardHeader>
              <CardTitle>{city}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold mb-2">{stats.pulse_score}</p>
              <div className="flex flex-wrap gap-2 mt-4">
                {stats.top_categories.map((cat: string) => (
                  <span key={cat} className="text-[10px] px-2 py-0.5 bg-secondary rounded uppercase">
                    {cat}
                  </span>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
