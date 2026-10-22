"""
Stock Portfolio Performance Tracker
-----------------------------------
- Enter ticker, buy price and quantity for each holding
- Validates tickers against the S&P 500 constituents CSV (cached as constituents.csv)
- Gets the current price live via yfinance (if installed), else asks you to type it
- Shows total invested, current value, and % gain/loss per holding
- Appends a summary to portfolio_summary.csv

Optional (for live prices):  pip install yfinance
"""

import csv
import os
import urllib.request
from datetime import datetime

TICKER_URL = (
    "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/"
    "master/data/constituents.csv"
)
TICKER_FILE = "constituents.csv"
SUMMARY_FILE = "portfolio_summary.csv"


# ---------------------------------------------------------------- tickers
def load_tickers():
    """Return {symbol: company name}. Downloads the CSV once and caches it."""
    if not os.path.exists(TICKER_FILE):
        try:
            print("Downloading S&P 500 ticker dataset...")
            urllib.request.urlretrieve(TICKER_URL, TICKER_FILE)
        except Exception:
            print("Could not download ticker dataset. Ticker validation disabled.\n")
            return {}

    tickers = {}
    try:
        with open(TICKER_FILE, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                tickers[row["Symbol"].strip().upper()] = row.get("Security", "").strip()
    except (OSError, KeyError):
        return {}
    return tickers


# ----------------------------------------------------------------- prices
def fetch_live_price(symbol):
    """Try to get the latest price with yfinance. Returns float or None."""
    try:
        import yfinance as yf  # imported lazily so the script works without it

        # yfinance uses '-' instead of '.' (e.g. BRK.B -> BRK-B)
        ticker = yf.Ticker(symbol.replace(".", "-"))
        hist = ticker.history(period="5d")
        if not hist.empty:
            return float(hist["Close"].iloc[-1])
    except Exception:
        pass
    return None


def get_current_price(symbol):
    price = fetch_live_price(symbol)
    if price is not None:
        return price, "live"
    # fallback: manual entry
    while True:
        raw = input(f"  Live price for {symbol} unavailable. Enter current price: ").strip()
        try:
            value = float(raw)
            if value > 0:
                return value, "manual"
        except ValueError:
            pass
        print("  Please enter a positive number.")


# ------------------------------------------------------------------ input
def read_positive(prompt, cast=float):
    while True:
        raw = input(prompt).strip()
        try:
            value = cast(raw)
            if value > 0:
                return value
        except ValueError:
            pass
        print("  Please enter a positive number.")


def collect_holdings(tickers):
    """Build the portfolio dictionary: {symbol: {'buy_price':..., 'quantity':...}}."""
    portfolio = {}
    print("\nEnter your holdings. Type 'done' as the ticker when finished.\n")

    while True:
        symbol = input("Ticker symbol (or 'done'): ").strip().upper()

        if symbol == "DONE":
            if portfolio:
                break
            print("  Add at least one holding first.")
            continue

        if not symbol:
            continue

        if tickers and symbol not in tickers:
            print(f"  '{symbol}' is not in the S&P 500 list. Check the symbol.")
            continue

        if tickers:
            print(f"  -> {tickers[symbol]}")

        buy_price = read_positive("  Buy price per share: ")
        quantity = read_positive("  Quantity (shares): ")

        if symbol in portfolio:
            # merge into one position using weighted-average cost
            old = portfolio[symbol]
            total_qty = old["quantity"] + quantity
            avg = (old["buy_price"] * old["quantity"] + buy_price * quantity) / total_qty
            portfolio[symbol] = {"buy_price": avg, "quantity": total_qty}
            print(f"  Updated {symbol}: avg buy {avg:.2f}, qty {total_qty:g}")
        else:
            portfolio[symbol] = {"buy_price": buy_price, "quantity": quantity}

    return portfolio


# ------------------------------------------------------------ calculation
def evaluate(portfolio):
    """Return (rows, totals) with invested, current value and gain/loss."""
    rows = []
    print("\nFetching current prices...")
    for symbol, pos in portfolio.items():
        current, source = get_current_price(symbol)
        invested = pos["buy_price"] * pos["quantity"]
        value = current * pos["quantity"]
        gain = value - invested
        pct = (gain / invested) * 100
        rows.append(
            {
                "symbol": symbol,
                "quantity": pos["quantity"],
                "buy_price": pos["buy_price"],
                "current_price": current,
                "invested": invested,
                "current_value": value,
                "gain_loss": gain,
                "gain_loss_pct": pct,
                "source": source,
            }
        )

    total_invested = sum(r["invested"] for r in rows)
    total_value = sum(r["current_value"] for r in rows)
    total_gain = total_value - total_invested
    total_pct = (total_gain / total_invested) * 100 if total_invested else 0.0
    totals = {
        "invested": total_invested,
        "current_value": total_value,
        "gain_loss": total_gain,
        "gain_loss_pct": total_pct,
    }
    return rows, totals


# ----------------------------------------------------------------- output
def print_report(rows, totals):
    line = "=" * 92
    print("\n" + line)
    print(f"{'PORTFOLIO PERFORMANCE':^92}")
    print(line)
    print(
        f"{'Ticker':<8}{'Qty':>8}{'Buy':>12}{'Current':>12}"
        f"{'Invested':>14}{'Value':>14}{'Gain/Loss':>12}{'%':>9}"
    )
    print("-" * 92)
    for r in rows:
        print(
            f"{r['symbol']:<8}{r['quantity']:>8g}{r['buy_price']:>12.2f}"
            f"{r['current_price']:>12.2f}{r['invested']:>14.2f}"
            f"{r['current_value']:>14.2f}{r['gain_loss']:>+12.2f}"
            f"{r['gain_loss_pct']:>+8.2f}%"
        )
    print("-" * 92)
    print(
        f"{'TOTAL':<8}{'':>8}{'':>12}{'':>12}"
        f"{totals['invested']:>14.2f}{totals['current_value']:>14.2f}"
        f"{totals['gain_loss']:>+12.2f}{totals['gain_loss_pct']:>+8.2f}%"
    )
    print(line)

    status = "PROFIT" if totals["gain_loss"] >= 0 else "LOSS"
    print(f"Overall portfolio status: {status}")


def save_summary(rows, totals):
    """Append this run's results to portfolio_summary.csv (header added once)."""
    file_exists = os.path.exists(SUMMARY_FILE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fields = [
        "timestamp", "ticker", "quantity", "buy_price", "current_price",
        "invested", "current_value", "gain_loss", "gain_loss_pct",
    ]

    with open(SUMMARY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(fields)
        for r in rows:
            writer.writerow([
                timestamp, r["symbol"], f"{r['quantity']:g}",
                f"{r['buy_price']:.2f}", f"{r['current_price']:.2f}",
                f"{r['invested']:.2f}", f"{r['current_value']:.2f}",
                f"{r['gain_loss']:.2f}", f"{r['gain_loss_pct']:.2f}",
            ])
        writer.writerow([
            timestamp, "TOTAL", "", "", "",
            f"{totals['invested']:.2f}", f"{totals['current_value']:.2f}",
            f"{totals['gain_loss']:.2f}", f"{totals['gain_loss_pct']:.2f}",
        ])

    print(f"\nSummary saved to '{SUMMARY_FILE}'.")


# ------------------------------------------------------------------- main
def main():
    print("=" * 40)
    print("   STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 40)

    tickers = load_tickers()
    portfolio = collect_holdings(tickers)
    rows, totals = evaluate(portfolio)
    print_report(rows, totals)
    save_summary(rows, totals)


if __name__ == "__main__":
    main()
