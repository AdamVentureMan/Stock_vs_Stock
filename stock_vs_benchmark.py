import os
import json
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

# File to save user input
config_file = 'user_input.json'

def save_user_input(stock_symbol, benchmark_symbol, start_date, end_date):
    user_input = {
        "stock_symbol": stock_symbol,
        "benchmark_symbol": benchmark_symbol,
        "start_date": start_date,
        "end_date": end_date
    }
    with open(config_file, 'w') as file:
        json.dump(user_input, file)

def load_user_input():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return json.load(file)
    return None

def fetch_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    return data

def plot_stock_data(stock_data, benchmark_data, stock_symbol, benchmark_symbol):
    # Normalize the prices
    stock_normalized = stock_data['Close'] / stock_data['Close'].iloc[0]
    benchmark_normalized = benchmark_data['Close'] / benchmark_data['Close'].iloc[0]

    # Plot normalized data
    plt.figure(figsize=(10, 5))
    plt.plot(stock_normalized.index, stock_normalized, label=stock_symbol)
    plt.plot(benchmark_normalized.index, benchmark_normalized, label=benchmark_symbol)
    plt.title(f'{stock_symbol} vs {benchmark_symbol} (Normalized Performance)')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def fetch_and_plot():
    stock_symbol = stock_symbol_entry.get().strip().upper()
    benchmark_symbol = benchmark_symbol_entry.get().strip().upper()
    start_date = start_date_entry.get_date().strftime('%Y-%m-%d')
    end_date = end_date_entry.get_date().strftime('%Y-%m-%d')

    save_user_input(stock_symbol, benchmark_symbol, start_date, end_date)
    
    stock_data = fetch_stock_data(stock_symbol, start_date, end_date)
    benchmark_data = fetch_stock_data(benchmark_symbol, start_date, end_date)
    
    if not stock_data.empty and not benchmark_data.empty:
        plot_stock_data(stock_data, benchmark_data, stock_symbol, benchmark_symbol)
    else:
        result_label.config(text="No data found for the given inputs")

# Load saved user input
user_input = load_user_input()

# Create main window
window = tk.Tk()
window.title("Stock vs Benchmark Performance")

# Stock symbol entry
tk.Label(window, text="Stock Symbol:").grid(row=0, column=0, padx=10, pady=10)
stock_symbol_entry = tk.Entry(window)
stock_symbol_entry.grid(row=0, column=1, padx=10, pady=10)
if user_input:
    stock_symbol_entry.insert(0, user_input.get("stock_symbol", ""))

# Benchmark symbol entry
tk.Label(window, text="Benchmark Symbol:").grid(row=1, column=0, padx=10, pady=10)
benchmark_symbol_entry = tk.Entry(window)
benchmark_symbol_entry.grid(row=1, column=1, padx=10, pady=10)
if user_input:
    benchmark_symbol_entry.insert(0, user_input.get("benchmark_symbol", ""))

# Start date entry
tk.Label(window, text="Start Date:").grid(row=2, column=0, padx=10, pady=10)
start_date_entry = DateEntry(window, date_pattern='y-mm-dd')
start_date_entry.grid(row=2, column=1, padx=10, pady=10)
if user_input:
    try:
        start_date_entry.set_date(datetime.strptime(user_input.get("start_date", ""), '%Y-%m-%d'))
    except ValueError:
        start_date_entry.set_date(datetime.now())

# End date entry
tk.Label(window, text="End Date:").grid(row=3, column=0, padx=10, pady=10)
end_date_entry = DateEntry(window, date_pattern='y-mm-dd')
end_date_entry.grid(row=3, column=1, padx=10, pady=10)
if user_input:
    try:
        end_date_entry.set_date(datetime.strptime(user_input.get("end_date", ""), '%Y-%m-%d'))
    except ValueError:
        end_date_entry.set_date(datetime.now())

# Fetch and plot button
fetch_button = tk.Button(window, text="Fetch and Plot", command=fetch_and_plot)
fetch_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Result label
result_label = tk.Label(window, text="")
result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Start the main loop
window.mainloop()
