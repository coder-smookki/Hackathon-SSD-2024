import React from "react";
import {Button} from "../ui/button.tsx";
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "../ui/select.tsx";

interface PaginationProps {
    page: number;
    totalPages: number;
    rowsPerPage: number;
    onNext: () => void;
    onPrev: () => void;
    onRowsChange: (value: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({ page, totalPages, rowsPerPage, onNext, onPrev, onRowsChange }) => (
    <>
        <div className="flex justify-between items-center mt-6">
            <Button onClick={onPrev} disabled={page === 1} aria-label="Предыдущая страница">
                Предыдущая
            </Button>
            <Button onClick={onNext} disabled={page === totalPages} aria-label="Следующая страница">
                Следующая
            </Button>
        </div>
        <div className={"leading-7 [&:not(:first-child)]:mt-6 text-center"}>
            <p className="text-center">
                Страница <span className="font-semibold">{page}</span> из <span
                className="font-semibold">{totalPages}</span>
            </p>
        </div>
        <div className="mt-4">
            <Select value={String(rowsPerPage)} onValueChange={(value) => onRowsChange(Number(value))}>
                <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Элементов на странице"/>
                </SelectTrigger>
                <SelectContent>
                    {[5, 10, 25, 50].map((option) => (
                        <SelectItem key={option} value={String(option)}>
                            {option}
                        </SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </div>
    </>
);

export default Pagination;
