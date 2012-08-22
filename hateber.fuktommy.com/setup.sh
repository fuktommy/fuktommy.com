#!/bin/sh -e

cd `dirname $0`

rsync -Cacv --delete \
    --exclude="- /*.ht" \
    --exclude="- /setup.sh" \
    --exclude="- /template" \
    ./ /srv/www/hateber.fuktommy.com/
