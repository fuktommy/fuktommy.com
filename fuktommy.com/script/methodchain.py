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
# $Id$
#

__version__ = '$Revision$'
__all__ = ['pack']


class MethodChainContainer:
    """Wrapper of Object for methods.
    """

    def __init__(self, val):
        """Wrap value.
        """
        self.val = val

    def func(self, function, *args):
        """Execute function with value and args.
        """
        array = [self.val]
        array.extend(args)
        return MethodChainContainer(function(*array))
    pipe = func

    def attr(self, attr_name):
        """Pack attributes of wrapped value.
        """
        return MethodChainContainer(getattr(self.val, attr_name))

    def method(self, method_name, *args):
        """Execute method with value and args.
        """
        array = [self.val]
        array.extend(args)
        return MethodChainContainer(getattr(self.val, method_name)(*args))

    def obj(self, method_name, *args):
        """Execute method with value and args and return packed object.
        """
        array = [self.val]
        array.extend(args)
        getattr(self.val, method_name)(*args)
        return self

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
    >>> pack(3).pipe(math.pow, 6).func(math.sqrt).unpack()
    27.0
    >>> pack('spam').method('upper').unpack()
    'SPAM'
    >>> pack(list('spam')).obj('sort').obj('reverse')
    ['s', 'p', 'm', 'a']
    >>> pack('spam').upper()
    'SPAM'
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

        def test_func(self):
            container = MethodChainContainer(9)
            result = container.func(math.sqrt)
            self.assertEquals(3, result.unpack())

        def test_pipe(self):
            container = MethodChainContainer(9)
            result = container.pipe(math.sqrt)
            self.assertEquals(3, result.unpack())

        def test_pipe_with_args(self):
            container = MethodChainContainer(9)
            result = container.pipe(math.pow, 2)
            self.assertEquals(81, result.unpack())

        def test_pipe_chain(self):
            container = MethodChainContainer(3)
            result = container.pipe(math.pow, 6).pipe(math.sqrt)
            self.assertEquals(27, result.unpack())

        def test_attr(self):
            container = MethodChainContainer('+')
            result = container.attr('join')
            self.assertEquals('o+o', result.unpack()('oo'))

        def test_method(self):
            container = MethodChainContainer('+')
            result = container.method('join', 'oo')
            self.assertEquals('o+o', result.unpack())

        def test_obj(self):
            container = MethodChainContainer(['1', '2', '3', '4'])
            result = container.obj('reverse').func(','.join)
            self.assertEquals('4,3,2,1', result.unpack())

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
