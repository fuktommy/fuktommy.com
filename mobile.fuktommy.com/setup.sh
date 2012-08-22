#!/bin/sh -e

cd `dirname $0`
del sitemap.txt || true
mksitemap http://mobile.fuktommy.com/ . | sort > sitemap.txt

rsync -Cacv --delete \
    --exclude="*.ht" \
    --exclude="- /setup.sh" \
    --exclude="- /template" \
    --exclude="- /blog" \
    --exclude="- /blogsitemap.txt" \
    --exclude="- /sitemap_buzz.txt" \
    ./ /srv/www/mobile.fuktommy.com/
