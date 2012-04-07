#!/usr/bin/python
"""Factorization into Prime Factors.

usage: primefactor <number>
"""
#
# Copyright (c) 2009 Satoshi Fukutomi <info@fuktommy.com>.
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

from __future__ import division

import doctest
import sys

__version__ = '$Revision$'


def factorize(n):
    """Factorization n into Prime Factors.

    sample:
    >>> factorize(0)
    []
    >>> factorize(1)
    []
    >>> factorize(2)
    [2]
    >>> factorize(4)
    [2, 2]
    >>> factorize(75)
    [3, 5, 5]
    """
    p = []
    i = 2
    while i <= n:
        tmp = n // i
        if tmp * i == n:
            p.append(i)
            n = tmp
        elif n < i * i:
            p.append(n)
            break
        elif i == 2:
            i += 1
        else:
            i += 2
    return p


def product(array):
    """Product of number in arrays.

    sample:
    >>> product([1, 2, 3])
    6
    """
    p = 1
    for n in array:
        p *= n
    return p


def _test():
    """Run doctest.
    """
    failure_count, test_count = doctest.testmod(verbose=True)
    if failure_count:
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: primefactor <number>')
    elif sys.argv[1] == '--test':
        _test()
        sys.exit()
    n = int(sys.argv[1])
    p = factorize(n)
    if product(p) == n:
        print p
    else:
        print 'error', p


if __name__ == '__main__':
    main()
