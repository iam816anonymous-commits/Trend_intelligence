"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import OpportunityCard from "@/components/OpportunityCard";

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState([]);
  const [synthesis, setSynthesis] = useState([]);

  useEffect(() => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiBase}/opportunities`)
      .then((res) => res.json())
      .then((data) => setOpportunities(data));

    fetch(`${apiBase}/synthesis`)
      .then((res) => res.json())
      .then((data) => setSynthesis(data));
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-black mb-8">Intelligence Hub</h1>

      <Tabs defaultValue="opportunities" className="space-y-8">
        <TabsList className="grid w-full grid-cols-2 max-w-[400px]">
          <TabsTrigger value="opportunities">Business Niches</TabsTrigger>
          <TabsTrigger value="synthesis">Correlation Pulse</TabsTrigger>
        </TabsList>

        <TabsContent value="opportunities">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {opportunities.map((opp: any) => (
              <OpportunityCard key={opp.id} opportunity={opp} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="synthesis">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {synthesis.map((item: any, idx: number) => (
              <Card key={idx} className="border-l-4 border-l-blue-500">
                <CardHeader>
                  <Badge className="w-fit mb-2">{item.type}</Badge>
                  <CardTitle className="text-lg">{item.topic_a} + {item.topic_b}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{item.reason}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
