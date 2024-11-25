export interface IMeeting {
    permalinkId: string;
    permalink: string;
    id: number;
    name: string;
    roomId?: number;
    participantsCount: number;
    sendNotificationsAt: string;
    startedAt: string;
    endedAt: string;
    duration?: number;
    isGovernorPresents: boolean;
    createdAt: string;
    closedAt?: string;
    state: string;
    organizedBy: number;
    createdBy: number;
    isNotifyAccepted: boolean;
    isVirtual: boolean;
}

export interface IMeetingsData {
    rowsPerPage: number;
    rowsNumber: number;
    page: number;
    showDeleted: boolean;
    data: IMeeting[];
    sortBy: string;
}