from models.batch_request import BatchRequest

class AnalyzeRequest(BatchRequest):
    operation: str = "analyze"
