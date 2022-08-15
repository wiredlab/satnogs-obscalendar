#/bin/bash

# update SatNOGS observations schedule

cd /home/dan/ed/satnogs/satnogs-obscalendar

# Configure the Conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate obscalendar

# add cache to speed up the lookups of transmitters and satellites
./obscalendar.py --start=-9 --cache=300 --out=satnogs-obscalendar.ics 834 
sleep 0.1
rsync -avuz \
    -e "ssh -i $HOME/.ssh/volta-tesla_satnogs-obscalendar" \
    ./satnogs-obscalendar.ics \
    dan@agnd.net:
#                ^^^
#   This is blank because authorized_keys on the remote end
#   looks like:
#     command="$HOME/bin/rrsync -wo /var/www/www.agnd.net/tmp/",no-agent-forwarding,no-port-forwarding,no-pty,no-user-rc,no-X11-forwarding ssh-rsa ...
#   which only allows a write to the named folder.
#   Since the folder is named already at the remote side, any paths added are
#   implicity under that structure, hence, the empty path.

