from pydantic import BaseModel


class AvitoPair(BaseModel):
    """
    model of a pair of Phrase and Region for '/add'
    """
    phrase: str  # Phrase to search for
    region: str  # region where the phrase should be monitored


