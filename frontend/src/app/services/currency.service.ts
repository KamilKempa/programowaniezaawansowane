import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Currency } from '../models/currency';

@Injectable({
  providedIn: 'root'
})
export class CurrencyService {

  private api = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getCurrencies(date?: string) {
    let url = `${this.api}/currencies`

    if (date) {
      url += `?date=${date}`;
    }

    return this.http.get<Currency[]>(url);
  }

  fetchCurrencies(date: string) {
    return this.http.post(`${this.api}/currencies/fetch?date=${date}`, {});
  }
}