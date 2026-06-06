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

  getByYear(year: number) {
    return this.http.get<Currency[]>(
      `${this.api}/currencies/year/${year}`
    );
  }
  
  getByMonth(year: number, month: number) {
    return this.http.get<Currency[]>(
      `${this.api}/currencies/month/${year}/${month}`
    );
  }
  
  getByQuarter(year: number, quarter: number) {
    return this.http.get<Currency[]>(
      `${this.api}/currencies/quarter/${year}/${quarter}`
    );
  }
  
  fetchCurrencies(date: string) {
    return this.http.post(`${this.api}/currencies/fetch?date=${date}`, {});
  }
}