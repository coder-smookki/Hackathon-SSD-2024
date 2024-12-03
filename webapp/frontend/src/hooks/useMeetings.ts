import { useEffect, useState } from "react";
import MeetingService from "@/services/MeetingService.ts";
import {IMeeting} from "@/types/Meetings.ts";

export const useMeetings = (
    page: number,
    rowsPerPage: number,
    startDate: string,
    endDate: string,
    state: string,
    userId?: number
) => {
    const [meetings, setMeetings] = useState<IMeeting[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [totalPages, setTotalPages] = useState(1);

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
                    userId
                );
                setMeetings(data.data.data);
                setTotalPages(Math.ceil(data.data.rowsNumber / rowsPerPage));
            } catch (err) {
                console.error(err);
                setError("Не удалось загрузить мероприятия");
            } finally {
                setLoading(false);
            }
        };

        fetchMeetingsData();
    }, [page, rowsPerPage, startDate, endDate, state, userId]);

    return { meetings, loading, error, totalPages };
};
