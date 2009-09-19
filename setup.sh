#!/bin/sh -e

cd /srv/stage/fuktommy.com
del rss.rdf sitemap.txt recent.js || true
mkrss -h head.txt > rss.rdf
mksitemap http://fuktommy.com/ . | sort > sitemap.txt
rss2js rss.rdf > recent.js

rsync -Cacv --delete \
    --exclude="*.ht" \
    --exclude="*.gz" \
    --exclude="*.bz2" \
    --exclude="*.zip" \
    --exclude="*.lzh" \
    --exclude="*.pdf" \
    --exclude="*.pyc" \
    --exclude="README.html" \
    --exclude="- /setup.sh" \
    --exclude="- /smarty" \
    --exclude="- /template" \
    --exclude="- /tropy/t/xml" \
    ./ /srv/www/fuktommy.com/

rsync -Cacv --delete \
    ./smarty/ /srv/templates/fuktommy.com/
