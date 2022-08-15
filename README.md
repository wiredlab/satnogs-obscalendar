# satnogs-obscalendar
Create an iCal file for a set of SatNOGS observations for a ground station.


See an example for [SatNOGS Ground Station 834 - Valpo WIRED Lab 1](https://network.satnogs.org/stations/834/) at: https://agnd.net/dalian/calendar/ (temporary URL)


## Installation
You will need to install the packages listed in the `environment.yml` file.
That particular one is for a [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).
You can use other tools

`pip install requests requests-cache arrow ics` should also install the required packages.
**It is recommended** that you use a virtual environment of some sort.


## Usage

```bash
$ ./obscalendar.py -h

usage: obscalendar.py [-h] [-o OUTFILE] [--start START] [--end END] [--cache [SECONDS]]
                      gs [gs ...]

Create an iCalendar file of SatNOGS observations.

positional arguments:
  gs                    Ground station ID

options:
  -h, --help            show this help message and exit
  -o OUTFILE, --out OUTFILE
                        Output file (default stdout)
  --start START         Earliest observation start
  --end END             Latest observation end
  --cache [SECONDS]     Cache API requests (default: 300)
```

## Automatic updates

`do-updates.sh` is a script for using with `cron` that:
* Sets up the proper Python environment (with conda)
* Runs the script with the desired options
* Copies the ICS file to a server

`crontab` line:
```crontab
# m h  dom mon dow   command
07  *   *   *   *   time $HOME/path/to/do-updates.sh
```

The script is included here merely as an example and _must be modified_ for your situation.

