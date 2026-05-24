"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Terminal, CheckCircle2, Loader2, AlertCircle } from "lucide-react";

export default function ActivityPage() {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const fetchActivities = () => {
        fetch(`${apiBase}/api/v1/agent-activities`)
          .then((res) => res.json())
          .then((data) => setActivities(data));
    };

    fetchActivities();
    const interval = setInterval(fetchActivities, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: string) => {
    switch(status) {
      case 'success': return <CheckCircle2 className="size-4 text-green-500" />;
      case 'thinking': return <Loader2 className="size-4 text-blue-500 animate-spin" />;
      case 'executing': return <Loader2 className="size-4 text-orange-500 animate-spin" />;
      case 'error': return <AlertCircle className="size-4 text-red-500" />;
      default: return null;
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <header className="flex items-center gap-4">
        <div className="bg-slate-900 p-3 rounded-2xl shadow-xl">
            <Terminal className="size-8 text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-black tracking-tight text-slate-900">Agent Activity Logs</h1>
          <p className="text-slate-500 font-medium">Real-time trace of autonomous system operations.</p>
        </div>
      </header>

      <ScrollArea className="h-[70vh] rounded-3xl border border-slate-200 bg-slate-950 p-6 shadow-2xl">
        <div className="space-y-4 font-mono">
          {activities.map((act: any) => (
            <div key={act.id} className="flex gap-4 items-start border-b border-slate-800 pb-4 last:border-0">
              <span className="text-[10px] text-slate-500 min-w-[80px] pt-1">
                {new Date(act.timestamp).toLocaleTimeString()}
              </span>
              <div className="pt-1">{getStatusIcon(act.status)}</div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-black text-slate-300 uppercase tracking-widest">[{act.task_name}]</span>
                    <Badge variant="outline" className="text-[8px] border-slate-700 text-slate-400 h-4">{act.status}</Badge>
                </div>
                <p className="text-sm text-slate-100 leading-relaxed">{act.message}</p>
              </div>
            </div>
          ))}
          {activities.length === 0 && (
            <div className="text-slate-500 italic text-center py-20">No activity recorded yet...</div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
