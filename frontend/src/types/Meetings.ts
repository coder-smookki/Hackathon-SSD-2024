import {BaseData} from "@/types/Base.ts";

export interface IMeeting {
    permalinkId: string;
    permalink: string;
    id: number;
    name: string;
    roomId: number | null;
    participantsCount: number;
    sendNotificationsAt: string;
    startedAt: string;
    endedAt: string;
    duration: number | null;
    isGovernorPresents: boolean;
    createdAt: string;
    closedAt: string | null;
    state: string;
    organizedBy: number;
    createdBy: number;
    isNotifyAccepted: boolean;
    isVirtual: boolean;
}

export interface MeetingFormValues {
    name: string;
    roomId?: number;
    comment: string;
    participantsCount: number;
    participants: User[];
    sendNotificationsAt: string;
    isMicrophoneOn: boolean;
    isVideoOn: boolean;
    isWaitingRoomEnabled: boolean;
    needVideoRecording: boolean;
    startedAt: string;
    endedAt: string;
    duration: number;
    isNotifyAccepted: boolean;
    isVirtual: boolean;
    state: string;
}

export interface User {
    id: number;
    email?: string;
    lastName?: string;
    firstName?: string;
    middleName?: string | null;
    roleIds?: number[];
    departmentId?: number;
}

interface Participant {
    id: number;
    email: string | null;
    lastName: string | null;
    firstName: string | null;
    middleName: string | null;
    isApproved: boolean | null;
}

interface CiscoSettings {
    isMicrophoneOn: boolean;
    isVideoOn: boolean;
    isWaitingRoomEnabled: boolean;
    needVideoRecording: boolean;
    id?: number;
    isPrivateLicenceUsed?: boolean;
}

interface Event {
    isOfflineEvent: boolean;
    roomId: string | null;
    name: string;
    startedAt: string;
    endedAt: string;
    duration: number;
    id: number;
}

export interface CreateMeetingResponse {
    permalinkId?: string;
    permalink?: string;
    id?: number;
    name: string;
    roomId?: string | null;
    participantsCount: number;
    sendNotificationsAt: string;
    startedAt: string;
    endedAt?: string;
    duration: number;
    isGovernorPresents?: boolean;
    createdAt?: string;
    closedAt?: string | null;
    state: string;
    isNotifyAccepted?: boolean;
    isVirtual: boolean;
    organizerPermalinkId?: string;
    organizerPermalink?: string;
    comment?: string | null;
    event?: Event;
    room?: string | null;
    ciscoRoom?: string | null;
    ciscoSettings: CiscoSettings;
    vinteoSettings: {
        needVideoRecording: boolean;
    };
    externalSettings?: string | null;
    participants: Participant[];
    attachments?: any[];
    groups?: any[];
    ciscoSettingsId?: number;
    ciscoRoomId?: string | null;
    eventId?: number;
    updatedAt?: string;
    backend: string;
    organizedBy: User;
    recurrenceUpdateType: string | null;
}

export interface GetMeetingResponse {
    id: number;
    name: string;
    roomId: number | null;
    room: string | null;
    startedAt: string;
    endedAt: string;
    backend: string;
    participantsCount: number;
    organizedBy: number;
    participants: Participant[];
    organizedUser: User;
    permalink: string;
}

export interface IMeetingsData extends BaseData<IMeeting> {}
