import os 
from dotenv import load_dotenv
import datetime
import json
import yfinance as yf
from flask import Flask, request, jsonify
load_dotenv()
from crew import FinancialAnalystCrew, CryptoCurrencyCrew


app = Flask(__name__)

def is_valid_ticker(ticker_symbol: str) -> bool:
    """
    Check if a ticker symbol is valid.

    Args:
        ticker_symbol (str): Stock ticker symbol.

    Returns:
        bool: True if the ticker symbol is valid, otherwise False.
    """
    try:
        # Fetch ticker information
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        # Check if valid info is returned (e.g., company name or other essential field)
        if info and "longName" in info:
            return True
        else:
            print(f"No valid information available for {ticker_symbol}.")
            return False
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return False

def stock_reccomendation(symbol : str):
    inputs={
        "company_name": symbol,
        "date": datetime.datetime.now().strftime("%d-%m-%Y")
    }
    output = FinancialAnalystCrew().crew().kickoff(inputs=inputs)
    return output.raw

def crypto_reccomendation(symbol :str):
    inputs={
        "company_name" : symbol,
        "date": datetime.datetime.now().strftime("%d-%m-%Y")
    }
    output = CryptoCurrencyCrew().crew().kickoff(inputs=inputs)
    return output.raw

@app.route("/analyze_stock", methods=["POST"])
def analyze_ticker():
    """
    Endpoint to analyze a ticker symbol for technology stocks.

    Request body:
        {
            "ticker_symbol": "AAPL"
        }

    Returns:
        JSON response with the analysis result or an error message.
    """
    data = request.get_json()
    ticker_symbol = data.get("ticker_symbol", "").strip()

    if not ticker_symbol:
        return jsonify({"error": "Ticker symbol is required."}), 400

    if is_valid_ticker(ticker_symbol):
        try:
            output = stock_reccomendation(symbol=ticker_symbol)
            return jsonify({"ticker_symbol": ticker_symbol, "analysis": output})
        except Exception as e:
            return jsonify({"error": f"An error occurred while analyzing the ticker: {e}"}), 500
    else:
        return jsonify({"error": f"{ticker_symbol} is not a valid technology sector ticker."}), 400

@app.route("/analyze_crypto", methods=["POST"])
def analyze_crypto():
    """
    Endpoint to analyze a ticker symbol for technology stocks.

    Request body:
        {
            "ticker_symbol": "BTC-USD"
        }

    Returns:
        JSON response with the analysis result or an error message.
    """
    data = request.get_json()
    ticker_symbol = data.get("ticker_symbol", "").strip()

    if not ticker_symbol:
        return jsonify({"error": "Ticker symbol is required."}), 400

    if is_valid_ticker(ticker_symbol):
        try:
            output = crypto_reccomendation(symbol=ticker_symbol)
            return jsonify({"ticker_symbol": ticker_symbol, "analysis": output})
        except Exception as e:
            return jsonify({"error": f"An error occurred while analyzing the ticker: {e}"}), 500
    else:
        return jsonify({"error": f"{ticker_symbol} is not a valid technology sector ticker."}), 400
    
if __name__ == "__main__":
    app.run(debug=True)
