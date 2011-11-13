"""GC debug utilities
"""
#
# Copyright (c) 2011 Satoshi Fukutomi <info@fuktommy.com>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHORS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# $Id$
#

import gc

__version__ = "$Revision$"
__all__ = ['debug_print']


class ObjectSet:
    def __init__(self):
        self.objects = []

    def includes(self, obj):
        for o in self.objects:
            if o is obj:
                return True
        return False

    def update(self, objects):
        self.objects = objects


_object_set = ObjectSet()
_counter = {}
gc.set_debug(gc.DEBUG_UNCOLLECTABLE)


def debug_print(verbose = False):
    collect = gc.collect()
    counter = {}
    objects = gc.get_objects()
    for i in objects:
        t = str(type(i))
        counter[t] = counter.get(t, 0) + 1
        if not verbose:
            continue
        if isinstance(i, dict) and len(i) and not _object_set.includes(i):
            print '[GC]', i.keys()[0]
        if isinstance(i, list) and len(i) and not _object_set.includes(i):
            print '[GC]', str(i)[0:60]
        if isinstance(i, tuple) and len(i) and not _object_set.includes(i):
            print '[GC]', str(i)[0:60]
    tmp = {}
    for k in counter.keys():
        if _counter.get(k, 0) != counter[k]:
            tmp[k] = counter[k] - _counter.get(k, 0)
            _counter[k] = counter[k]
    print '[GC]', collect, len(objects), len(gc.garbage), tmp
    if verbose:
        _object_set.update(objects)
