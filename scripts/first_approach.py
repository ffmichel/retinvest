''' Compute the amount needed for retirement, provided we have
* the number of retirement years,
* the number of years before retirement (for inflation purposes),
* the yearly amount we want at retirement in current currency (inflation
  until year of retirement will be accounted for),
* the average anual return of our investment.
The calculations are done with a simplistic assumption of an average anual return.
'''
import argparse

from retinvest import term

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--aar', type=float, required=True)
    parser.add_argument('-i', '--inflation_rate', type=float, required=True)
    parser.add_argument(
        '-N', '--num_retirement_years', type=int, required=True)
    parser.add_argument('-n', '--num_years_before', type=int, required=True)
    parser.add_argument('-Y', '--yearly_salary', type=float, required=True)
    args = parser.parse_args()

    inflated_yearly = args.yearly_salary * term.inflation_factor(
        args.inflation_rate, args.num_years_before)

    res = args.yearly_salary * term.rsf_simple(
        growth_rate=args.aar,
        inflation_rate=args.inflation_rate,
        num_years=args.num_retirement_years)

    msg = '''Amount needed to be saved for retirement with:
    * average anual return of the investment: {p},
    * yearly inflation rate: {i},
    * {N} years of pension.
    * {n} years before pension.
    * ${Y:,.2f} yearly salary in current currency (${inflated_Y:,.2f} at retirement time)
    ------------------
    ${A:,.2f}
    ------------------'''
    print msg.format(
        p=args.aar,
        i=args.inflation_rate,
        N=args.num_retirement_years,
        n=args.num_years_before,
        Y=args.yearly_salary,
        inflated_Y=inflated_yearly,
        A=res)
