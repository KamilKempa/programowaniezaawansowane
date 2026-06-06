import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { CurrencyService } from './services/currency.service';
import { of } from 'rxjs';
import { ComponentFixture} from '@angular/core/testing';

describe('AppComponent', () => {
  let fixture: ComponentFixture<AppComponent>;
  let component: AppComponent;
  let serviceSpy: jasmine.SpyObj<CurrencyService>;

  beforeEach(async () => {
    serviceSpy = jasmine.createSpyObj('CurrencyService', [
      'getCurrencies',
      'fetchCurrencies',
      'getByYear',
      'getByMonth',
      'getByQuarter',
    ]);

    serviceSpy.getCurrencies.and.returnValue(of([]));

    await TestBed.configureTestingModule({
      declarations: [AppComponent],
      providers: [
        {provide: CurrencyService, useValue: serviceSpy}
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
  });

  it('should load currencies on init', () => {
    serviceSpy.getCurrencies.and.returnValue(of([]));
    component.date = '2026-06-01';
    component.ngOnInit();

    expect(serviceSpy.getCurrencies).toHaveBeenCalled();
  });

  it('should fetch data', () => {
    serviceSpy.fetchCurrencies.and.returnValue(of({}));
    component.date = '2026-06-01';
    component.fetch();

    expect(serviceSpy.fetchCurrencies).toHaveBeenCalledWith('2026-06-01');
  });

});
