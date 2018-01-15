''' Term calculation functions. '''
import numpy as np


def rsf_simple(growth_rate, inflation_rate, num_years):
    '''Get retirement savings factor from growth and inflation.'''
    growth = 1.0 + growth_rate
    inflation = 1.0 + inflation_rate
    pN = growth**num_years
    inflated_growth = sum(
        growth**(num_years - k) * inflation**k for k in range(num_years))
    return float(inflated_growth) / pN


def inflation_factor(inflation_rate, num_years):
    ''' Get the inflation factor for num_years from an average anual inflation rate. '''
    return (inflation_rate + 1.0)**num_years


def mixed_anual_returns(bonds_init_percentage, num_years, bond_aar, stock_aar):
    ''' Create a list of mixed anual returns.

    Considers a protfolio with two types of equities, bonds and stocks.
    Considers that the percentage of stocks diminishes by one every year.

    Args:
        bonds_init_percentage: int, initial percentage of bonds in the portfolio.
        num_years: int, number of years we want to compute
            our mixed anual returns for.
        bond_aar: float, bonds average anual returns.
        stock_aar: float, stocks average anual returns.

    Returns:
        list of float: average anual return of the portfolio per year.
    '''
    ret = []
    for year in range(num_years):
        year_percentage = bonds_init_percentage + year
        year_percentage = min(year_percentage, 100)
        w1 = float(year_percentage) / 100
        w2 = float(100 - year_percentage) / 100
        ret.append(w1 * (1.0 + bond_aar) + w2 * (1.0 + stock_aar))

    return ret


def rsf_returns(bonds_init_percentage, num_years, bond_aar,
                stock_aar, inflation_rate):
    ''' Get the retirement saving factor for a bonds and stocks mixed portfolio.

    Considers a protfolio with two types of equities, bonds and stocks.
    Considers that the percentage of stocks diminishes by one every year.

    Args:
        bonds_init_percentage: int, initial percentage of bonds in the portfolio.
        num_years: int, number of years we want to compute
            our mixed anual returns for.
        bond_aar: float, bonds average anual returns.
        stock_aar: float, stocks average anual returns.
        inflation_rate: float, average anual inflation rate.

    Returns:
        float
    '''
    yearly_growth = mixed_anual_returns(bonds_init_percentage, num_years,
                                        bond_aar, stock_aar)
    final_growth = np.prod(yearly_growth)
    inflation = inflation_rate + 1.0
    inflated_growth = sum(
        np.prod(yearly_growth[k:]) * inflation**k for k in range(num_years))
    return float(inflated_growth) / final_growth
