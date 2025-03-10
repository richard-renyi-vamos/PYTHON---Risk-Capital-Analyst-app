import numpy as np
import pandas as pd
import scipy.stats as stats

# Portfolio Simulation Parameters
np.random.seed(42)  # For reproducibility
portfolio_mean_return = 0.08  # 8% annual return
portfolio_volatility = 0.15   # 15% standard deviation
initial_capital = 1_000_000   # Initial investment: 1 million HUF

# Monte Carlo Simulation (10000 scenarios)
simulations = 10_000
time_horizon = 252  # 1 year of trading days
simulated_returns = np.random.normal(portfolio_mean_return / time_horizon, 
                                     portfolio_volatility / np.sqrt(time_horizon), 
                                     (time_horizon, simulations))

# Portfolio Value Simulation
simulated_portfolio = initial_capital * np.cumprod(1 + simulated_returns, axis=0)

# Compute Value at Risk (VaR)
confidence_level = 0.95
VaR_95 = initial_capital - np.percentile(simulated_portfolio[-1, :], (1 - confidence_level) * 100)

# Stress Testing (Worst-Case Scenarios)
worst_case = np.percentile(simulated_portfolio[-1, :], 5)

# Print Key Risk Metrics
print(f"Initial Capital: {initial_capital:,.0f} HUF")
print(f"95% Value at Risk (VaR): {VaR_95:,.0f} HUF")
print(f"Worst 5% Outcome (Stress Test): {worst_case:,.0f} HUF")

# Generate a Simple Risk Report
risk_report = pd.DataFrame({
    "Metric": ["Initial Capital", "95% VaR", "Worst 5% Case"],
    "Value (HUF)": [initial_capital, VaR_95, worst_case]
})

print("\nRisk Report:")
print(risk_report)
