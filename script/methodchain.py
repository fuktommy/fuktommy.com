"""Method Chain Container
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
# $Id:$
#

__version__ = '$Revision:$'
__all__ = ['pack']


class MethodChainContainer:
    """Wrapper of Object for methods.
    """

    def __init__(self, val):
        """Wrap value.
        """
        self.val = val

    def pipe(self, method, *args):
        """Execute method with value and args.
        """
        array = [self.val]
        array.extend(args)
        return MethodChainContainer(method(*array))

    def unpack(self):
        """Content value.
        """
        return self.val

    def __getattr__(self, name):
        """Access attributes of wrapped value.
        """
        return getattr(self.val, name)


def pack(val):
    """Pack value into Method chain container.

    example:
    >>> import math
    >>> pack(9).pipe(math.pow, 6).pipe(math.sqrt).unpack()
    729.0
    >>> int(pack(9))
    9
    """
    return MethodChainContainer(val)


def _test():
    """Run unittest and doctest.
    """
    import doctest
    import math
    import sys
    import unittest

    class MethodChainContainerTest(unittest.TestCase):
        def test_unpack(self):
            container = MethodChainContainer(9)
            self.assertEquals(9, container.unpack())

        def test_pipe(self):
            container = MethodChainContainer(9)
            result = container.pipe(math.sqrt)
            self.assertEquals(3, result.unpack())

        def test_pipe_with_args(self):
            container = MethodChainContainer(9)
            result = container.pipe(math.pow, 2)
            self.assertEquals(81, result.unpack())

        def test_pipe_chain(self):
            container = MethodChainContainer(9)
            result = container.pipe(math.pow, 6).pipe(math.sqrt)
            self.assertEquals(729, result.unpack())

        def test_getattr(self):
            container = MethodChainContainer(9)
            self.assertEquals('9', str(container))

        def test_getattr_AttributeError(self):
            container = MethodChainContainer(9)
            try:
                len(container)
            except AttributeError:
                return
            else:
                fail()

    class PackTest(unittest.TestCase):
        def test_pack(self):
            container = pack(9)
            self.assertEquals(9, container.unpack())

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MethodChainContainerTest))
    suite.addTest(unittest.makeSuite(PackTest))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.errors or result.failures:
        sys.exit(1)

    failure_count, test_count = doctest.testmod(verbose=True)
    if failure_count:
        sys.exit(1)


if __name__ == '__main__':
    _test()
