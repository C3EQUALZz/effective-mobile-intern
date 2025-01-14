from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.base import BaseEntity
from app.domain.values.buy_step import Step


@dataclass(eq=False, slots=True)
class BuyStep(BaseEntity):
    step: Step
    date_step_begin: datetime
    date_step_end: datetime
