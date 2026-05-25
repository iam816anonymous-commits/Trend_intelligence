import { Sidebar, SidebarContent, SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarMenu, SidebarMenuButton, SidebarMenuItem } from "@/components/ui/sidebar";
import { LayoutDashboard, TrendingUp, Lightbulb, Map, Brain, Terminal, Settings } from "lucide-react";

const items = [
  { title: "Dashboard", icon: LayoutDashboard, url: "/dashboard" },
  { title: "Trends", icon: TrendingUp, url: "/trends" },
  { title: "Opportunities", icon: Lightbulb, url: "/opportunities" },
  { title: "Geo Pulse", icon: Map, url: "/geo" },
  { title: "Knowledge Base", icon: Brain, url: "/knowledge" },
  { title: "Agent Activity", icon: Terminal, url: "/activity" },
  { title: "Settings", icon: Settings, url: "/settings" },
];

export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="text-primary font-bold text-lg mb-4 pl-2">TrendPulse AI</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton tooltip={item.title}>
                    <a href={item.url} className="flex items-center gap-2">
                      <item.icon className="size-4" />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
