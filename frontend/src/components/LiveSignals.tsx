"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function LiveSignals() {
  const [signals, setSignals] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/signals?limit=20`)
      .then((res) => res.json())
      .then((data) => setSignals(data));
  }, []);

  return (
    <ScrollArea className="h-[400px] rounded-md border p-4 bg-white shadow-inner">
      <div className="space-y-4">
        {signals.map((s: any) => (
          <div key={s.id} className="flex flex-col gap-1 border-b pb-2 last:border-0">
            <div className="flex justify-between items-center">
              <span className="text-[10px] font-mono text-muted-foreground">{new Date(s.timestamp).toLocaleTimeString()}</span>
              <Badge variant="outline" className="text-[9px] uppercase">{s.source}</Badge>
            </div>
            <p className="text-sm font-medium">{s.title}</p>
            <span className="text-[10px] text-primary">{s.region}</span>
          </div>
        ))}
      </div>
    </ScrollArea>
  );
}
