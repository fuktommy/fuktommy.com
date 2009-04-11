<?php
//
// Copyright (c) 2009 Satoshi Fukutomi <info@fuktommy.com>.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
// 1. Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE AUTHORS AND CONTRIBUTORS ``AS IS'' AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
// OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
// HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
// LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
// OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
// SUCH DAMAGE.
//
// $Id:$
//

require_once 'PHPUnit/Framework.php';

error_reporting(E_ALL | E_STRICT);

require_once 'ModifireChain.php';


/**
 * Mock Object.
 */
interface ObjectMock
{
    public function foo($format);
}


/**
 * Test of Wrapper.
 * @package ModifireChain
 */
class WrapperTest extends PHPUnit_Framework_TestCase
{
    /**
     * Get wrapped value.
     */
    public function testUnpack()
    {
        $wrapper = ModifireChain_Wrapper::getInstance(100);
        $this->assertSame(100, $wrapper->unpack());
    }

    /**
     * Call Function.
     */
    public function testFunc()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('%03d');
        $this->assertSame('012', $wrapper->func('sprintf', 12)->unpack());
    }
 
    /**
     * Call testMethod
     */
    public function testMethod()
    {
        $obj = $this->getMock('ObjectMock');
        $obj->expects($this->once())
            ->method('foo')
            ->with('arg')
            ->will($this->returnValue('bar'));
        $wrapper = ModifireChain_Wrapper::getInstance($obj);
        $this->assertSame('bar', $wrapper->method('foo', 'arg')->unpack());
    }
 
    /**
     * Call undefined methods.
     */
    public function testCallFunction()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('%03d');
        $this->assertSame('012', $wrapper->sprintf(12)->unpack());
    }
 
    /**
     * Call undefined methods.
     */
    public function testCallMethod()
    {
        $obj = $this->getMock('ObjectMock');
        $obj->expects($this->once())
            ->method('foo')
            ->with('arg')
            ->will($this->returnValue('bar'));
        $wrapper = ModifireChain_Wrapper::getInstance($obj);
        $this->assertSame('bar', $wrapper->foo('arg')->unpack());
    }
 
    /**
     * Call undefined methods.
     */
    public function testCallUndefinedFunction()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('foo');
        $this->assertSame(null, $wrapper->undefinedfunction('arg')->unpack());
    }
 
    /**
     * Date format using strftime.
     */
    public function testDateFormat()
    {
        $wrapper = ModifireChain_Wrapper::getInstance(strtotime('2009-04-11'));
        $this->assertSame('2009-04-11', $wrapper->dateFormat('%Y-%m-%d')->unpack());
    }

    /**
     * Return default value if wrapped value is false.
     */
    public function testDefaultsNotReplaced()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('bar');
        $this->assertSame('bar', $wrapper->defaults('foo')->unpack());
    }

    /**
     * Return default value if wrapped value is false.
     */
    public function testDefaultsReplaced()
    {
        $wrapper = ModifireChain_Wrapper::getInstance(null);
        $this->assertSame('foo', $wrapper->defaults('foo')->unpack());
    }

    /**
     * Escape value.
     */
    public function testEscapeHtml()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('<br>');
        $this->assertSame('&lt;br&gt;', $wrapper->escape()->unpack());
        $this->assertSame('&lt;br&gt;', $wrapper->escape('html')->unpack());
    }

    /**
     * Escape value.
     */
    public function testEscapeUrl()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('/ a');
        $this->assertSame('%2F%20a', $wrapper->escape('url')->unpack());
    }

    /**
     * Escape value.
     */
    public function testEscape()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('<br>');
        $this->assertSame('<br>', $wrapper->escape('invalidParameter')->unpack());
    }

    /**
     * Replace by regexp.
     */
    public function testRegexReplace()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('abcde');
        $this->assertSame('axxxe', $wrapper->regexReplace('/[b-d]/', 'x')->unpack());
    }

    /**
     * Replace by string.
     */
    public function testReplace()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('abcde');
        $this->assertSame('axyze', $wrapper->replace('bcd', 'xyz')->unpack());
    }

    /**
     * String format.
     */
    public function testStringFormat()
    {
        $wrapper = ModifireChain_Wrapper::getInstance(100);
        $this->assertSame('100.0', $wrapper->stringFormat('%.1f')->unpack());
    }

    /**
     * Print value.
     */
    public function testPrint()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('<br>');
        ob_start();
        $result = $wrapper->p();
        $output = ob_get_contents();
        ob_end_clean();
        $this->assertSame($wrapper, $result);
        $this->assertSame('<br>', $output);
    }

    /**
     * Print escaped value.
     */
    public function testEcho()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('<br>');
        ob_start();
        $result = $wrapper->e();
        $output = ob_get_contents();
        ob_end_clean();
        $this->assertSame($wrapper, $result);
        $this->assertSame('&lt;br&gt;', $output);
    }

    /**
     * Print escaped value.
     */
    public function testEchoHtml()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('<br>');
        ob_start();
        $result = $wrapper->e('html');
        $output = ob_get_contents();
        ob_end_clean();
        $this->assertSame($wrapper, $result);
        $this->assertSame('&lt;br&gt;', $output);
    }

    /**
     * Print escaped value.
     */
    public function testEchoUrl()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('/ a');
        ob_start();
        $result = $wrapper->e('url');
        $output = ob_get_contents();
        ob_end_clean();
        $this->assertSame($wrapper, $result);
        $this->assertSame('%2F%20a', $output);
    }

    /**
     * Get iterator.
     */
    private function myTestGetIterator($value, $expected)
    {
        $wrapper = ModifireChain_Wrapper::getInstance($value);
        $i = 0;
        foreach ($wrapper as $k => $v) {
            $this->assertSame($i, $k);
            $this->assertSame($expected[$i], $v->unpack());
            $i++;
        }
        $this->assertSame(count($expected), $i);
    }

    /**
     * Get iterator.
     */
    public function testGetIterator()
    {
        $this->myTestGetIterator(array(1, 2, 3), array(1, 2, 3));
        $this->myTestGetIterator(new ArrayIterator(array(1, 2, 3)), array(1, 2, 3));
        $this->myTestGetIterator(1, array(1));
        $this->myTestGetIterator(array(), array());

        $aggregate = $this->getMock('IteratorAggregate');
        $aggregate->expects($this->once())
                  ->method('getIterator')
                  ->will($this->returnValue(new ArrayIterator(array(1, 2, 3))));
        $this->myTestGetIterator($aggregate, array(1, 2, 3));
    }

    /**
     * Get array element.
     */
    public function testGet()
    {
        $wrapper = ModifireChain_Wrapper::getInstance(array('a' => 'b'));
        $this->assertSame('b', $wrapper->get('a')->unpack());
    }

    /**
     * Get array element.
     */
    public function testGetNull()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('a');
        $this->assertSame(null, $wrapper->get('a')->unpack());
    }

    /**
     * Get object field.
     */
    public function testField()
    {
        $obj = new StdClass();
        $obj->foo = 'bar';
        $wrapper = ModifireChain_Wrapper::getInstance($obj);
        $this->assertSame('bar', $wrapper->foo->unpack());
    }

    /**
     * Get object field.
     */
    public function testFieldNull()
    {
        $obj = new StdClass();
        $wrapper = ModifireChain_Wrapper::getInstance($obj);
        $this->assertSame(null, $wrapper->foo->unpack());
    }

    /**
     * Get object field.
     */
    public function testFieldScalar()
    {
        $wrapper = ModifireChain_Wrapper::getInstance('foo');
        $this->assertSame(null, $wrapper->foo->unpack());
    }
}
