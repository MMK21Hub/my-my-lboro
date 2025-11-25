# My myLboro

Access your Loughborough University timetable through an iCal link (compatible with Google Calendar, Apple Calendar, and basically any other calendar app!)

## Development instructions

You'll need Python and `uv`.

1. Clone repo
2. Create `.env`
3. Run `uv run fastapi dev`
4. Test it by going to <http://127.0.0.1:8000/lboro.ics>
