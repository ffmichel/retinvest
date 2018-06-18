''' Compute the amount needed for retirement, provided we have
* the number of retirement years,
* the number of years before retirement (for inflation purposes),
* the yearly amount we want at retirement in current currency (inflation
  until year of retirement will be accounted for),
* the average annual return of our investment in bonds.
* the average annual return of our investment in stocks.
* the age at which we want to have a portfolio consisting of bonds only.
We assume that every year more stocks will be reassigned to bonds,
at a rate of one percent per year.
The calculations are done with a simplistic assumption of an average growth
rate.
'''
import argparse

from retinvest import term

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-B', '--bonds_aar', type=float, required=True)
    parser.add_argument('-S', '--stocks_aar', type=float, required=True)
    parser.add_argument('-a', '--retirement_age', type=int, required=True)
    parser.add_argument('-i', '--inflation_rate', type=float, required=True)
    parser.add_argument(
        '-N', '--num_retirement_years', type=int, required=True)
    parser.add_argument('-n', '--num_years_before', type=int, required=True)
    parser.add_argument('-Y', '--yearly_salary', type=float, required=True)
    parser.add_argument(
        '--bond_portfolio_age', type=float, required=False, default=100)
    args = parser.parse_args()

    inflated_yearly = args.yearly_salary * term.inflation_factor(
        args.inflation_rate, args.num_years_before)

    annual_returns = term.mixed_annual_returns(
        start=args.retirement_age,
        length=args.num_retirement_years,
        bond_portfolio_age=args.bond_portfolio_age,
        bond_aar=args.bonds_aar,
        stock_aar=args.stocks_aar)
    res = inflated_yearly * term.retirement_saving_factor(
        annual_returns=annual_returns, inflation_rate=args.inflation_rate)

    msg = '''Amount needed to be saved for retirement with:
    * bonds average annual return: {B},
    * stocks average annual return: {S},
    * retirement age: {a},
    * Age of full bond portfolio: {bpa},
    * yearly inflation rate: {i},
    * {N} years of pension.
    * {n} years before pension.
    * ${Y:,.2f} yearly salary in current currency (${inflated_Y:,.2f} at
      retirement time)
    ------------------
    ${A:,.2f}
    ------------------'''
    print msg.format(
        B=args.bonds_aar * 100.,
        S=args.stocks_aar * 100.,
        a=args.retirement_age,
        bpa=args.bond_portfolio_age,
        i=args.inflation_rate,
        N=args.num_retirement_years,
        n=args.num_years_before,
        Y=args.yearly_salary,
        inflated_Y=inflated_yearly,
        A=res)
