#!/bin/sh -e

cd /srv/stage/bbs.fuktommy.com

rsync -Cacv --delete \
    --exclude="- /setup.sh" \
    --exclude="- /images" \
    ./ /srv/www/bbs.fuktommy.com/
