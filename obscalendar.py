#!/usr/bin/env python3

import argparse
import datetime
from pprint import pprint
import sys

import arrow
from ics import Calendar, Event
import requests
import requests_cache



OBSERVATIONS_API='https://network.satnogs.org/api/observations'
TRANSMITTERS_API='https://db.satnogs.org/api/transmitters'
SATELLITES_API='https://db.satnogs.org/api/satellites'


def date_or_reldays(s):
    """Accept an ISO 8601 date string or a signed integer as a date.

    ISO string -- attempt to convert it to UTC with Arrow
    integer -- days from now(), negative is past
    """
    try:
        days = int(s)
        d = arrow.utcnow().shift(days=days)
    except ValueError:
        d = arrow.get(s)
    return d.to('UTC').format('YYYY-MM-DDTHH:mm:ss')


parser = argparse.ArgumentParser(
    description='Create an iCalendar file of SatNOGS observations.')
parser.add_argument('gs', nargs='+', type=int,
                    help='Ground station ID')
parser.add_argument('-o', '--out', type=argparse.FileType('w'),
                    dest='outfile', default=sys.stdout,
                    help='Output file (default stdout)')
parser.add_argument('--start', type=date_or_reldays,
                    default=date_or_reldays(-7),
                    help='Earliest observation start')
parser.add_argument('--end', type=date_or_reldays,
                    help='Latest observation end')
parser.add_argument('--cache', nargs='?', metavar='SECONDS', type=int,
                    const=300,
                    help='Cache API requests (default: %(const)s)')

args = parser.parse_args()


print('gs:', args.gs)
print('outfile:', args.outfile)
print('start:', args.start)
print('end:', args.end)
print('cache:', args.cache)



# Handle cache option
if args.cache is not None:
    s = requests_cache.CachedSession('satnogs-obscalendar-cache',
                                     use_cache_dir=True,
                                     expire_after=args.cache)
    # requests-cache does not automatically remove expired responses, it only
    # replaces responses the next time they are requested
    s.remove_expired_responses()
else:
    s = requests.Session()




def get_observations(params, url=OBSERVATIONS_API):
    """Handle paginated results from /observations endpoint."""

    result = s.get(url, params=params)

    print(url)
    pprint(params)
    for obs in result.json():
        yield obs

    nextpage = result.links.get('next')
    while nextpage:
        pprint(nextpage)
        result = s.get(nextpage['url'])
        for obs in result.json():
            yield obs

        nextpage = result.links.get('next')



def create_calendar(args):
    cal = Calendar(creator='https://github.com/wiredlab/satnogs-obscalendar')
    for gs in args.gs:
        params = {'ground_station':gs,
                'start':args.start,
                'end':args.end,
                }

        for obs in get_observations(params):
            print(obs['start'])
            # get the transmitter information
            txid = obs['transmitter_uuid']
            response = s.get(TRANSMITTERS_API, params={'uuid':txid})
            transmitter = response.json()[0]  # query yields a list of length 1

            # get the satellite's information
            sat_id = transmitter['sat_id']
            response = s.get(SATELLITES_API, params={'sat_id':sat_id})
            satellite = response.json()[0]  # query yields a list of length 1

            e = Event()
            e.begin = obs['start']
            e.end = obs['end']
            e.name = satellite['name']
            e.description = f"""{obs['transmitter_downlink_low']/1e6:.3f} MHz
    {obs['transmitter_description']}
    """
            cal.events.add(e)
    return cal


if __name__ == '__main__':
    # do the deed
    cal = create_calendar(args)
    args.outfile.write(cal.serialize())

