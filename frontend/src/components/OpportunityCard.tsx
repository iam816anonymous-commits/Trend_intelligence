import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function OpportunityCard({ opportunity }: { opportunity: any }) {
  return (
    <Card className="border-primary/20 bg-primary/5">
      <CardHeader>
        <CardTitle>{opportunity.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm mb-4">{opportunity.description}</p>
        <div className="flex justify-between items-center">
          <span className="text-xs font-semibold px-2 py-1 bg-green-100 text-green-800 rounded">
            Score: {opportunity.evidence_score}
          </span>
          <span className="text-xs text-muted-foreground">
            Est. Cost: ₹{opportunity.launch_cost_est.toLocaleString()}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
