# rangeplus: Range()

### Extended Python Range Class

`Range` is a class that is compatible with Python [`range()`](https://docs.python.org/3/library/functions.html#func-range),
plus it implements the following extensions:

- The range can be unbound:

```
>>> from rangeplus import Range
>>> Range(None)               # zero to forever
Range(0, None)
>>> Range(20, None, 7)        # 20, 27, 34,...
Range(20, None, 7)
>>> Range(20, None, -7)       # 20, 13, 6, -1,...
Range(20, None, -7)
```

- The initial arguments don't have to be integers:

```
>>> from fractions import Fraction as frac
>>> tuple(Range(frac(1, 3), 2.5, frac(1, 6)))
(Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(5, 6), Fraction(1, 1),
Fraction(7, 6), Fraction(4, 3))
```

- Use the `&` operator to calculate the intersection (overlap) of ranges:

```
>>> Range(1, 100, 3) & Range(2, 100, 4)
Range(10, 100, 12)
>>> Range(1, None, 3) & Range(3, None, 4)
Range(7, None, 12)
>>> Range(200, -200, -7) & range(5, 80, 2)  # can intersect with Python range() too
Range(67, 4, -14)
```

- Solves the `maxsize` limits of `len()` by exporting the `.length` property:

```
>>> r0=range(2**200)
>>> len(r0)
<snip...>
OverflowError: Python int too large to convert to C ssize_t
>>> r1=Range(2**200)
>>> len(r1)
<snip...>
OverflowError: cannot fit 'int' into an index-sized integer
>>> r1.length
1606938044258990275541962092341162602522202993782792835301376
>>> Range(None).length is None      # get the length of an unbound range too
True
```

- Cast between `Range` and `range`:

```
>>> Range(range(20))
Range(0, 20)
>>> Range(20).range
range(0, 20)
```

- The `.args` property returns a tuple with the initialization arguments, which lets you do fun stuff:

```
>>> slice(*(Range(1, 100, 7) & Range( 2, 200, 5))[::-1].args)
slice(92, -13, -35)
```

### Notes

- Unbound `Range` obviously doesn't have negative indices, and can't be sliced unbound in reverse
order:

```
>>> Range(None)[10]
10
>>> Range(None)[-10]
<snip...>
IndexError: Negative index not allowed on unbound Range
>>> Range(None)[:10:-1]
<snip...>
ValueError: cannot reverse an unbound slice of an unbound Range
>>> Range(None)[20::-1]               # No problem if slice is bound
Range(20, -1, -1)
```

- While possible to initialize with floats, beware rounding issues, `Decimal` is better:

```
>>> tuple(Range(0.1, 2, 0.1))
(0.1, 0.2, 0.30000000000000004, 0.4, 0.5, 0.6, 0.7, 0.7999999999999999, 0.8999999999999999)
>>> from decimal import Decimal
>>> tuple(Range(Decimal('0.1'), 2, Decimal('0.1')))
(Decimal('0.1'), Decimal('0.2'), Decimal('0.3'), Decimal('0.4'), Decimal('0.5'), Decimal('0.
6'), Decimal('0.7'), Decimal('0.8'), Decimal('0.9'), Decimal('1.0'))
```

- Intersection is not guaranteed to return valid results if the `Range` was initialized with
non-integer values.

### Testing and Compatability

`Range` was developed aspiring for 100% compatibility with Python `range()`. Accordingly, it passes
Python's unit testing for `range()` with but very minor adaptations. You will find the Python unit
testing modified for `Range` in the `test` directory under the name `test_range.py`. This is the
original file copied from the Python source code repository with the nacessary adaptations commented
with double hash tags (`##`) so they can easily be searched for within the file.

In addition, a second file named `test_extra.py` in the `test` directory contains the additional
unit tests for features unique to `Range`.

Please be encouraged to offer additional test cases which you believe should be added.

### Installation

Install with `pip install rangeplus`, or copy `rangeplus.py` to your project (a single file with no
dependencies), or clone the project with `git clone https://github.com/avnr/rangeplus`.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=4UBXPG5PBJ76J)
Your financial support of this project will be highly appreciated!

### License

MIT License.
