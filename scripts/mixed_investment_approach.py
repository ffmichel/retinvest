''' Compute the amount needed for retirement, provided we have
* the number of retirement years,
* the number of years before retirement (for inflation purposes),
* the yearly amount we want at retirement in current currency (inflation
  until year of retirement will be accounted for),
* the average anual return of our investment in bonds.
* the average anual return of our investment in stocks.
* the initial percentage of bonds when we start our retirement.
We assume that every year more stocks will be reassigned to bonds,
at a rate of one percent per year.
The calculations are done with a simplistic assumption of an average growth rate.
'''
import argparse

from retinvest import term

DEFAULT_BONDS_INITIAL_PERCENTAGE = 65

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-B', '--bonds_aar', type=float, required=True)
    parser.add_argument('-S', '--stocks_aar', type=float, required=True)
    parser.add_argument(
        '-b',
        '--bonds_initial_percentage',
        type=float,
        required=False,
        default=DEFAULT_BONDS_INITIAL_PERCENTAGE)
    parser.add_argument('-i', '--inflation_rate', type=float, required=True)
    parser.add_argument(
        '-N', '--num_retirement_years', type=int, required=True)
    parser.add_argument('-n', '--num_years_before', type=int, required=True)
    parser.add_argument('-Y', '--yearly_salary', type=float, required=True)
    args = parser.parse_args()

    inflated_yearly = args.yearly_salary * term.inflation_factor(
        args.inflation_rate, args.num_years_before)

    res = inflated_yearly * term.rsf_returns(
        bonds_init_percentage=args.bonds_initial_percentage,
        num_years=args.num_retirement_years,
        bond_aar=args.bonds_aar,
        stock_aar=args.stocks_aar,
        inflation_rate=args.inflation_rate)

    msg = '''Amount needed to be saved for retirement with:
    * bonds average anual return: {B},
    * stocks average anual return: {S},
    * bonds initial percentage: {b}%,
    * yearly inflation rate: {i},
    * {N} years of pension.
    * {n} years before pension.
    * ${Y:,.2f} yearly salary in current currency (${inflated_Y:,.2f} at retirement time)
    ------------------
    ${A:,.2f}
    ------------------'''
    print msg.format(
        B=args.bonds_aar,
        S=args.stocks_aar,
        b=args.bonds_initial_percentage,
        i=args.inflation_rate,
        N=args.num_retirement_years,
        n=args.num_years_before,
        Y=args.yearly_salary,
        inflated_Y=inflated_yearly,
        A=res)
