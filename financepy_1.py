from financepy.utils.date import Date
from financepy.products.rates.ibor_deposit import IborDeposit
from financepy.products.rates.ibor_single_curve import IborSingleCurve
from financepy.utils.calendar import CalendarTypes
from financepy.utils.day_count import DayCountTypes
from financepy.products.fx.fx_forward import FXForward


def fx_forward(
    valuation_date,
    forName,
    domName,
    spot_fx_rate,
    strike_fx_rate,
    ccy1InterestRate,
    ccy2InterestRate,
    spot_days,
    notional,
):
    expiry_date = valuation_date.add_months(12)
    currency_pair = forName + domName
    settlement_date = valuation_date.add_weekdays(spot_days)
    maturity_date = settlement_date.add_months(12)
    calendar_type = CalendarTypes.TARGET

    depos = []
    fras = []
    swaps = []
    deposit_rate = ccy1InterestRate
    depo = IborDeposit(settlement_date, maturity_date, deposit_rate,
                       DayCountTypes.ACT_360, notional, calendar_type)
    depos.append(depo)
    for_discount_curve = IborSingleCurve(valuation_date, depos, fras, swaps)

    depos = []
    fras = []
    swaps = []
    deposit_rate = ccy2InterestRate
    depo = IborDeposit(settlement_date, maturity_date, deposit_rate,
                       DayCountTypes.ACT_360, notional, calendar_type)
    depos.append(depo)
    dom_discount_curve = IborSingleCurve(valuation_date, depos, fras, swaps)

    notional_currency = forName

    fxForward = FXForward(expiry_date,
                          strike_fx_rate,
                          currency_pair,
                          notional,
                          notional_currency)

    fwdValue = fxForward.value(valuation_date, spot_fx_rate,
                               dom_discount_curve, for_discount_curve)

    fwdFXRate = fxForward.forward(valuation_date, spot_fx_rate,
                                  dom_discount_curve,
                                  for_discount_curve)

    return fwdValue, fwdFXRate


fx_value, fx_rate = fx_forward(
    valuation_date=Date(13, 2, 2018),
    forName="EUR",
    domName="USD",
    spot_fx_rate=1.300,
    strike_fx_rate=1.365,
    ccy1InterestRate=0.02,
    ccy2InterestRate=0.05,
    spot_days=0,
    notional=100.0,
)

print(fx_value)
print(fx_rate)
