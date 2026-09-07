from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Event(BaseModel):
    event_ref: str = Field(alias="eventRef")
    desc1: str
    desc2: str
    desc3: str
    alert_com: str = Field(alias="alertCom")  # ??
    cal_date: datetime = Field(alias="calDate")
    start: datetime
    end: datetime
    is_all_day: bool = Field(alias="isAllDay")
    duration_unit: str | None = Field(alias="durationUnit")
    legend_col: str | None = Field(alias="legendCol")
    loc_code: UUID = Field(alias="locCode")
    loc_add1: str = Field(alias="locAdd1")
    loc_add2: str | None = Field(alias="locAdd2")
    loc_add3: str | None = Field(alias="locAdd3")
    loc_add4: str | None = Field(alias="locAdd4")
    loc_add_post_code: str | None = Field(alias="locAddPostCode")
    loc_work_tel: str | None = Field(alias="locWorkTel")
    loc_post_code: str | None = Field(alias="locPostCode")
    attendance_exclude: bool = Field(alias="attendanceExclude")
    meeting: bool
    meeting_url: str | None = Field(alias="meetingUrl")
    teacher_name: str | None = Field(alias="teacherName", default=None)
    teacher_email: str | None = Field(alias="teacherEmail", default=None)


class CalendarEventsResponse(BaseModel):
    events: list[Event]
