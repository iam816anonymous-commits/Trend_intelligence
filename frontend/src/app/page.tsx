"use client";

import TrendDataTable from "@/components/TrendDataTable";
import LiveSignals from "@/components/LiveSignals";

export default function Home() {
  return (
    <div className="p-8 max-w-7xl mx-auto space-y-12">
      <header className="flex justify-between items-center bg-white p-6 rounded-2xl border shadow-sm border-slate-100">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 flex items-center gap-3">
            Market Intelligence OS
            <span className="text-[10px] px-2 py-0.5 bg-primary text-primary-foreground rounded uppercase font-black tracking-widest">Enterprise</span>
          </h1>
          <p className="text-slate-500 font-medium mt-1">Cross-signal predictive monitoring for India Tier-1/2/3.</p>
        </div>
        <div className="flex gap-4">
          <div className="text-right px-4 border-r">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Global Pulse</p>
            <p className="text-xl font-black text-slate-800">84.2</p>
          </div>
          <div className="text-right">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Signals Ingested</p>
            <p className="text-xl font-black text-blue-600">1.2M+</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <section className="lg:col-span-3 space-y-6">
          <div className="flex justify-between items-end">
            <h2 className="text-xl font-bold text-slate-800">Active Trends & Sentiment</h2>
            <p className="text-xs text-blue-500 font-bold hover:underline cursor-pointer uppercase tracking-wider">Export PDF Report</p>
          </div>
          <TrendDataTable />
        </section>

        <section className="space-y-6">
          <h2 className="text-xl font-bold text-slate-800">Signal Velocity</h2>
          <div className="bg-white rounded-2xl border shadow-sm p-1">
             <LiveSignals />
          </div>
        </section>
      </div>
    </div>
  );
}
