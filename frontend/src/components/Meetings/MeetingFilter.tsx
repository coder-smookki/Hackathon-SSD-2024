import React from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger
} from "@/components/ui/dialog.tsx";

interface MeetingFilterProps {
    startDate: string;
    endDate: string;
    setStartDate: React.Dispatch<React.SetStateAction<string>>;
    setEndDate: React.Dispatch<React.SetStateAction<string>>;
    handleResetFilters: () => void;
}

const MeetingFilter: React.FC<MeetingFilterProps> = ({
                                                         startDate,
                                                         endDate,
                                                         setStartDate,
                                                         setEndDate,
                                                         handleResetFilters
                                                     }) => {
    const handleStartDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newStartDate = e.target.value;
        const end = new Date(endDate).getTime();
        const start = new Date(newStartDate).getTime();

        // Ensure start date is at least 1 hour before the end date
        if (start + 3600000 > end) {
            alert("Дата начала должна быть как минимум на час раньше даты конца.");
            return;
        }
        setStartDate(newStartDate);
    };

    const handleEndDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newEndDate = e.target.value;
        const start = new Date(startDate).getTime();
        const end = new Date(newEndDate).getTime();

        // Ensure end date is at least 1 hour after the start date
        if (end < start + 3600000) {
            alert("Дата конца должна быть как минимум на час позже даты начала.");
            return;
        }
        setEndDate(newEndDate);
    };

    return (
        <Dialog>
            <DialogTrigger className="mb-5">
                <Button>Фильтры</Button>
            </DialogTrigger>
            <DialogContent className="w-max rounded-xl">
                <DialogHeader>
                    <DialogTitle>Фильтры</DialogTitle>
                    <DialogDescription className="flex flex-col gap-4">
                        <div>
                            <label
                                className="block text-sm font-medium text-gray-700 mb-1 text-start"
                                htmlFor="startDate"
                            >
                                Начало
                            </label>
                            <Input
                                id="startDate"
                                type="datetime-local"
                                value={startDate}
                                onChange={handleStartDateChange}
                            />
                        </div>
                        <div>
                            <label
                                className="block text-sm font-medium text-gray-700 mb-1 text-start"
                                htmlFor="endDate"
                            >
                                Конец
                            </label>
                            <Input
                                id="endDate"
                                type="datetime-local"
                                value={endDate}
                                onChange={handleEndDateChange}
                            />
                        </div>
                        <div className="flex justify-between gap-2">
                            <Button variant="outline" onClick={handleResetFilters} className="flex-1">
                                Сбросить
                            </Button>
                        </div>
                    </DialogDescription>
                </DialogHeader>
            </DialogContent>
        </Dialog>
    );
};

export default MeetingFilter;
