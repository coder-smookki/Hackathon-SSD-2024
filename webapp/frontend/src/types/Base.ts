export interface BaseData<T> {
    rowsPerPage: number;
    rowsNumber: number;
    page: number;
    showDeleted: boolean;
    data: T[];
    sortBy: string;
}