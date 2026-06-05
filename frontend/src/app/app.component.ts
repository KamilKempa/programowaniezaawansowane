import { Component, OnInit } from '@angular/core';
import { CurrencyService } from './services/currency.service';
import { Currency } from './models/currency';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
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

fetch() {
  this.service.fetchCurrencies(this.date).subscribe(() => {
    alert('Pobrano dane');
    this.load(this.date);
  });
}
}
