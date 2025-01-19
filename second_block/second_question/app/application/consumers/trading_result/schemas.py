from datetime import date

from pydantic import BaseModel


class ParseAllBulletinsSphinxRequest(BaseModel):
    start_date: date
    end_date: date
