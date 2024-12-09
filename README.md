### GCal Garmin Integration

Simple Google Calendar CLI I built for working with a configured calendar.

### Usage

```bash
# add full-day event
gcal add <name> --type=full [--desc=<description>] [--day=<day>] [--month=<month>] [--year=<year>]

# add partial-day event
gcal add <name> --type=partial [--desc=<description>] --starthour=<hour> --startminute=<minute> --endhour=<hour> --endminute=<minute> [--day=<day>] [--month=<month>] [--year=<year>]

# add multi-day event
gcal add <name> --type=multi [--desc=<description>] --startday=<day> --startmonth=<month> --startyear=<year> --endday=<day> --endmonth=<month> --endyear=<year>

# view events
gcal view [--startday=<day>] [--startmonth=<month>] [--startyear=<year>] [--endday=<day>] [--endmonth=<month>] [--endyear=<year>]
```

### Configuring

1. Create a `Google Cloud` project and add the `Google Calendar API`. Create a service account for the project, copy its email, and create new credentials in `Keys -> Add Key -> JSON`. Save `credentials.json` to your machine.

2. Go to `Google Calendar -> Settings -> Add calendar -> Create new calendar`, then navigate to `Settings and Sharing` for that calendar and share the calendar with the email of the service account, and give it `Make Changes to Events` permissions.

3. Clone this repository, then install packages in your desired environment.

```bash
git clone https://github.com/yourusername/gcal-cli.git
cd gcal-cli
pip install -r requirements.txt
```

4. Update the example script with the required variables.

```bash
cp gcal.example.sh gcal.sh
chmod +x gcal.sh
```

5. Copy it to your bin directory or set up an alias:

```bash
cp gcal.sh /usr/local/bin/gcal
alias gcal='/path/to/gcal.sh'
```
