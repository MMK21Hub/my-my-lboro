from typing import Iterable
from my_lboro_types import Event as LboroEvent
from ics import Calendar, Event


def convert_events_to_ical(events: list[LboroEvent]) -> Iterable[str]:
    calendar = Calendar()
    for lboro_event in events:
        description = [
            f"Class: {lboro_event.desc2}",
            f"Lecturer: {lboro_event.teacher_name}",
        ]

        calendar.events.add(
            Event(
                name=lboro_event.desc1,
                begin=lboro_event.start,
                end=lboro_event.end,
                location=lboro_event.loc_add1,
                description="\n".join(description),
            )
        )

    return calendar.serialize_iter()
