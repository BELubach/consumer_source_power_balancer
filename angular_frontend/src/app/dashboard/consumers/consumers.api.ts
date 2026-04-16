import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Consumer } from './consumers.models';
import { ToggleConsumerPowerRequirementRequest } from './consumers.models';

@Injectable({ providedIn: 'root' })
export class ConsumerApi {

    constructor(private http: HttpClient) { }

    getConsumers(): Observable<Consumer[]> {
        return this.http.get<Consumer[]>('/api/v1/consumers');
    }

    deactivateConsumer(
        consumerId: number,
        request: ToggleConsumerPowerRequirementRequest
    ): Observable<Consumer> {
        return this.http.patch<Consumer>(
            `/api/v1/consumers/${consumerId}`,
            request
        );
    }
}