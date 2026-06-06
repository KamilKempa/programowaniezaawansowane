import { Component, OnInit } from '@angular/core';
import { CurrencyService } from './services/currency.service';
import { Currency } from './models/currency';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  year: number = new Date().getFullYear();
  month: number = new Date().getMonth() + 1;
  quarter: number = 1;
  currencies: Currency[] = [];

  constructor(private service: CurrencyService) {}

  ngOnInit(): void {
    this.date = new Date().toISOString().split('T')[0];
    this.load(this.date);
  }

  load(date?: string) {
    this.service.getCurrencies(date).subscribe(data => {
      this.currencies = data;
    });
  }
  date: string = '';

  handleError(err: any) {
    const msg =
      err.error?.detail ||
      err.error?.error ||
      'Brak danych dla wybranego okresu';
  
    alert(msg);
  }

  fetch() {
    this.service.fetchCurrencies(this.date).subscribe({
      next: () => {
        alert('Pobrano dane');
        this.load(this.date);
      },
      error: (err) => this.handleError(err)
    });
  }
  loadYear() {
    this.service.getByYear(this.year).subscribe({
      next: data => this.currencies = data,
      error: err => this.handleError(err)
    });
  }
  
  loadMonth() {
    this.service.getByMonth(this.year, this.month).subscribe({
      next: data => this.currencies = data,
      error: err => this.handleError(err)
    });
  }
  
  loadQuarter() {
    this.service.getByQuarter(this.year, this.quarter).subscribe({
      next: data => this.currencies = data,
      error: err => this.handleError(err)
    });
  }
}
