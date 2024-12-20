from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
from crewai.project import CrewBase, agent , crew, task
import yfinance as yf
import os
groq_llm = LLM(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/mixtral-8x7b-32768",
)
ollamaLLM = LLM(
    model="ollama/openhermes", base_url="https://b51c-143-239-9-5.ngrok-free.app",
    temperature=0.2
)
llama31 = LLM(
    model="ollama/llama3.1", base_url="https://b51c-143-239-9-5.ngrok-free.app",
    temperature=0.2
)
openAI = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o"
)

@tool("yfinance_connector")
def yfinance_connector(stock_symbol: str) -> dict:
    """
    Retrieves comprehensive financial data for a company using its stock symbol.
    
    This tool fetches metrics such as:
    - Market Capitalization
    - Enterprise Value
    - Price-to-Earnings (P/E) Ratio
    - Price-to-Sales (P/S) Ratio
    - Price-to-Book (P/B) Ratio
    - EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization)
    - Revenue, Net Income, and Growth Rates
    - Dividend Yield and Payout
    - Operating and Profit Margins
    - Return on Assets (ROA) and Return on Equity (ROE)
    - Free Cash Flow
    - Debt-to-Equity Ratio
    - Current Ratio and Quick Ratio
    - Stock Volatility Metrics (Beta, 52-Week High/Low)
    - Trading Volume and more.
    
    :param stock_symbol: Stock ticker symbol (e.g., "AAPL" for Apple, "MSFT" for Microsoft).
    :return: A dictionary containing the retrieved financial metrics.
    """
    try:
        # Fetch stock data
        stock = yf.Ticker(stock_symbol)
        info = stock.get_info()  # Fetch all available metrics
        
        # Extract the relevant data
        relevant_data = {
            "Company Name": info.get("shortName", "N/A"),
            "Market Capitalization": info.get("marketCap", "N/A"),
            "Enterprise Value": info.get("enterpriseValue", "N/A"),
            "P/E Ratio": info.get("forwardPE", "N/A"),
            "P/S Ratio": info.get("priceToSalesTrailing12Months", "N/A"),
            "P/B Ratio": info.get("priceToBook", "N/A"),
            "EBITDA": info.get("ebitda", "N/A"),
            "Revenue": info.get("totalRevenue", "N/A"),
            "Revenue Growth": info.get("revenueGrowth", "N/A"),
            "Net Income": info.get("netIncomeToCommon", "N/A"),
            "Earnings Growth": info.get("earningsGrowth", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "Operating Margin": info.get("operatingMargins", "N/A"),
            "Profit Margin": info.get("profitMargins", "N/A"),
            "ROA": info.get("returnOnAssets", "N/A"),
            "ROE": info.get("returnOnEquity", "N/A"),
            "Free Cash Flow": info.get("freeCashflow", "N/A"),
            "Debt-to-Equity Ratio": info.get("debtToEquity", "N/A"),
            "Current Ratio": info.get("currentRatio", "N/A"),
            "Quick Ratio": info.get("quickRatio", "N/A"),
            "Beta": info.get("beta", "N/A"),
            "52-Week High": info.get("fiftyTwoWeekHigh", "N/A"),
            "52-Week Low": info.get("fiftyTwoWeekLow", "N/A"),
            "Average Volume": info.get("averageVolume", "N/A"),
        }
        
        return relevant_data
    
    except Exception as e:
        return {"error": str(e), "message": "Failed to fetch data for the stock symbol."}

@tool("crypto_info")
def crypto_info(stock_symbol: str) -> dict:
    """
    Retrieves comprehensive financial data for a crypto asset using its ticker symbol.
    
    This tool fetches metrics such as:
        ticker: The ticker symbol of the cryptocurrency (e.g., BTC-USD for Bitcoin).
        name: The name of the cryptocurrency (e.g., "Bitcoin" or "Ethereum").
        previousClose: The price at which the cryptocurrency closed during the previous trading session.
        regularMarketOpen: The price at which the cryptocurrency opened in the current trading session.
        dayLow: The lowest price of the cryptocurrency during the day.
        dayHigh: The highest price of the cryptocurrency during the day.
        regularMarketDayLow: The lowest price in the regular trading hours.
        regularMarketDayHigh: The highest price in the regular trading hours.
        volume: The total amount of cryptocurrency traded during the current trading session (includes all markets).
        regularMarketVolume: The trading volume specifically during regular market hours.
        averageVolume: The average trading volume over a longer historical period.
        averageVolume10days: The average trading volume over the past 10 days.
        fiftyTwoWeekLow: The lowest price of the cryptocurrency over the past 52 weeks.
        fiftyTwoWeekHigh: The highest price of the cryptocurrency over the past 52 weeks.
        fiftyDayAverage: The average price of the cryptocurrency over the last 50 days.
        twoHundredDayAverage: The average price of the cryptocurrency over the last 200 days.
        marketCap: The total market value of the cryptocurrency, calculated as current price × circulating supply.
        circulatingSupply: The number of cryptocurrency units that are currently available and circulating in the market.
    
    :param stock_symbol: crypto ticker symbol.
    :return: A dictionary containing the retrieved financial metrics.
    """
    try:
        # Fetch stock data
        stock = yf.Ticker(stock_symbol)
        info = stock.get_info()  # Fetch all available metrics
        
        
        crypto_data = {
            "ticker": stock_symbol,
            "name": info.get("name", "N/A"),
            "previousClose": info.get("previousClose"),
            "regularMarketOpen": info.get("regularMarketOpen"),
            "dayLow": info.get("dayLow"),
            "dayHigh": info.get("dayHigh"),
            "regularMarketDayLow": info.get("regularMarketDayLow"),
            "regularMarketDayHigh": info.get("regularMarketDayHigh"),
            "volume": info.get("volume"),
            "regularMarketVolume": info.get("regularMarketVolume"),
            "averageVolume": info.get("averageVolume"),
            "averageVolume10days": info.get("averageVolume10days"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyDayAverage": info.get("fiftyDayAverage"),
            "twoHundredDayAverage": info.get("twoHundredDayAverage"),
            "marketCap": info.get("marketCap"),
            "circulatingSupply": info.get("circulatingSupply"),
            }
        
        return crypto_data
    
    except Exception as e:
        return {"error": str(e), "message": "Failed to fetch data for the stock symbol."}

@CrewBase
class FinancialAnalystCrew():
    """FinancialAnalystCrew crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    
    
    @agent
    def company_research(self) -> Agent:
        return Agent(
            config = self.agents_config['company_researcher'],
            llm = openAI,
            tools=[yfinance_connector]
        )
    
    @agent
    def company_analyst(self) -> Agent:
        return Agent(
            config = self.agents_config['company_analyst'],
            llm = openAI,
            
        )
    @agent
    def investment_reccomender(self) -> Agent:
        return Agent(
            config = self.agents_config['company_reccomender'],
            llm=openAI
        )
    @agent
    def company_blogger(self) -> Agent:
        return Agent(
            config= self.agents_config['comapny_blogger'],
            llm = openAI
        )
    
    @task
    def research_company_task(self) -> Task:
        return Task(
            config = self.tasks_config['research_company_task'],
            agent = self.company_research()
        )
        
    @task
    def analyse_company_task(self)-> Task:
        return Task(
            config= self.tasks_config['analyse_company_task'],
            agent=self.company_analyst()
        )
        
    @task
    def investment_reccomendation_task(self)-> Task:
        return Task(
            config= self.tasks_config['investment_reccomendation_task'],
            agent= self.investment_reccomender()
        )
        
    @task
    def decision_blog_task(self)-> Task:
        return Task(
            config= self.tasks_config['decision_blog_task'],
            agent= self.company_blogger()
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the FinancialAnalystCrew crew"""
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process= Process.sequential,
        )

@CrewBase
class CryptoCurrencyCrew():
    """CryptoCurrency crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    @agent
    def company_research(self) -> Agent:
        return Agent(
            config = self.agents_config['crypto_researcher'],
            llm = openAI,
            tools=[crypto_info]
        )
    
    @agent
    def company_analyst(self) -> Agent:
        return Agent(
            config = self.agents_config['crypto_analyst'],
            llm = openAI,
            
        )
    @agent
    def investment_reccomender(self) -> Agent:
        return Agent(
            config = self.agents_config['company_reccomender'],
            llm=openAI
        )
    @agent
    def company_blogger(self) -> Agent:
        return Agent(
            config= self.agents_config['comapny_blogger'],
            llm = openAI
        )
    
    @task
    def research_company_task(self) -> Task:
        return Task(
            config = self.tasks_config['research_crypto_task'],
            agent = self.company_research()
        )
        
    @task
    def analyse_company_task(self)-> Task:
        return Task(
            config= self.tasks_config['analyse_crypto_task'],
            agent=self.company_analyst()
        )
        
    @task
    def investment_reccomendation_task(self)-> Task:
        return Task(
            config= self.tasks_config['crypto_reccomendation_task'],
            agent= self.investment_reccomender()
        )
        
    @task
    def decision_blog_task(self)-> Task:
        return Task(
            config= self.tasks_config['decision_blog_task'],
            agent= self.company_blogger()
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the CryptoCurrencyCrew crew"""
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process= Process.sequential,
        )