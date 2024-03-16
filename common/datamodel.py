from pydantic import BaseModel


class WorkReports(BaseModel):
    error: int
    text: str