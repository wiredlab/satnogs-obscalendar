#/bin/bash

# Update SatNOGS observations schedule
#
# 2022 Dan White <dan.white@valpo.edu>
#
# MIT License (https://opensource.org/licenses/MIT)

# Script that I use with cron to create a calendar ICS file and sync it to my
# server.  From the server, there are other scripts that use the file.
#
# In the repository for my convenience and for an example of how the tool is
# used.


cd /home/dan/ed/satnogs/satnogs-obscalendar

# Configure the Conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate obscalendar

# add cache to speed up the lookups of transmitters and satellites
./obscalendar.py --start=-14 --cache=300 --out=satnogs-obscalendar.ics 834 
sleep 0.1
rsync -avuz \
    -e "ssh -i $HOME/.ssh/volta-tesla_satnogs-obscalendar" \
    ./satnogs-obscalendar.ics \
    dan@agnd.net:
#                ^^^
#   This is blank because authorized_keys on the remote end looks like:
#     command="$HOME/bin/rrsync -wo /var/www/www.agnd.net/tmp/",no-agent-forwarding,no-port-forwarding,no-pty,no-user-rc,no-X11-forwarding ssh-rsa ...
#
#   which only allows a write to the named folder.
#   Since the folder is named already at the remote side, any paths added are
#   implicity under that structure, hence, the empty path.

