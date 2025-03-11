import numpy as np
import pandas as pd
import scipy.stats as stats
import tkinter as tk
from tkinter import ttk, messagebox

# Monte Carlo Simulation Function
def run_simulation():
    try:
        # Get user inputs
        initial_capital = float(capital_var.get())
        portfolio_mean_return = float(return_var.get()) / 100
        portfolio_volatility = float(volatility_var.get()) / 100
        confidence_level = float(confidence_var.get()) / 100

        # Simulation Parameters
        np.random.seed(42)
        simulations = 10_000
        time_horizon = 252  # 1 year of trading days
        simulated_returns = np.random.normal(
            portfolio_mean_return / time_horizon,
            portfolio_volatility / np.sqrt(time_horizon),
            (time_horizon, simulations)
        )

        # Portfolio Value Simulation
        simulated_portfolio = initial_capital * np.cumprod(1 + simulated_returns, axis=0)

        # Compute Risk Metrics
        VaR_95 = initial_capital - np.percentile(simulated_portfolio[-1, :], (1 - confidence_level) * 100)
        worst_case = np.percentile(simulated_portfolio[-1, :], 5)

        # Display Results
        result_text.set(f"Initial Capital: {initial_capital:,.0f} HUF\n"
                        f"95% Value at Risk (VaR): {VaR_95:,.0f} HUF\n"
                        f"Worst 5% Outcome: {worst_case:,.0f} HUF")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# GUI Setup
root = tk.Tk()
root.title("Risk Capital Analysis Tool")
root.geometry("400x400")

# Input Fields
tk.Label(root, text="Initial Capital (HUF):").pack()
capital_var = tk.StringVar(value="1000000")
tk.Entry(root, textvariable=capital_var).pack()

tk.Label(root, text="Expected Return (% per year):").pack()
return_var = tk.StringVar(value="8")
tk.Entry(root, textvariable=return_var).pack()

tk.Label(root, text="Volatility (% per year):").pack()
volatility_var = tk.StringVar(value="15")
tk.Entry(root, textvariable=volatility_var).pack()

tk.Label(root, text="Confidence Level (%):").pack()
confidence_var = tk.StringVar(value="95")
tk.Entry(root, textvariable=confidence_var).pack()

# Run Simulation Button
ttk.Button(root, text="Run Simulation", command=run_simulation).pack(pady=10)

# Result Display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", fg="blue")
result_label.pack()

# Run GUI
root.mainloop()
