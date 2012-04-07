#!/bin/sh -e

cd /srv/stage/hateber.fuktommy.com

rsync -Cacv --delete \
    --exclude="- /*.ht" \
    --exclude="- /setup.sh" \
    --exclude="- /template" \
    ./ /srv/www/hateber.fuktommy.com/
