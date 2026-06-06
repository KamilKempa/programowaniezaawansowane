import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { CurrencyService } from './currency.service';

describe('CurrencyService', () => {
  let service: CurrencyService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [CurrencyService]
    });
    service = TestBed.inject(CurrencyService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should fetch currencies', () => {
    service.getCurrencies('2026-06-01').subscribe(data =>{
      expect(data).toBeTruthy();
    });
    const req = httpMock.expectOne('http://localhost:8000/currencies?date=2026-06-01');
    expect(req.request.method).toBe('GET');
    req.flush([]);
  });

  it('should call fetch endpoint', () => {
    service.fetchCurrencies('2026-06-01').subscribe(Response =>{
      expect(Response).toBeTruthy();
    });
    
    const req = httpMock.expectOne('http://localhost:8000/currencies/fetch?date=2026-06-01');
    expect(req.request.method).toBe('POST');
    req.flush({message: 'ok'});
  })
});
