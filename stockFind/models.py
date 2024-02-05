from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Stock:
    _id: str
    ticker: str
    company: str
    bought: bool = False
    amtInvested: int = 0


@dataclass
class User:
    _id: str
    email: str
    password: str
    stocks: list[str] = field(default_factory=list)
