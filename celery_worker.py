from celery import Celery
from datetime import datetime
import os
from crew import FinancialAnalystCrew, CryptoCurrencyCrew

url = os.getenv("REDIS_URL")
celery = Celery(
        "tasks",
        backend=os.getenv("CELERY_RESULT_BACKEND", url),
        broker=os.getenv("CELERY_BROKER_URL", url),
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