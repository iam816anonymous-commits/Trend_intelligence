"use client";

import { useEffect, useState } from "react";
import OpportunityCard from "@/components/OpportunityCard";

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/opportunities`)
      .then((res) => res.json())
      .then((data) => setOpportunities(data));
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Opportunity Finder</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {opportunities.map((opp: any) => (
          <OpportunityCard key={opp.id} opportunity={opp} />
        ))}
      </div>
    </div>
  );
}
