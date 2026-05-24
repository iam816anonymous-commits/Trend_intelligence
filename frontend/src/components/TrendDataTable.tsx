"use client";

import { useEffect, useState } from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export default function TrendDataTable() {
  const [trends, setTrends] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/trends`)
      .then((res) => res.json())
      .then((data) => setTrends(data));
  }, []);

  return (
    <div className="rounded-md border bg-white shadow-sm overflow-hidden">
      <Table>
        <TableHeader className="bg-slate-50">
          <TableRow>
            <TableHead className="font-bold">Trend Name</TableHead>
            <TableHead className="font-bold text-center">Status</TableHead>
            <TableHead className="font-bold text-center text-primary">Score</TableHead>
            <TableHead className="font-bold text-right pr-6">Confidence</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {trends.map((trend: any) => (
            <TableRow key={trend.id} className="hover:bg-slate-50/50 transition-colors">
              <TableCell className="font-medium text-slate-900">{trend.name}</TableCell>
              <TableCell className="text-center">
                <Badge variant={trend.status === 'Hot' ? 'destructive' : 'secondary'} className="rounded-full px-3">
                  {trend.status}
                </Badge>
              </TableCell>
              <TableCell className="text-center font-black text-lg">{Math.round(trend.trend_score)}%</TableCell>
              <TableCell className="text-right pr-6">
                <div className="flex items-center justify-end gap-2">
                  <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-500 transition-all"
                      style={{ width: `${trend.confidence * 100}%` }}
                    />
                  </div>
                  <span className="text-[10px] text-slate-500 font-mono">{(trend.confidence * 100).toFixed(0)}%</span>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
