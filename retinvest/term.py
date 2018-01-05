import argparse


def rsf_simple(growth, inflation, year_number):
    '''Get retirement savings factor from growth and inflation.'''
    pN = growth**year_number
    inflated_growth = sum(growth**(year_number - k) * inflation**k
                          for k in range(year_number))
    return float(inflated_growth) / pN

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--growth_rate', type=float, required=True)
    parser.add_argument('-i', '--inflation_rate', type=float, required=True)
    parser.add_argument('-N', '--num_years', type=int, required=True)
    parser.add_argument('-Y', '--yearly_salary', type=float, required=True)
    args = parser.parse_args()

    res = args.yearly_salary * rsf_simple(growth=args.growth_rate + 1.0,
                                          inflation=args.inflation_rate + 1.0,
                                          year_number=args.num_years)
    msg = '''Amount needed to be saved for retirement with:
             * yearly growth rate of the investment: {},
             * yearly inflation rate: {},
             * {} years of pension.
             ------------------
             {}
             ------------------'''
    print(msg.format(args.growth_rate, args.inflation_rate, args.num_years, res))
