#!/bin/sh -e

cd `dirname $0`
del rss.rdf sitemap.txt recent.js || true
mkrss -h head.txt > rss.rdf
mksitemap https://fuktommy.com/ . | sort > sitemap.txt
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
    --exclude="- /aafont" \
    --exclude="- /genpasswd/index.html" \
    --exclude="- /head.txt" \
    --exclude="- /setup.sh" \
    --exclude="- /smarty" \
    --exclude="- /template" \
    --exclude="- /tropy/t/xml" \
    ./ /srv/www/fuktommy.com/

rsync -Cacv --delete \
    ./smarty/ /srv/templates/fuktommy.com/
