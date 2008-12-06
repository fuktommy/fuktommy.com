#!/bin/sh -e

cd /srv/stage/hateber.fuktommy.com

rsync -Cacv --delete \
    ./ /srv/www/hateber.fuktommy.com/
