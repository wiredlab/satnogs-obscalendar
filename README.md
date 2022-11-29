# satnogs-obscalendar
Create an iCal file for a set of SatNOGS observations for a ground station.


See an example for [SatNOGS Ground Station 834 - Valpo WIRED Lab 1](https://network.satnogs.org/stations/834/) at: [example](https://agnd.net/dalian/calendar/) (temporary URL)


## Installation

There are two options prepared for installing the needed packages: virtualenv
and conda.


### virtualenv

Option 1:: manual

```bash
# create a new environment in the root of the repository
virtualenv venv

# activate the new environment
source venv/bin/activate

# ensure pip is from the new environment under folder: venv/bin/pip
which pip
# install packages
pip install -r requirements.txt
```

---


Option 2:: with [direnv](https://direnv.net/) (my favorite)

```bash
# (set up direnv in your shell, see its docs)

# declare the .envrc as safe to run
# (the .envrc file is already in the repository)
direnv allow

# ensure pip is from the new environment under folder: .direnv/bin/pip
which pip

# if so, then install the packages
pip install -r requirements.txt
```


### conda

Install the packages listed in the `environment.yml` file to create a [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

```bash
conda env create -f environment.yml

# activate the environment
conda activate obscalendar
```


### System python

**It is recommended** that you use a virtual environment of some sort instead
of installing packages system- or user-wide.

`pip install requests requests-cache arrow ics` should also install the required packages.



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

The script is included here merely as an example and **must be modified** for your situation.

