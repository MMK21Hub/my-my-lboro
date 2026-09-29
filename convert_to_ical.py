from collections.abc import Iterable

from ics import Calendar, Event

from my_lboro_types import Event as LboroEvent

def event_name(event: LboroEvent) -> str:
    # desc1 is module code, desc2 is module name, desc3 is event type
    name = f"{event.desc1}"
    if event.desc2:
        name += f" - {event.desc2}"
    if event.desc3:
        name += f" ({event.desc3})"
    return name
    


def convert_events_to_ical(events: list[LboroEvent]) -> Iterable[str]:
    calendar = Calendar()
    for lboro_event in events:
        description = [
            f"Module: {lboro_event.desc1} - {lboro_event.desc2}",
            f"Type: {lboro_event.desc3 or 'N/A'}",
            f"Lecturer: {lboro_event.teacher_name}",
        ]

        calendar.events.add(
            Event(
                name=event_name(lboro_event),
                begin=lboro_event.start,
                end=lboro_event.end,
                location=lboro_event.loc_add1,
                description="\n".join(description),
            )
        )

    return calendar.serialize_iter()
