# This file contains only the extra tests.
#
# The primary set of tests for Range is in file test_range.py (copied from Python's unit tests),
# whereas this file tests the extra features in Range and the compatability of slicing between
# Range and Python range.

import sys, unittest
sys. path. insert( 0, '..' )
from rangeplus import Range

class RangeTest(unittest.TestCase):

    # The following test verifies the compatibility of indexing/slicing operations between Range and range
    # and the proper indexing/slicing of unbound Range-s
    def test_slicing( self ):
        BIGGISH = 10000
        same = lambda a, b: a. start == b. start and ( a. stop == b. stop or ( a. stop is None and BIGGISH <= abs( b. stop ) + abs( b. step ))) and a. step == b. step
        range_cases = (( 10, 50, 3 ), ( 50, 10, -3 ), ( -10, 50, 3 ), ( 50, -10, -3 ), 
            ( -50, -10, 3 ), ( 10, 50, -3 ), ( 50, 10, 3 ),
            ( 0, 0, 1 ), ( 0, -1, 1 ), ( 0, -1, -1 ), ( -1, 0, 1 ), 
            ( -1, -1, 1 ), ( -1, -1, -1 ), ( 0, 1, 1 ), ( 1, 0, -1 ),
            ( 0, 1, -1 ), ( 1, 0, -1 ),
            ( 0, None, 1 ), ( 0, None, -1 ), ( 10, None, 7 ), ( 10, None, -7 ), 
            ( -10, None, 7 ), ( -10, None, -7 ))
        slice_cases = (( None, None ), ( 2, None ), ( None, 5 ), ( 0, None, 0 ),
            ( None, None, -7 ), ( None, 0, -7 ), ( None, None, 7 ), 
            ( 2, None, -7 ), ( None, None, -1 ), ( None, 0, -1 ), ( None, None, 1 ), 
            ( 2, 5 ), ( 2, 5, -1 ), ( -2, 5, -1 ), ( 2, -5 , -1 ), ( -2, -5 , -1 ),
            ( 20, 5 ), ( 2, 50 ), ( 20, 5, -1 ), ( 2, 50, -1 ), ( 2, 5, 5 ),
            ( -2, 5, 5 ), ( -2, -5 , 5 ), ( 20, 5, 5 ), ( 2, 50, 5 ), ( 2, 5, -5 ),
            ( -2, 5, -5 ), ( -2, -5 , -5 ), ( 20, 5, -5 ), ( 2, 50, -5 ))
        for _range in range_cases:
            r0 = Range( *_range )
            r1 = range( r0. start, r0. stop if r0. stop is not None else BIGGISH if r0. step > 0 else -BIGGISH, r0. step )
            for _slice in ( slice( *i ) for i in slice_cases ):
                # test handling of reversing an unbound Range
                if r0. stop is None and _slice. start is None and _slice. step is not None and _slice. step < 0:
                    self. assertRaises( ValueError, r0. __getitem__, _slice )
                # test handling of negative indices in an unbound Range
                elif r0. stop is None and (_slice. start is not None and _slice. start < 0 or _slice. stop is not None and _slice. stop < 0 ):
                    self. assertRaises( IndexError, r0. __getitem__, _slice )
                # test handling of a zero slice step
                elif _slice. step == 0:
                    self. assertRaises( ValueError, r0. __getitem__, _slice )
                else:
                    self. assertTrue( same( r0[ _slice ], r1[ _slice ]))

    def test_self_sameness( self ):
        range_cases = (( None, ), ( 1, None ), ( -1, None ), ( 10, None, 7 ),
            ( 0, None, -1 ), ( 0, None, -3 ), ( 10, None, -7 ), ( 10, None, -3 ),
            ( 2**200, ), ( 2**80 - 50, 2**80, 7 ), ( 2**80, 0 , -1 ))
        cases_len = len( range_cases )
        for i in range( cases_len ):
            r0 = Range( *range_cases[ i ])
            self. assertEqual( r0, Range( *range_cases[ i ]))
            for j in range( i + 1, cases_len ):
                self. assertNotEqual( r0, Range( *range_cases[ j ]))

    def test_range_sameness( self ):
        range_cases = (( 10, ), ( 1, 10 ), ( -1, 10 ), ( 10, 100, 7 ),
            ( 0, 100, -1 ), ( 0, -100, -3 ), ( 10, 0, -7 ), ( -10, -100, -3 ),
            ( 0, 2**63 - 1 ), ( 2**63 - 50, 2**63, 7 ), ( 2**63 - 1, 0, -1 ))
        cases_len = len( range_cases )
        for i in range( cases_len ):
            r0 = Range( *range_cases[ i ])
            self. assertEqual( r0, range( *range_cases[ i ]))
            for j in range( i + 1, cases_len ):
                self. assertNotEqual( r0, range( *range_cases[ j ]))

    def test_iterator( self ):
        def loop( r, c ):
            i = None
            for i in r:
                c -= 1
                if c == 0:
                    break
            return i
        cases = (( None, ), ( 0, None, -1 ), ( 50, None, 7 ),
            ( 50, None, -7 ), ( 1, 18, 2 ))
        COUNT = 10
        for x in cases:
            r = Range( *x )
            l = loop( r, COUNT )
            expect = r[ min( COUNT - 1, r. length - 1 ) if r. length is not None else COUNT - 1 ]
            self. assertEqual( l, expect )

    def test_intersect_bound( self ):
        cases = (
            (( 100, ), ( 100, )),
            (( 300, ), ( 200, )),
            (( 200, ), ( 300, )),
            (( 0, 300, 2 ), ( 0, 200, 3 )),
            (( 10, 300, 2 ), ( 15, 200, 3 )),
            (( 15, 300, 2 ), ( 10, 200, 3 )),
            (( 15, 200, 2 ), ( 10, 300, 3 )),
            (( 10, 200, 2 ), ( 16, 300, 3 )),
            (( 10, 300, 2 ), ( 16, 200, 3 )),
            (( 16, 300, 2 ), ( 10, 200, 3 )),
            (( 16, 200, 2 ), ( 10, 300, 3 )),
            (( 10, 300, 2 ), ( 17, 200, 3 )),
            (( 17, 300, 2 ), ( 10, 200, 3 )),
            (( 10, 300, 2 ), ( 18, 200, 3 )),
            (( 18, 300, 2 ), ( 10, 200, 3 )),
            (( 10, 300, 2 ), ( 11, 200, 2 )),
            (( 11, 300, 2 ), ( 10, 200, 2 )),
            (( 10, 300, 2 ), ( 16, 200, 2 )),
            (( 16, 300, 2 ), ( 10, 200, 2 )),
            (( 10, 300, 2 ), ( 17, 200, 2 )),
            (( -10, 300, 2 ), ( -16, 200, 3 )),
            (( -16, 300, 2 ), ( -10, 200, 3 )),
            (( 300, 10, -2 ), ( 200, 16, -3 )),
            (( 300, 10, -2 ), ( 201, 16, -3 )),
            (( 301, 10, -2 ), ( 200, 16, -3 )),
            (( 200, 10, -2 ), ( 300, 16, -3 )),
            (( 300, 16, -2 ), ( 200, 10, -3 )),
            (( 200, 16, -2 ), ( 300, 10, -3 )),
            (( 10, -300, -2 ), ( 16, -200, -3 )),
            (( -10, -300, -2 ), ( -16, -200, -3 )),
            (( 10, 300, 2 ), ( -16, -200, -3 )),
            (( -10, -300, -2 ), ( 16, 200, 3 )),
            (( 16, -300, -2 ), ( 10, 200, 3 )),
            (( 16, -300, -2 ), ( 200, 10, -3 )),
            (( -27, -300, -3 ), ( -16, -300, -2 )),
            (( 10, 100, 2 ), ( 100, 10, -2 )),
            (( 10, 100, 2 ), ( 100, 10, -3 )),
            (( 10, 100, 2 ), ( 10, -10, -3 )),
            (( 10, 100, 2 ), ( 11, -10, -3 )),
            (( 1, 500, 7 ), ( 2, 500, 11 )),
            (( 1, 500, 14 ), ( 2, 500, 22 )),
            (( 1, 500, 14 ), ( 3, 500, 22 )),
            (( 1, 500, 14 ), ( 300, -500, -22 )),
            (( 1, 500, 14 ), ( 1, 1, -22 )),
            (( 1, 500, -14 ), ( 1, 1, 22 )),
            (( 1, 1, -14 ), ( 1, 100, 22 )),
            (( 1, 1, 14 ), ( 100, 1, -22 )),
        )
        for t0, t1 in cases:
            r0, r1 = Range( *t0 ), Range( *t1 )
            self. assertEqual( set( r0 & r1 ), set( r0 ) & set( r1 ))

    def test_intersect_unbound( self ):
        def seek( r0, r1 ):
            patience, first = 5000, None
            for i in r0:
                patience -= 1
                if not patience:
                    return first, None
                elif i in r1:
                    if first is None:
                        first = i
                    else:
                        return first, i
            return first, None
        def last( r0, r1 ):
            current = 5000 if r0. length is None else r0. length
            while current:
                current -= 1
                if r0[ current ] in r1:
                    return r0[ current ]
            raise Exception( 'Never get here' )
        fix_stop = lambda: int( r0. step / abs( r0. step )) 
        cases = (
            (( 0, None, 1 ), ( 0, None, 1 )),
            (( 0, None, 1 ), ( 10, None, 1 )),
            (( 10, None, 1 ), ( 0, None, 1 )),
            (( 0, None, 5 ), ( 0, None, 7 )),
            (( 0, None, 5 ), ( 10, None, 7 )),
            (( 10, None, 5 ), ( 0, None, 7 )),
            (( 0, None, -1 ), ( 0, None, -1 )),
            (( 0, None, -1 ), ( 10, None, -1 )),
            (( 10, None, -1 ), ( 0, None, -1 )),
            (( 0, None, 1 ), ( 1000, None, -1 )),
            (( 1000, None, -1 ), ( 0, None, 1)),
            (( 0, None, 5 ), ( 1000, None, -7 )),
            (( 1000, None, -5 ), ( 0, None, 7 )),
            (( 0, None, 5 ), ( 0, 2000, 7 )),
            (( 0, None, 5 ), ( 10, 2000, 7 )),
            (( 0, None, -5 ), ( 10, -2000, -7 )),
            (( 10, None, 5 ), ( 0, 2000, 7 )),
            (( 0, None, 5 ), ( 1000, -2000, -7 )),
            (( 1000, None, -5 ), ( 0, 2000, 7 )),
            (( 0, 2000, 5 ), ( 0, None, 7 )),
            (( 0, 2000, 5 ), ( 10, None, 7 )),
            (( 0, -2000, -5 ), ( 10, None, -7 )),
            (( 10, 2000, 5 ), ( 0, None, 7 )),
            (( 0, 2000, 5 ), ( 1000, None, -7 )),
            (( 1000, -2000, -5 ), ( 0, None, 7 )),
            (( 0, None, 10 ), ( 0, None, 14 )),
            (( 0, None, -10 ), ( 0, None, -14 )),
            (( 0, None, 10 ), ( 0, 2000, 14 )),
            (( 0, None, 10 ), ( 10, 2000, 14 )),
            (( 0, None, -10 ), ( 10, -2000, -14 )),
            (( 10, None, 10 ), ( 0, 2000, 14 )),
            (( 0, None, 10 ), ( 1000, -2000, -14 )),
            (( 1000, None, -10 ), ( 0, 2000, 14 )),
            (( 0, 2000, 10 ), ( 0, None, 14 )),
            (( 0, 2000, 10 ), ( 10, None, 14 )),
            (( 0, -2000, -10 ), ( 10, None, -14 )),
            (( 10, 2000, 10 ), ( 0, None, 14 )),
            (( 0, 2000, 10 ), ( 1000, None, -14 )),
            (( 1000, -2000, -10 ), ( 0, None, 14 )),
            (( 0, None, 1 ), ( 0, None, -1 )),
        )
        for t0, t1 in cases:
            r0, r1 = Range( *t0 ), Range( *t1 )
            first, second = seek( r0, r1 )
            if first is None:
                result = Range( r0. start, r0. start, 1 )
            elif second is None:
                result = Range( first, first + fix_stop(), 1 )
            elif r0. stop is None and r1. stop is None and not(( r0. step > 0 ) ^ ( r1. step > 0 )):
                result = Range( first, None, second - first )
            else:
                result = Range( first, last( r0, r1 ) + fix_stop(), second - first )
        self. assertEqual( result, r0 & r1 )

    def test_cast( self ):
        cases = (( 10, ), ( -10, ), ( 10, 200, 13 ), ( 10, -200, -13 ))
        for case in cases:
            self. assertEqual( Range( range( *case )). range, range( *case ))
        cases, cast = (( None, ), ( 10, None, 7 ), ( 10, None, -7 ), ( 10.0, ), ( 7, 461, 34.0 )), lambda x: x. range
        for case in cases:
            self. assertRaises( ValueError, cast, Range( *case ))


if __name__ == "__main__":
    unittest.main()
