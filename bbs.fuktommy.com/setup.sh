#!/bin/sh -e

cd `dirname $0`

rsync -Cacv --delete \
    --exclude="- /setup.sh" \
    --exclude="- /images" \
    ./ /srv/www/bbs.fuktommy.com/
