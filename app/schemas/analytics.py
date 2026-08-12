from datetime import date

from pydantic import BaseModel


class DailyTransactionResponse(BaseModel):
    currency: str
    transaction_count: int
    total_transaction_amount: float
    average_transaction_amount: float
    maximum_transaction_amount: float
    minimum_transaction_amount: float
    successful_transactions: int
    failed_transactions: int
    fraudulent_transactions: int
    average_fraud_score: float
    transaction_date: date


class MerchantPerformanceResponse(BaseModel):
    merchant_id: str
    merchant_name: str
    merchant_category: str
    merchant_city: str
    merchant_province: str
    currency: str
    transaction_count: int
    total_transaction_amount: float
    average_transaction_amount: float
    successful_transactions: int
    failed_transactions: int
    fraudulent_transactions: int
    average_fraud_score: float
    maximum_transaction_amount: float


class FraudAnalysisResponse(BaseModel):
    merchant_category: str
    payment_method: str
    fraud_status: str
    currency: str
    transaction_count: int
    total_transaction_amount: float
    average_transaction_amount: float
    average_fraud_score: float
    maximum_fraud_score: float
    minimum_fraud_score: float
    transaction_date: date