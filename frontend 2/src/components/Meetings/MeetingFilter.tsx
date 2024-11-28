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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface MeetingFilterProps {
    startDate: string;
    endDate: string;
    setStartDate: React.Dispatch<React.SetStateAction<string>>;
    setEndDate: React.Dispatch<React.SetStateAction<string>>;
    handleResetFilters: () => void;
    selectedState: string;
    setSelectedState: React.Dispatch<React.SetStateAction<string>>;
}

const MeetingFilter: React.FC<MeetingFilterProps> = ({
                                                         startDate,
                                                         endDate,
                                                         setStartDate,
                                                         setEndDate,
                                                         handleResetFilters,
                                                         selectedState,
                                                         setSelectedState
                                                     }) => {
    const handleStartDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newStartDate = e.target.value;
        const end = new Date(endDate).getTime();
        const start = new Date(newStartDate).getTime();

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

        if (end < start + 3600000) {
            alert("Дата конца должна быть как минимум на час позже даты начала.");
            return;
        }
        setEndDate(newEndDate);
    };

    const handleStatusChange = (value: string) => {
        setSelectedState(value);
    };

    return (
        <Dialog>
            <DialogTrigger asChild className="mb-5">
                <Button variant="default">Фильтры</Button>
            </DialogTrigger>
            <DialogContent className="w-max rounded-xl">
                <DialogHeader>
                    <DialogTitle>Фильтры</DialogTitle>
                </DialogHeader>
                <DialogDescription className="flex flex-col gap-4">
                    <div>
                        <label
                            className="block text-sm font-medium mb-1 text-start"
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
                            className="block text-sm font-medium mb-1 text-start"
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
                    <div>
                        <label
                            className="block text-sm font-medium mb-1 text-start"
                            htmlFor="stateFilter"
                        >
                            Статус
                        </label>
                        <Select
                            value={selectedState}
                            onValueChange={handleStatusChange}
                        >
                            <SelectTrigger id="stateFilter">
                                <SelectValue placeholder="Выберите статус" />
                            </SelectTrigger>
                            <SelectContent>
                                {/*<SelectItem value="">Не выбрано</SelectItem>*/}
                                <SelectItem value="booked">Забронированные</SelectItem>
                                <SelectItem value="started">Начатые</SelectItem>
                                <SelectItem value="ended">Законченные</SelectItem>
                                <SelectItem value="cancelled">Отмененные</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="flex justify-between gap-2">
                        <Button
                            variant="outline"
                            onClick={handleResetFilters}
                            className="flex-1"
                        >
                            Сбросить
                        </Button>
                    </div>
                </DialogDescription>
            </DialogContent>
        </Dialog>
    );
};

export default MeetingFilter;
