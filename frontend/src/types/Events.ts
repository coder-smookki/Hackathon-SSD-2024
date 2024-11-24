export interface IEvent {
    duration: number;
    endedAt: string;
    id: number;
    isOfflineEvent: boolean;
    name: string;
    roomId?: number;
    startedAt: string
}

export interface IEventsData {
    data: IEvent[];
    page: number;
    rowsNumber: number;
    rowsPerPage: number;
    showDeleted: boolean;
    sortBy: string;
}