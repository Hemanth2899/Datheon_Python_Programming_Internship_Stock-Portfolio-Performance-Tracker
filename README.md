# Datheon_Python_Programming_Internship_Stock-Portfolio-Performance-Tracker
A Python-based Stock Portfolio Performance Tracker that calculates total investment, current portfolio value, and profit or loss for stock holdings. Features include stock ticker validation using S&amp;P 500 data, live stock prices with yfinance, manual price entry as a fallback, and CSV report generation.
📈 Stock Portfolio Performance Tracker

📌 Project Description

The Stock Portfolio Performance Tracker is a Python-based application that helps users monitor their stock investments. Users can enter stock ticker symbols, purchase prices, and quantities to calculate their total investment, current portfolio value, and profit or loss.

The application retrieves stock prices using "yfinance" when available and allows manual price entry if live prices cannot be retrieved. It also saves portfolio summaries in a CSV file for future reference.

✨ Features

- Enter stock ticker symbols, purchase prices, and quantities.
- Validate stock symbols against an S&P 500 constituents dataset when available.
- Retrieve recent stock prices using "yfinance".
- Manually enter current prices when live prices are unavailable.
- Calculate total invested amount and current portfolio value.
- Calculate profit or loss for individual stocks and the entire portfolio.
- Display a formatted performance report in the terminal.
- Save portfolio summaries with timestamps in a CSV file.
- Merge repeated stock holdings using weighted-average purchase prices.

🛠️ Technologies Used

- Python 3
- CSV module
- OS module
- urllib.request
- datetime module
- yfinance (optional, for live stock prices)

📂 Project Structure

Python-Stock-Portfolio-Tracker/
│
├── portfolio.py
├── constituents.csv
├── portfolio_summary.csv
└── README.md

Note: "constituents.csv" is downloaded automatically when available. "portfolio_summary.csv" is created when the program saves its first report. Both CSV files may be absent before the first successful run.

⚙️ Requirements

- Python 3 installed.
- Internet connection for downloading the S&P 500 dataset and retrieving live prices.
- "yfinance" for automatic price retrieval (optional).

🚀 Installation

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

Replace "YOUR_GITHUB_REPOSITORY_URL" with your actual repository URL.

2. Open the project folder

cd Python-Stock-Portfolio-Tracker

3. Install the optional dependency

pip install yfinance

4. Run the program

python portfolio.py

🎮 How to Use

1. Run the Python program.
2. Enter a stock ticker symbol, such as "AAPL".
3. Enter the purchase price per share.
4. Enter the number of shares purchased.
5. Add more holdings if required.
6. Type "done" when you have finished entering holdings.
7. Enter current prices manually if automatic price retrieval is unavailable.
8. Review the portfolio performance report.
9. Find the saved results in "portfolio_summary.csv".

📊 Calculations

Total Investment

Total Investment = Purchase Price × Quantity

Current Portfolio Value

Current Value = Current Price × Quantity

Profit or Loss

Profit/Loss = Current Value − Total Investment

Percentage Gain or Loss

Percentage = (Profit/Loss ÷ Total Investment) × 100

📋 Sample Output

The following is an illustrative example using manually entered prices, not live market data.

Ticker       Qty         Buy     Current      Invested         Value   Gain/Loss        %
AAPL           2      100.00      120.00        200.00        240.00      +40.00   +20.00%

TOTAL                                          200.00        240.00      +40.00   +20.00%

Overall portfolio status: PROFIT

📚 Concepts Learned

- Python functions and loops
- Conditional statements
- Dictionaries and data structures
- Input validation and exception handling
- File handling and CSV operations
- Working with external datasets
- Fetching financial data using a Python library
- Financial calculations and percentage analysis

🔮 Future Enhancements

- Support for stocks from multiple exchanges.
- Interactive charts showing portfolio performance.
- A graphical user interface using Tkinter or Streamlit.
- Historical portfolio tracking and performance visualization.
- More detailed reports and downloadable summaries.
- Improved support for currencies and market-specific symbols.

⚠️ Disclaimer

This project is intended for educational purposes only. Stock prices may be delayed or unavailable, and calculated results may not include brokerage fees, taxes, or other charges. This application does not provide financial advice or investment recommendations.

👨‍💻 Author

Hemanth

📄 License

This project is available for educational and personal learning purposes.
