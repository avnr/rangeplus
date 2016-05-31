#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    rangeplus - Extended Python Range Class
#    Copyright (c) 2016 Avner Herskovits
#
#    MIT License
#
#    Permission  is  hereby granted, free of charge, to any person  obtaining  a
#    copy of this  software and associated documentation files (the "Software"),
#    to deal in the Software  without  restriction, including without limitation
#    the rights to use, copy, modify, merge,  publish,  distribute,  sublicense,
#    and/or  sell  copies of  the  Software,  and to permit persons to whom  the
#    Software is furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this  permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT  WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE  WARRANTIES  OF  MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR  ANY  CLAIM,  DAMAGES  OR  OTHER
#    LIABILITY, WHETHER IN AN  ACTION  OF  CONTRACT,  TORT OR OTHERWISE, ARISING
#    FROM,  OUT  OF  OR  IN  CONNECTION WITH THE SOFTWARE OR THE  USE  OR  OTHER
#    DEALINGS IN THE SOFTWARE.
#

# determine if a value can be treated as a number
_calculateable = lambda value: type( value ) in ( int, float ) or \
    all( hasattr( value, attr ) for attr in
    ( '__eq__', '__ne__', '__gt__', '__ge__', '__lt__', '__le__',
    '__add__', '__floordiv__', '__mod__', '__mul__', '__sub__' ))

def _normalize( value, msg ):
    if _calculateable( value ):
        return value
    elif hasattr( value, '__index__' ):
        return _normalize( value. __index__(), msg )
    raise TypeError( msg )

