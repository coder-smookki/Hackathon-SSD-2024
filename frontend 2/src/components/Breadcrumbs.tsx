import React from 'react';
import {useLocation} from "react-router";
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbSeparator
} from "@/components/ui/breadcrumb.tsx";

const Breadcrumbs: React.FC = () => {
    const location = useLocation();
    const currentLink: string[] = [];
    console.log(location.pathname.split("/"))

    const crumbs = location.pathname.split("/")
        .filter(crumb => crumb !== '')
        .map(crumb => {
            currentLink.push(`/${crumb}`)

            return (
                <BreadcrumbItem className="hidden md:block" key={crumb}>
                    <BreadcrumbLink href={currentLink.join('')}>
                        {crumb}
                    </BreadcrumbLink>
                </BreadcrumbItem>
            )
        })
    return (
        <Breadcrumb>
            <BreadcrumbList>
                {crumbs}
                <BreadcrumbSeparator className="hidden md:block"/>
            </BreadcrumbList>
        </Breadcrumb>
    );
};

export default Breadcrumbs;