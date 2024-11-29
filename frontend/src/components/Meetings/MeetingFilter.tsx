import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription, DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger
} from "@/components/ui/dialog.tsx";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {Label} from "@/components/ui/label.tsx";

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
    const [tempStartDate, setTempStartDate] = useState(startDate);
    const [tempEndDate, setTempEndDate] = useState(endDate);
    const [tempSelectedState, setTempSelectedState] = useState(selectedState);

    const handleStartDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTempStartDate(e.target.value);
    };

    const handleEndDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTempEndDate(e.target.value);
    };

    const handleStatusChange = (value: string) => {
        setTempSelectedState(value);
    };

    const handleApplyFilters = () => {
        const start = new Date(tempStartDate).getTime();
        const end = new Date(tempEndDate).getTime();

        // Проверка на корректность дат
        if (start + 3600000 > end) {
            alert("Дата начала должна быть как минимум на час раньше даты конца.");
            return;
        }
        if (end < start + 3600000) {
            alert("Дата конца должна быть как минимум на час позже даты начала.");
            return;
        }

        // Применяем фильтры
        setStartDate(tempStartDate);
        setEndDate(tempEndDate);
        setSelectedState(tempSelectedState);
    };

    return (
        <Dialog>
            <DialogTrigger asChild className="mb-5">
                <Button variant="default">Фильтры</Button>
            </DialogTrigger>
            <DialogContent className="w-[75vw] max-w-[450px] rounded-xl">
                <DialogHeader>
                    <DialogTitle>Фильтры</DialogTitle>
                    <DialogDescription>
                        Выберите подходящие параметры
                    </DialogDescription>
                </DialogHeader>
                <div className="flex flex-col gap-4">
                    <div>
                        <Label
                            className="block text-sm font-medium mb-1 text-start"
                            htmlFor="startDate"
                        >
                            Начало
                        </Label>
                        <Input
                            id="startDate"
                            type="datetime-local"
                            value={tempStartDate}
                            onChange={handleStartDateChange}
                        />
                    </div>
                    <div>
                        <Label
                            className="block text-sm font-medium mb-1 text-start"
                            htmlFor="endDate"
                        >
                            Конец
                        </Label>
                        <Input
                            id="endDate"
                            type="datetime-local"
                            value={tempEndDate}
                            onChange={handleEndDateChange}
                        />
                    </div>
                    <div>
                        <Label
                            className="block text-sm font-medium mb-1 text-start"
                            htmlFor="stateFilter"
                        >
                            Статус
                        </Label>
                        <Select
                            value={tempSelectedState}
                            onValueChange={handleStatusChange}
                        >
                            <SelectTrigger id="stateFilter">
                                <SelectValue placeholder="Выберите статус" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="booked">Забронированные</SelectItem>
                                <SelectItem value="started">Начатые</SelectItem>
                                <SelectItem value="ended">Законченные</SelectItem>
                                <SelectItem value="cancelled">Отмененные</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </div>
                <DialogFooter className="flex flex-row justify-between gap-2">
                    <Button
                        variant="outline"
                        onClick={handleResetFilters}
                        className="flex-1"
                    >
                        Сбросить
                    </Button>
                    <Button
                        variant="default"
                        onClick={handleApplyFilters}
                        className="flex-1"
                    >
                        Применить
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};

export default MeetingFilter;
