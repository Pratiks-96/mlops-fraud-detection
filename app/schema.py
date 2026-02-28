from pydantic import BaseModel


class FraudRequest(BaseModel):

    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float
