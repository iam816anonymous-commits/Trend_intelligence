"use client";

import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Search, Loader2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: any) => {
    if (e.key === "Enter" && query) {
      setLoading(true);
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/search?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        setResults(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 size-5" />
        <Input
          className="pl-12 h-14 text-lg rounded-xl shadow-sm border-slate-200"
          placeholder="Search semantic memory for signals or topics..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleSearch}
        />
        {loading && <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 animate-spin text-primary size-5" />}
      </div>

      <div className="space-y-4">
        {results.map((res: any, idx: number) => (
          <Card key={idx} className="border-none shadow-sm">
            <CardHeader className="flex flex-row justify-between items-center pb-2">
              <CardTitle className="text-sm font-bold">{res.payload.title || res.payload.name}</CardTitle>
              <Badge variant="outline">{Math.round(res.score * 100)}% Match</Badge>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground uppercase font-bold tracking-tighter">
                {res.payload.type || "signal"} • ID: {res.id}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
