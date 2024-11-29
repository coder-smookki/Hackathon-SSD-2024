import { useEffect, useState } from "react";
import { IMeeting } from "@/types/meetings/Meetings.ts";
import MeetingService from "@/services/MeetingService.ts";
import {IToken} from "@/types/auth/Auth.ts";

export const useMeetings = (initialStartDate: string, initialEndDate: string, tokenData?: IToken | null ) => {
    const [meetings, setMeetings] = useState<IMeeting[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [totalPages, setTotalPages] = useState(1);

    const [startDate, setStartDate] = useState<string>(initialStartDate);
    const [endDate, setEndDate] = useState<string>(initialEndDate);
    const [state, setState] = useState<string>("");

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
                    tokenData?.user.id
                );

                let fetchedMeetings = data.data.data;

                if (state !== "") {
                    fetchedMeetings = fetchedMeetings.filter(meeting => meeting.state === state);
                }

                const uniqueMeetings = Object.values(
                    fetchedMeetings.reduce((acc, meeting) => {
                        acc[meeting.id] = meeting;
                        return acc;
                    }, {} as Record<string, IMeeting>)
                );

                setMeetings(uniqueMeetings);

                const newTotalPages = Math.ceil(data.data.rowsNumber / rowsPerPage);
                setTotalPages(newTotalPages);

                if (page > newTotalPages && newTotalPages !== 0) {
                    setPage(newTotalPages);
                }
            } catch (err) {
                console.error(err);
                setError("Не удалось загрузить мероприятия");
            } finally {
                setLoading(false);
            }
        };

        fetchMeetingsData();
    }, [page, rowsPerPage, startDate, endDate, state]);

    const resetFilters = () => {
        setStartDate(initialStartDate);
        setEndDate(initialEndDate);
        setState("");
        setPage(1);
    };

    return {
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
    };
};
