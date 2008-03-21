#!/bin/sh -e

cd /srv/stage/mobile.fuktommy.com
del sitemap.txt || true
mksitemap http://mobile.fuktommy.com/ . | sort > sitemap.txt

rsync -Cacv --delete \
    --exclude="*.ht" \
    --exclude="- /setup.sh" \
    --exclude="- /template" \
    --exclude="- /blog" \
    --exclude="- /blogsitemp.txt" \
    ./ /srv/www/mobile.fuktommy.com/