class Range:
    """
    Range(stop) -> Range object
    Range(start, stop[, step]) -> Range object

    Return a sequence of numbers from start to stop by step,
    start defaults to 0, step defaults to 1.
    When stop is None the Range is unbound.
    All arguments must be calculateable, i.e., implement maths ops
    +, -, *, %, // and all comparisons, or implement an __index__
    method that returns a calculateable
    """

    def __init__( self, *args ):
        """
        Initilize self
        """
        normalize = lambda value: _normalize( value, '%s object cannot be interpreted as an integer' % ( type( value ), ))
        normalize_stop = lambda value: None if value is None else normalize( value )
        # calculate start, stop and step
        if len( args ) is 0:
            raise TypeError( 'Range expected 1 arguments, got 0' )      # argument(s) sic., same text as Python range
        elif len( args ) is 1:
            if type( args[ 0 ]) is range:
                self. _start, self. _stop, self. _step = args[ 0 ]. start, args[ 0 ]. stop, args[ 0 ]. step
            else:
                self. _start, self. _stop, self. _step = 0, normalize_stop( args[ 0 ]), 1
        elif len( args ) is 2:
            self. _start, self. _stop, self. _step = normalize( args[ 0 ]), normalize_stop( args[ 1 ]), 1
        elif len( args ) is 3:
            self. _start, self. _stop, self. _step = normalize( args[ 0 ]), normalize_stop( args[ 1 ]), normalize( args[ 2 ])
            if self. _step == 0:
                raise ValueError( 'Range() arg 3 must not be zero' )
        else:
            raise TypeError( 'Range expected at most 3 arguments, got %s' % ( len( args ), ))
        # calculate the length
        if self. _stop is None:
            self. _length = None
        elif ( self. _start == self. _stop ) or (( self. _start < self. _stop ) ^ ( self. _step > 0 )):
            self. _length = 0
        else:
            self. _length = ( abs( self. _stop - self. _start ) - 1 ) // abs( self. _step ) + 1

    @property
    def start( self ): return self. _start

    @property
    def stop( self ): return self. _stop

    @property
    def step( self ): return self. _step

    @property
    def length( self ): return self. _length

    @property
    def range( self ):
        if self. _is_range_compatible:
            return range( self. _start, self. _stop, self. _step )
        raise ValueError( 'Range objct cannot be cast to range' )

    @property
    def args( self ):
        return ( self. _start, self. _stop, self. _step )

    def __getitem__( self, key ):
        """
        Return self[key] or self[start:stop:step]
        Index values must be of a calculateable type.
        Negative indices not allowed on unbound Range.
        When reversing an unbound Range the slice must be bound.
        """
        # Handle slice notation
        if type( key ) is slice:
            normalize = lambda value: value if value is None \
                else _normalize( value, 'slice indices must be integer-like or None or have an __index__ method' )
            start, stop, step = normalize( key. start ), normalize( key. stop ), normalize( key. step )
            if step == 0:
                raise ValueError( 'slice step cannot be zero' )
            # Bound range
            if self. _length is not None:
                indices = slice( start, stop, step ). indices( self. _length )
                return Range(
                    self. _start + self. _step * indices[ 0 ],
                    self. _start + self. _step * indices[ 1 ],
                    self. _step * indices [ 2 ])
            # Unbound range
            fix_stop = 0
            if step is None:
                step = 1
            if start is None and step < 0:
                raise ValueError( 'cannot reverse an unbound slice of an unbound Range' )
            if stop is None and step < 0:
                stop, fix_stop = 0, self. _step
            if start is not None and start < 0 or stop is not None and stop < 0:
                raise IndexError( 'Negative index not allowed on unbound Range' )
            # Unbound slice
            if stop is None:
                return Range( self[ start ] if start is not None else self. _start, None, self. _step * step )
            # Bound slice
            indices = slice( start, stop, step ). indices( 2 * stop if start is None else 2 * max( start, stop ))
            return Range(
                self. _start + self. _step * indices[ 0 ],
                self. _start + self. _step * indices[ 1 ] - fix_stop,
                self. _step * indices [ 2 ])
        # handle index notation
        index_in_range = lambda value: self. _length is None and ( value is None or 0 <= value ) or \
            self. _length is not None and self. _length != 0 and -self. _length <= value < self. _length
        key = _normalize( key, 'Range indices cannot be %s' % ( type( key ), ))
        if self. _length is None and key < 0:
            raise IndexError( 'Negative index not allowed on unbound Range' )
        elif not index_in_range( key ):
            raise IndexError( 'Range object index out of range' )
        if key < 0:
            key += self. _length
        return self. _start + self. _step * key

    def _value_in_range( self, value ):
        if self. _stop is None:
            return (( self. _step > 0 and self. _start <= value ) or
                ( self. _step < 0 and value <= self. _start )) and \
                0 == ( value - self. _start ) % self. _step
        return (( self. _step > 0 and self. _start <= value < self. _stop ) or
            ( self. _step < 0 and self. _stop < value <= self. _start )) and \
            0 == ( value - self. _start ) % self. _step

    # Check if self can be cloned to a regular Python range
    #
    # Needed in the fringe cases where one wants to use __contains__(), count() or index(),
    # using an argument that is not a number, just a filter, using the basic Sequence
    # implementation of a linear search. Such a search is obviously irrelevant when Range is unbound.
    # In addition, such a search is very inefficient on large ranges. Therefore, in order to maintain
    # compatability with Python range at reasonable efficiency, we will clone self to a Python
    # range and use the latter's implementation which is written in C and which is dozens-fold faster
    # then the equivalent Python implementation, at the cost of being able to provide this capability
    # only if Range's start/stop/step are ints.
    #
    # In most cases, the argument to __contains__(), count() and index() will be a number and the result
    # will be calculated numerically with no need for this fallback.
    @property
    def _is_range_compatible( self ):
        return type( self. _start ) is int and type( self. _stop ) is int and type( self. _step ) is int

    def __contains__( self, value ):
        """
        Return value in self
        Optimize if value is calculateable, search linearly otherwise
        """
        if type( value ) is complex and value. imag == 0:
            value = value. real
        if _calculateable( value ):
            return self. _value_in_range( value )
        elif hasattr( value, '__eq__' ):
            if self. _is_range_compatible:
                return range( self. _start, self. _stop, self. _step ). __contains__( value )
            else:
                raise ValueError( 'cannot perform a linear search on this object' )
        return False

    def count( self, value ):
        """
        self.count(value) -> integer
        Return number of occurrences of value in self
        Optimize if value is calculateable, search linearly otherwise
        """
        if type( value ) is complex and value. imag == 0:
            value = value. real
        if _calculateable( value ):
            return 1 if self. _value_in_range( value ) else 0
        elif hasattr( value, '__eq__' ):
            if self. _is_range_compatible:
                return range( self. _start, self. _stop, self. _step ). count( value )
            else:
                raise ValueError( 'cannot perform a linear search on this object' )
        return 0

    def index( self, value ):
        """
        self.index(value) -> integer
        Return index of value in self
        Optimize if value is calculateable, search linearly otherwise
        """
        if type( value ) is complex and value. imag == 0:
            value = value. real
        if _calculateable( value ):
            if self. _value_in_range( value ):
                return ( value - self. _start ) // self. _step
            raise ValueError( '%s is not in Range' % ( value, ))
        elif hasattr( value, '__eq__' ):
            if self. _is_range_compatible:
                return range( self. _start, self. _stop, self. _step ). index( value )
            else:
                raise ValueError( 'cannot perform a linear search on this object' )
        raise ValueError( '%s is not in Range' % ( value, ))

    # According to Python range's implementation, range_a==range_b when tuple(range_a)==tuple(range_b)
    def __eq__( self, other ):
        """
        Return self==other
        """
        other_type = type( other )
        if other_type is Range:
            other_len = other. length
        elif other_type is range:
            other_len = len( other )
        else:
            if not all( hasattr( other, attr ) for attr in ( '__len__', 'start', 'step' )):
                return False
            try:
                other_len = len( other )
            except:
                if not hasattr( other, 'length' ):
                    return False
                other_len = other. length
        return self. _length == other_len and \
            ( self. _length == 0 or ( self. _start == other. start and ( self. _length == 1 or self. _step == other. step )))

    def __ne__( self, other ):
        """
        Return self!=other
        """
        return not self. __eq__( other )

    # According to Python range's implementation, range_a==range_b when tuple(range_a)==tuple(range_b)
    def __hash__( self ):
        """
        Return hash(self)
        """
        return hash( tuple() ) if self. _length == 0 \
            else hash(( self. _start, )) if self. _length == 1 \
            else hash(( self. _start, self. _step, self. _length ))

    def __iter__( self ):
        """
        Return iter(self)
        """
        return Range_iterator( self. _start, self. _length, self. _step )

    def __reversed__( self ):
        """
        Return reversed(self)
        Not applicable on unbound range
        """
        if self. _length is None:
            raise ValueError( 'cannot reverse an unbound Range' )
        return Range_iterator( self. _start + self. _step * ( self. _length - 1 ), self. _length, - self. _step )

    def __len__( self ):
        """
        Return len(self)
        This method doesn't support unbound Range
        Please use Range.length to get the length of any Range including unbound
        """
        if self. _length is None:
            raise AttributeError( 'len() not available on unbound Range, please use Range.length instead' )
        return self. _length

    def __repr__( self ):
        """
        Return repr(self)
        """
        if self. _step == 1:
            return 'Range(%s, %s)' % ( self. _start, self. _stop )
        return 'Range(%s, %s, %s)' % ( self. _start, self. _stop, self. _step )

    def __and__( self, other ):
        """
        Calculate the intersect of the two linear sets described by Range/range
        objects and return the result as a Range object.
        """
        # Return a triple (g, x, y), where ax + by = g = gcd(a, b)
        def egcd( a, b ):
            x, y, u, v = 0, 1, 1, 0
            while a:
                q, r = b // a, b % a
                m, n = x - u * q, y - v * q
                b, a, x, y, u, v = a, r, u, v, m, n
            return b, x, y
        # more helpers
        stop_min = lambda x, y: None if x is None and y is None else x if y is None else y if x is None else min( x, y )
        stop_max = lambda x, y: None if x is None or y is None else max( x, y )
        stop_max_inv = lambda x, y: None if x is None and y is None else x if y is None else y if x is None else max( x, y )
        # return empty Range if either ranges is empty
        empty = lambda: Range( self. _start, self. _start, self. _step * other. step )
        if 0 == self. _length:
            return empty()
        try:
            if 0 == other. length:
                return empty()
        except:     # in case "other" is Python range
            if 0 == len( other ):
                return empty()
        # align both ranges in same direction
        if self. _step > 0 and other. step < 0:
            if self. _start > other. start:     # return empty result
                return empty()
            elif other. stop is None:
                other = Range( Range( other. start, self. _start - 1, other. step )[ -1 ], other. start + 1, - other. step )
            else:
                other = Range( Range( other. start, stop_max( self. _start - 1, other. stop ), other. step )[ -1 ], other. start + 1, - other. step )
        elif self. _step < 0 and other. step > 0:
            if self. _start < other. start:     # return empty result
                return empty()
            elif other. stop is None:
                other = Range( Range( other. start, self. _start + 1, other. step )[ -1 ], other. start - 1, - other. step )
            else:
                other = Range( Range( other. start, stop_min( self. _start + 1, other. stop ), other. step )[ -1 ], other. start - 1, - other. step )
        # now both directions are the same
        step0, step1, sign, offset = abs( self. _step ), abs( other. step ), ( self. _step > 0 ) - ( self. _step < 0 ), other. start - self. _start
        gcd, x, y = egcd( step0, step1 )
        interval0, interval1 = step0 // gcd, step1 // gcd           # calculate the coprime intervals
        step = interval0 * interval1 * gcd * sign
        if offset % gcd != 0:                           # return empty result if offset not alligned on gcd
            return empty()
        # Apply Chinese Remainder Theorem
        crt = ( offset * interval0 * ( x % interval1 )) % step    # x % interval1 means inverse_mod( interval0, interval1 )
        filler = 0
        if sign > 0 and offset > 0 or sign < 0 and offset < 0:
            gap = offset - crt
            filler = gap if 0 == gap % step else ( gap // step + 1 ) * step
        start = self. _start + crt + filler
        stop = stop_min( self. _stop, other. stop ) if sign > 0 else stop_max_inv( self. _stop, other. stop )
        return Range( start, stop, step )


# The following iterator class does nothing more than a generator, however
# it is implemented as a standalone class so that the iterations can be pickeled
# (generators can't be pickled).
class Range_iterator:
    """
    Implement a Range object iterator
    """

    def __init__( self, current, count, step ):
        """
        Initialize the iterator
        """
        self. current, self. count, self. step = current - step, count, step

    def __iter__( self ):
        """
        Return iter(self) -> self
        """
        return self

    def __next__( self ):
        """
        Return next(self)
        """
        if self. count == 0:
            raise StopIteration
        self. current += self. step
        if self. count is not None:
            self. count -= 1
        return self. current
