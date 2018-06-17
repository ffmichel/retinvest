''' Term calculation functions. '''
import numpy as np


def inflation_factor(inflation_rate, num_years):
    ''' Get the compund inflation factor after num_years. '''
    return (inflation_rate + 1.0)**num_years


def constant_returns(average_anual_return, num_retirement_years):
    ''' Create a list of constant returns. '''
    return [average_anual_return for _ in range(num_retirement_years)]


def mixed_anual_returns(retirement_age, num_retirement_years,
                        bond_portfolio_age, bond_aar, stock_aar):
    ''' Create a list of mixed annual returns.

    Considers a portfolio with two types of equities, bonds and stocks.
    Considers that the percentage of stocks diminishes by one every year.

    Args:
        retirement_age (int): Age considered for retirment.
        num_retirement_years (int): Number of years for retirement.
        bond_portfolio_age (int): Age at which the portfolio consists of only
            bonds (e.g, 100, 110 or 120).
        bond_aar: float, bonds average annual returns.
        stock_aar: float, stocks average annual returns.

    Returns:
        (list[float]): Average annual return of the portfolio per year.
    '''
    ret = [
        float(max(bond_portfolio_age - year, 0)) / 100.0 * stock_aar +
        float(min(bond_portfolio_age, year) / 100.0) * bond_aar
        for year in range(retirement_age, retirement_age +
                          num_retirement_years)
    ]
    return ret


def retirement_saving_factor(anual_returns, inflation_rate):
    ''' Get the retirement saving factor given a list of anual growth.

    Args:
        anual_returns (list[float]): Expected anual return for each
            retirement year.
        inflation_rate (float): average annual inflation rate.

    Returns:
        float
    '''
    anual_growths = [1. + ret for ret in anual_returns]
    final_return = np.prod(anual_growths)
    num_retirement_years = len(anual_growths)
    inflation = inflation_rate + 1.0
    inflated_return = sum(
        np.prod(anual_growths[k:]) * inflation**k
        for k in range(num_retirement_years))
    return float(inflated_return) / final_return
