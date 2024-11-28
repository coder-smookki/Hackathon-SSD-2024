import React, { useEffect, useState } from "react";
import { IMeeting } from "@/types/Meetings.ts";
import MeetingCard from "@/components/Meetings/MeetingCard.tsx";
import Pagination from "@/components/Meetings/Pagination.tsx";
import Skeleton from "@/components/Meetings/Skeleton.tsx";
import SidebarLayout from "@/layout.tsx";
import MeetingService from "@/services/MeetingService.ts";
import MeetingFilter from "@/components/Meetings/MeetingFilter.tsx";

const MeetingsPage: React.FC = () => {
    const [meetings, setMeetings] = useState<IMeeting[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [totalPages, setTotalPages] = useState(1);

    // Фильтры
    const initialStartDate = "2022-11-14T00:23:09";
    const initialEndDate = "2024-11-14T20:23:09";

    const [startDate, setStartDate] = useState<string>(initialStartDate);
    const [endDate, setEndDate] = useState<string>(initialEndDate);
    const [state, setState] = useState<string>("");

    // Загрузка данных
    useEffect(() => {
        const fetchMeetingsData = async () => {
            setLoading(true);
            setError(null);

            try {
                const data = await MeetingService.fetchMeetings(
                    page,
                    rowsPerPage,
                    startDate,
                    endDate,
                    state,
                );
                let fetched_meetings = data.data.data;

                if (state != "") {
                    fetched_meetings = data.data.data.filter(meeting => meeting.state === state);
                }

                setMeetings(fetched_meetings);

                const newTotalPages = Math.ceil(data.data.rowsNumber / rowsPerPage);
                setTotalPages(newTotalPages);

                // Если текущая страница выходит за пределы общего количества страниц
                if (page > newTotalPages) {
                    setPage(newTotalPages);
                }
            } catch (err) {
                console.error(err);
                setError("Не удалось загрузить мероприятия");
                setState("");
                setPage(1);
            } finally {
                setLoading(false);
                console.log(meetings)
            }
        };

        fetchMeetingsData();
    }, [page, rowsPerPage, startDate, endDate, state]);

    const handleResetFilters = () => {
        setStartDate(initialStartDate);
        setEndDate(initialEndDate);
        setState("")
        setPage(1);
    };

    const header = (
        <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-10 text-center">
            Мероприятия
        </h1>
    );

    const skeletons = (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({length: rowsPerPage}).map((_, index) => (
                <Skeleton key={index} index={index}/>
            ))}
        </div>
    );

    const errorMessage = <p className="text-center text-red-500">{error}</p>;

    const meetingsGrid = (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {meetings.map((meeting) => (
                <MeetingCard key={meeting.id} meeting={meeting}/>
            ))}
        </div>
    );

    const noMeetingsMessage = (
        <p className="text-center text-lg">Мероприятия отсутствуют</p>
    );

    const pagination = (
        <Pagination
            page={page}
            totalPages={totalPages}
            rowsPerPage={rowsPerPage}
            onNext={() => setPage(page + 1)}
            onPrev={() => setPage(page - 1)}
            onRowsChange={setRowsPerPage}
        />
    );

    return (
        <SidebarLayout>
            <div className="p-10 flex flex-col">
                {header}
                <MeetingFilter
                    startDate={startDate}
                    endDate={endDate}
                    setStartDate={setStartDate}
                    setEndDate={setEndDate}
                    handleResetFilters={handleResetFilters}
                    selectedState={state}
                    setSelectedState={setState}
                />
                {loading && skeletons}
                {error && errorMessage}
                {!loading && !error && meetings.length > 0 && (
                    <>
                        {meetingsGrid}
                        {pagination}
                    </>
                )}
                {!loading && !error && meetings.length === 0 && noMeetingsMessage}
            </div>
        </SidebarLayout>
    );
};

export default MeetingsPage;
