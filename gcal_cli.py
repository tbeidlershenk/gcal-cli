import argparse
from typing import NoReturn
from gcal_api import GoogleCalendarAPI
from datetime import date
import os

TODAY = date.today()

def error(message: str) -> NoReturn:
    print(f"Usage: {message}")
    exit(1)

def add_event(api: GoogleCalendarAPI, args):
    """Handles adding different types of events."""
    if args.type == "full":
        api.add_event_full_day(
            name=args.name.replace("_", " "),
            description=args.desc or "",
            day=args.day,
            month=args.month,
            year=args.year,
        )
    elif args.type == "partial":
        if not all([args.starthour, args.startminute, args.endhour, args.endminute]):
            error("For partial events, start and end times are required.")
        api.add_event_with_time(
            name=args.name.replace("_", " "),
            starthour=args.starthour,
            startminute=args.startminute,
            endhour=args.endhour,
            endminute=args.endminute,
            description=args.desc or "",
            day=args.day,
            month=args.month,
            year=args.year,
        )
    elif args.type == "multi":
        if not all([args.startday, args.startmonth, args.startyear, args.endday, args.endmonth, args.endyear]):
            error("For multi-day events, start and end dates are required.")
        api.add_multi_day_event(
            name=args.name.replace("_", " "),
            description=args.desc or "",
            startday=args.startday,
            startmonth=args.startmonth,
            startyear=args.startyear,
            endday=args.endday,
            endmonth=args.endmonth,
            endyear=args.endyear,
        )
    else:
        error("Invalid event type specified.")

def view_events(api: GoogleCalendarAPI, args):
    events = api.get_events(
        startday=args.startday or TODAY.day,
        startmonth=args.startmonth or TODAY.month,
        startyear=args.startyear or TODAY.year,
        endday=args.endday or TODAY.day,
        endmonth=args.endmonth or TODAY.month,
        endyear=args.endyear or TODAY.year,
    )
    if not events:
        print("No events found.")
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"{start}: {event['summary']}")

def main():
    parser = argparse.ArgumentParser(prog="gcal", description="Google Calendar CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add subcommand for 'add'
    add_parser = subparsers.add_parser("add", help="Add a new event")
    add_parser.add_argument("name", type=str, help="Name of the event")
    add_parser.add_argument("--type", required=True, choices=["full", "partial", "multi"], help="Event type")
    add_parser.add_argument("--desc", default=None, help="Event description")
    add_parser.add_argument("--day", type=int, help="Day for full/partial day events")
    add_parser.add_argument("--month", type=int, help="Month for full/partial day events")
    add_parser.add_argument("--year", type=int, help="Year for full/partial day events")
    add_parser.add_argument("--starthour", type=int, help="Start hour for partial day events")
    add_parser.add_argument("--startminute", type=int, help="Start minute for partial day events")
    add_parser.add_argument("--endhour", type=int, help="End hour for partial day events")
    add_parser.add_argument("--endminute", type=int, help="End minute for partial day events")
    add_parser.add_argument("--startday", type=int, help="Start day for multi-day events")
    add_parser.add_argument("--startmonth", type=int, help="Start month for multi-day events")
    add_parser.add_argument("--startyear", type=int, help="Start year for multi-day events")
    add_parser.add_argument("--endday", type=int, help="End day for multi-day events")
    add_parser.add_argument("--endmonth", type=int, help="End month for multi-day events")
    add_parser.add_argument("--endyear", type=int, help="End year for multi-day events")

    # Add subcommand for 'view'
    view_parser = subparsers.add_parser("view", help="View calendar events")
    view_parser.add_argument("--startday", type=int, help="Start day for viewing events")
    view_parser.add_argument("--startmonth", type=int, help="Start month for viewing events")
    view_parser.add_argument("--startyear", type=int, help="Start year for viewing events")
    view_parser.add_argument("--endday", type=int, help="End day for viewing events")
    view_parser.add_argument("--endmonth", type=int, help="End month for viewing events")
    view_parser.add_argument("--endyear", type=int, help="End year for viewing events")

    args = parser.parse_args()

    api = GoogleCalendarAPI(
        credentials_file=os.getenv("CREDENTIALS_FILE"),
        calendar_id=os.getenv("CALENDAR_ID"),
    )

    if args.command == "add":
        add_event(api, args)
    elif args.command == "view":
        view_events(api, args)

if __name__ == "__main__":
    main()
