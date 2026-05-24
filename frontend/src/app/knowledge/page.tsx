"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Brain, Zap, History } from "lucide-react";

export default function KnowledgePage() {
  const [knowledge, setKnowledge] = useState([]);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiBase}/api/v1/knowledge`)
      .then((res) => res.json())
      .then((data) => setKnowledge(data));

    fetch(`${apiBase}/api/v1/learning-logs`)
      .then((res) => res.json())
      .then((data) => setLogs(data));
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-12">
      <header className="flex items-center gap-4">
        <div className="bg-primary/10 p-3 rounded-2xl">
            <Brain className="size-8 text-primary" />
        </div>
        <div>
          <h1 className="text-3xl font-black tracking-tight text-slate-900">Agent Knowledge Base</h1>
          <p className="text-slate-500 font-medium">Autonomous taxonomy expansion and concept learning.</p>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <section className="lg:col-span-2 space-y-6">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <Zap className="size-5 text-yellow-500" /> Learned Concepts
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {knowledge.map((item: any) => (
              <Card key={item.id} className="border-none shadow-sm bg-white">
                <CardHeader className="pb-2">
                  <Badge variant="secondary" className="w-fit mb-2">{item.category}</Badge>
                  <CardTitle className="text-lg">{item.concept}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{item.definition}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <History className="size-5 text-blue-500" /> Brain Activity
          </h2>
          <ScrollArea className="h-[500px] rounded-xl border bg-white p-4">
            <div className="space-y-6">
              {logs.map((log: any) => (
                <div key={log.id} className="relative pl-6 border-l-2 border-slate-100 pb-2">
                  <div className="absolute -left-[9px] top-0 size-4 bg-white border-2 border-primary rounded-full" />
                  <p className="text-[10px] font-bold text-slate-400 uppercase">{new Date(log.timestamp).toLocaleString()}</p>
                  <p className="text-sm font-bold text-slate-800 mt-1">{log.action}</p>
                  <Badge variant="outline" className="text-[9px] mt-2">{log.impact_area}</Badge>
                </div>
              ))}
            </div>
          </ScrollArea>
        </section>
      </div>
    </div>
  );
}
