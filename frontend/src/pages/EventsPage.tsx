import React, { useEffect, useState } from "react";
import { IEvent } from "@/types/Events.ts";
import EventCard from "@/components/Events/EventCard.tsx";
import Pagination from "@/components/Events/Pagination.tsx";
import Skeleton from "@/components/Events/Skeleton.tsx";
import SidebarLayout from "@/layout.tsx";
import EventService from "@/services/EventService.ts";

const EventsPage: React.FC = () => {
    // Состояния
    const [events, setEvents] = useState<IEvent[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [totalPages, setTotalPages] = useState(1);

    // Загрузка данных
    useEffect(() => {
        const fetchEventsData = async () => {
            setLoading(true);
            setError(null);

            try {
                const data = await EventService.fetchEvents(page, rowsPerPage);
                setEvents(data.data.data);
                const newTotalPages = Math.ceil(data.data.rowsNumber / rowsPerPage);
                setTotalPages(newTotalPages);

                // Если текущая страница выходит за пределы общего количества страниц
                if (page > newTotalPages) {
                    setPage(newTotalPages);
                }
            } catch (err) {
                console.error(err);
                setError("Не удалось загрузить мероприятия");
            } finally {
                setLoading(false);
            }
        };

        fetchEventsData();
    }, [page, rowsPerPage]);

    // Управление страницами
    const handleNextPage = () => {
        if (page < totalPages) setPage(page + 1);
    };

    const handlePrevPage = () => {
        if (page > 1) setPage(page - 1);
    };

    // Элементы для рендера
    const header = (
        <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-10 text-center">
            Мероприятия
        </h1>
    );

    const skeletons = (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: rowsPerPage }).map((_, index) => (
                <Skeleton key={index} index={index} />
            ))}
        </div>
    );

    const errorMessage = (
        <p className="text-center text-red-500">{error}</p>
    );

    const eventsGrid = (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {events.map((event) => (
                <EventCard
                    key={event.id}
                    name={event.name}
                    startedAt={event.startedAt}
                    endedAt={event.endedAt}
                />
            ))}
        </div>
    );

    const noEventsMessage = (
        <p className="text-center text-lg">Мероприятия отсутствуют</p>
    );

    const pagination = (
        <Pagination
            page={page}
            totalPages={totalPages}
            rowsPerPage={rowsPerPage}
            onNext={handleNextPage}
            onPrev={handlePrevPage}
            onRowsChange={setRowsPerPage}
        />
    );

    // Основной рендер
    return (
        <SidebarLayout>
            <div className="p-10">
                {header}
                {loading && skeletons}
                {error && errorMessage}
                {!loading && !error && events.length > 0 && (
                    <>
                        {eventsGrid}
                        {pagination}
                    </>
                )}
                {!loading && !error && events.length === 0 && noEventsMessage}
            </div>
        </SidebarLayout>
    );
};

export default EventsPage;
