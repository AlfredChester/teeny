# Math
## Closures

| Closure   | Description |
|-----------|-------------|
| `abs(x)`    | return the absolute value of x |
| `floor(x)`  | return the closest integer of x that's smaller than x |
| `ceil(x)`   | return the closest integer of x that's bigger than x |
| `round(x)`  | round x to an integer |
| `trunc(x)`  | round x towards zero |
| `min(a, b)`    | return a if a < b, otherwise b |
| `max(a, b)`    | return a if a > b, otherwise b |
| `sign(x)`   | return 1 if x > 0, 0 if x is 0, -1 otherwise |
| `sin(x)`    | return sin(x) |
| `cos(x)`    | return cos(x) |
| `tan(x)`    | return tan(x) |
| `asin(x)`   | return arcsin(x) |
| `acos(x)`   | return arccos(x) |
| `atan(x)`   | return arctan(x) |
| `atan2(x, y)`   | return arctan of x / y, where both x and y's sign are considered, unlike atan(x / y) |
| `degrees(x)` | turn x from radians to degrees |
| `radians(x)` | turn x from degrees to radians |
| `exp(x)` | return e to the power of x |
| `pow(x, y)` | return x to the power of y |
| `log(x, b = e)` | return log_b(x) |
| `log10(x)` | return log10(x) |
| `log2(x)` | return log2(x) |
| `hypot(...)` | return the sum of square of each argument |
| `random()` | return a random number between 0.0 and 1.0, exclusive on left side and inclusive on the other |
| `uniform(x, y)` | return a random number between x and y, inclusive |
| `randint(x, y)` | return a random integer between x and y, inclusive |
| `clamp(x, upper, lower)` | return max(min(x, upper), lower) |
| `lerp(a, b, t)` | return a + (b - a) * t |
| `eq(a, b)` | return the value of expression a == b |
| `lt(a, b)` | return the value of expression a < b |
| `gt(a, b)` | return the value of expression a > b |
| `le(a, b)` | return the value of expression a <= b |
| `ge(a, b)` | return the value of expression a >= b |
| `neq(a, b)` | return the value of expression a != b |

> Note for eq, lt, gt, le, ge and neq
>
> Since it's possible to overload comparison operators, There's no guarentee that these closures will return a Number

## Constants

| Constants | Value | Description |
|-----------|-------|-------------|
| pi | 3.141592653589793 | |
| e | 2.718281828459045 | |
| tau | 6.283185307179586 | 2 times pi |

## Example Usage

```teeny
println(math.pi)           # 3.14159…
println(math.sin(0))       # 0
println(math.cos(math.pi)) # −1
```