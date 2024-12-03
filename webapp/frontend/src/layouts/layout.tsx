import React from "react";
import {SidebarInset, SidebarProvider, SidebarTrigger} from "@/components/ui/sidebar.tsx";
import {AppSidebar} from "@/components/app-sidebar.tsx";
import {Separator} from "@/components/ui/separator.tsx";
import {Breadcrumb, BreadcrumbItem, BreadcrumbList, BreadcrumbPage} from "@/components/ui/breadcrumb.tsx";
import {Toaster} from "sonner";

export default function SidebarLayout({children}: { children: React.ReactNode }) {
    return (
        <SidebarProvider>
            <AppSidebar/>
            <SidebarInset>
                <header className="fixed w-full flex h-16 bg-background shrink-0 items-center gap-2 border-b px-4">
                    <SidebarTrigger className="-ml-1"/>
                    <Separator orientation="vertical" className="mr-2 h-4"/>
                    <Breadcrumb>
                        <BreadcrumbList>
                            <BreadcrumbItem>
                                <BreadcrumbPage>{location.pathname.toString().split("/")[1].toUpperCase()}</BreadcrumbPage>
                            </BreadcrumbItem>
                        </BreadcrumbList>
                    </Breadcrumb>
                </header>
                <div className="pt-16">
                    {children}
                </div>
                <Toaster/>
            </SidebarInset>
        </SidebarProvider>
    );
}