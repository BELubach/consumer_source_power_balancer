export interface RequiredPower {
    consumer_id: number;
    capacity: number;
    source_id: number;
    is_active: boolean;
}

export interface Consumer {
    id: number;
    name: string;
    priority: number;
    requiredPower: RequiredPower[];
    active_power: number | null;
}

export interface ToggleConsumerPowerRequirementRequest {
    is_active: boolean;
}