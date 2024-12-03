import React from 'react';
import {Card, CardContent, CardHeader, CardTitle} from "../ui/card.tsx";

interface SkeletonProps {
    index: number;
}

const Skeleton: React.FC<SkeletonProps> = ({index}) => {
    return (
        <Card key={index} className="animate-pulse">
            <CardHeader>
                <CardTitle className="h-6 bg-gray-200 rounded"></CardTitle>
            </CardHeader>
            <CardContent>
                <div className="h-4 bg-gray-200 rounded mb-2"></div>
                <div className="h-4 bg-gray-200 rounded"></div>
            </CardContent>
        </Card>
    );
};

export default Skeleton;