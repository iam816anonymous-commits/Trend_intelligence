import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function OpportunityCard({ opportunity }: { opportunity: any }) {
  const getBadgeVariant = (type: string) => {
    switch(type) {
      case 'D2C': return 'default';
      case 'SaaS': return 'secondary';
      default: return 'outline';
    }
  };

  return (
    <Card className="border-primary/10 shadow-sm hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-lg font-bold">{opportunity.title}</CardTitle>
        <Badge variant={getBadgeVariant(opportunity.type)}>{opportunity.type}</Badge>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground mb-6 line-clamp-3">{opportunity.description}</p>
        <div className="flex justify-between items-center text-xs">
          <div className="space-y-1">
            <p className="text-muted-foreground uppercase tracking-wider font-semibold">Evidence Score</p>
            <p className="text-base font-bold text-primary">{Math.round(opportunity.evidence_score)}%</p>
          </div>
          <div className="space-y-1 text-right">
            <p className="text-muted-foreground uppercase tracking-wider font-semibold">Launch Cost</p>
            <p className="text-base font-bold">₹{opportunity.launch_cost_est.toLocaleString()}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
