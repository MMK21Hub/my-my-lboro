from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional


class Event(BaseModel):
    event_ref: str = Field(alias="eventRef")
    desc1: str
    desc2: str
    cal_date: datetime = Field(alias="calDate")
    start: datetime
    end: datetime
    loc_code: UUID = Field(alias="locCode")
    loc_add1: str = Field(alias="locAdd1")
    attendance_exclude: bool = Field(alias="attendanceExclude")
    teacher_name: Optional[str] = Field(alias="teacherName", default=None)
    teacher_email: Optional[str] = Field(alias="teacherEmail", default=None)


class CalendarEventsResponse(BaseModel):
    events: list[Event]
