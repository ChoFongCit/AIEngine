from celery import Celery
from datetime import datetime
import os
from crew import FinancialAnalystCrew, CryptoCurrencyCrew

celery = Celery(
        "tasks",
        backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
)



# Define tasks
@celery.task
def stock_reccomendation_task(symbol: str):
    inputs = {
        "company_name": symbol,
        "date": datetime.now().strftime("%d-%m-%Y")
    }
    output = FinancialAnalystCrew().crew().kickoff(inputs=inputs)
    return output.raw

@celery.task
def crypto_reccomendation_task(symbol: str):
    inputs = {
        "company_name": symbol,
        "date": datetime.now().strftime("%d-%m-%Y")
    }
    output = CryptoCurrencyCrew().crew().kickoff(inputs=inputs)
    return output.raw