import { User, Inbox } from "lucide-react"

import {
    Sidebar,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "./ui/sidebar.tsx"
import {ModeToggle} from "./mode-toggle.tsx";
import {Link, useLocation} from "react-router";

const items = [
    {
        title: "Все мероприятия",
        url: "/events",
        icon: Inbox,
    },
    {
        title: "Профиль",
        url: "/profile",
        icon: User,
    },
]

export function AppSidebar() {
    const location = useLocation();

    return (
        <Sidebar>
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel>Меню</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {items.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton asChild>
                                        <Link
                                            to={item.url}
                                            onClick={(e) => {
                                                if (location.pathname === item.url) {
                                                    e.preventDefault();
                                                }
                                            }}
                                        >
                                            <item.icon />
                                            <span>{item.title}</span>
                                        </Link>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                            <ModeToggle />
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
        </Sidebar>
    );
}
