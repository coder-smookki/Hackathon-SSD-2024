import React from "react";
import { IMeeting } from "@/types/meetings/Meetings.ts";
import MeetingCard from "@/components/Meetings/MeetingCard.tsx";
import Pagination from "@/components/Meetings/Pagination.tsx";
import Skeleton from "@/components/Meetings/Skeleton.tsx";
import SidebarLayout from "@/layouts/MainLayout.tsx";
import MeetingFilter from "@/components/Meetings/MeetingFilter.tsx";
import TitlePage from "@/components/Base/TitlePage.tsx";
import {useMeetings} from "@/hooks/useMeetings.tsx";

const MeetingsPage: React.FC = () => {
    const {
        meetings,
        loading,
        error,
        page,
        rowsPerPage,
        totalPages,
        startDate,
        endDate,
        state,
        setPage,
        setRowsPerPage,
        setStartDate,
        setEndDate,
        setState,
        resetFilters,
    } = useMeetings("2023-11-10T00:00:00", "2024-12-14T20:00:00");


    const skeletons = (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: rowsPerPage }).map((_, index) => (
                <Skeleton key={index} index={index} />
            ))}
        </div>
    );

    const errorMessage = (
        <p className="text-center text-red-500">Не удалось загрузить мероприятия</p>
    );

    const meetingsGrid = (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {meetings.map((meeting: IMeeting) => (
                <MeetingCard key={meeting.id} meeting={meeting} />
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
            <div className="p-10 pt-0 flex flex-col">
                <TitlePage text="Мероприятия" />
                <MeetingFilter
                    startDate={startDate}
                    endDate={endDate}
                    setStartDate={setStartDate}
                    setEndDate={setEndDate}
                    handleResetFilters={resetFilters}
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
