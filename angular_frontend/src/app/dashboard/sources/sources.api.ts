import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import { Source } from './sources.models';

@Injectable({
    providedIn: 'root'
})
export class SourcesApi {

    constructor(private http: HttpClient) {
    }

    getSources(): Observable<Source[]> {
        return this.http.get<Source[]>('/api/v1/sources');
    }

}