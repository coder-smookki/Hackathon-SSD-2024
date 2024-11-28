import React, { useState, useEffect } from "react";
import { Select, SelectItem, SelectTrigger, SelectValue, SelectContent } from "@/components/ui/select";
import {Label} from "@/components/ui/label.tsx";
import $api from "@/http";

interface Room {
    id: number;
    name: string;
    description: string;
    buildingId: number;
}

interface Building {
    id: number;
    name: string;
    address: string;
}

interface BuildingsListProps {
    selectedBuildingId: number | null;
    onBuildingSelect: (id: number) => void;
    selectedRoomId: number | null;
    onRoomSelect: (id: number) => void;
}

const BuildingsList: React.FC<BuildingsListProps> = ({ selectedBuildingId, onBuildingSelect, selectedRoomId, onRoomSelect }) => {
    const [buildings, setBuildings] = useState<Building[]>([]);
    const [rooms, setRooms] = useState<Room[]>([]);
    const [filteredRooms, setFilteredRooms] = useState<Room[]>([]);
    const [loadingBuildings, setLoadingBuildings] = useState<boolean>(false);
    const [loadingRooms, setLoadingRooms] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchBuildings = async () => {
            setLoadingBuildings(true);
            try {
                const response = await $api.get("https://test.vcc.uriit.ru/api/catalogs/buildings");
                setBuildings(response.data.data);
            } catch (err) {
                setError("Не удалось загрузить список зданий.");
            } finally {
                setLoadingBuildings(false);
            }
        };

        fetchBuildings();
    }, []);

    useEffect(() => {
        const fetchRooms = async () => {
            setLoadingRooms(true);
            try {
                const response = await $api.get("https://test.vcc.uriit.ru/api/catalogs/rooms");
                setRooms(response.data.data);
            } catch (err) {
                setError("Не удалось загрузить список комнат.");
            } finally {
                setLoadingRooms(false);
            }
        };

        fetchRooms();
    }, []);

    useEffect(() => {
        if (selectedBuildingId) {
            const filtered = rooms.filter(room => room.buildingId === selectedBuildingId);
            setFilteredRooms(filtered);
        }
    }, [selectedBuildingId, rooms]);

    return (
        <>
            {/* Выбор здания */}
            <div>
                <Label htmlFor="building">Выберите здание</Label>
                {loadingBuildings && <p>Загружаем здания...</p>}
                {error && <p className="text-red-500">{error}</p>}

                <Select
                    value={selectedBuildingId ? selectedBuildingId.toString() : ""}
                    onValueChange={(value) => onBuildingSelect(Number(value))}
                >
                    <SelectTrigger id="building">
                        <SelectValue placeholder="Выберите здание" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value={null!}>Выберите здание</SelectItem>
                        {buildings.map((building) => (
                            <SelectItem key={building.id} value={building.id.toString()}>
                                {building.name} - {building.address}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>

            {/* Выбор комнаты */}
            <div>
                <Label htmlFor="roomId">Выберите комнату <span className="text-red-500">*</span></Label>
                {loadingRooms && <p>Загружаем комнаты...</p>}
                {error && <p className="text-red-500">{error}</p>}

                <Select
                    value={selectedRoomId ? selectedRoomId.toString() : ""}
                    onValueChange={(value) => onRoomSelect(Number(value))}
                    disabled={!selectedBuildingId}
                >
                    <SelectTrigger id="roomId">
                        <SelectValue placeholder="Выберите комнату" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value={null!}>Выберите комнату</SelectItem>
                        {filteredRooms.map((room) => (
                            <SelectItem key={room.id} value={room.id.toString()}>
                                {room.name} - {room.description}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>
        </>
    );
};

export default BuildingsList;
