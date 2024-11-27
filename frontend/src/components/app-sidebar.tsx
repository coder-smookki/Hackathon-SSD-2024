import {User, CalendarPlus, CalendarDays, CalendarHeart, LogOut} from "lucide-react"
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
        url: "/meetings",
        icon: CalendarDays,
    },
    {
        title: "Создать мероприятие",
        url: "/create-meeting",
        icon: CalendarPlus,
    },
    {
        title: "Мои мероприятия",
        url: "/my-meetings",
        icon: CalendarHeart,
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
                        <SidebarMenu className="gap-5">
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
                            <SidebarMenuItem>
                                <SidebarMenuButton asChild>
                                    <Link
                                        to={"/login"}
                                        onClick={(e) => {
                                            localStorage.removeItem("token")
                                            localStorage.removeItem("refreshToken")
                                            if (location.pathname === "/login") {
                                                e.preventDefault();
                                            }
                                        }}
                                    >
                                        <LogOut />
                                        <span>Выйти</span>
                                    </Link>
                                </SidebarMenuButton>
                            </SidebarMenuItem>
                            <ModeToggle />
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
        </Sidebar>
    );
}
