# **Control Flow**

## `if` and `match`

Teeny provides `if` and `match` for branching logic.

### `if`

`if` in Teeny works similarly to most languages:

```teeny
a := 2
if a == 1 {
    println("a equals to 1!")
} elif a == 2 {
    println("a equals to 2!")
} else {
    println("a is neither 1 nor 2!")
}
```

Since `if` is an expression, it can be used where values are expected:

```teeny
result :=
    if a > 0 {
        "positive"
    } else {
        "non-positive"
    }
```

### `match`

`match` is a more expressive alternative to chained `if` statements. It compares a value against a series of **patterns**:

```teeny
a := 3
match [a % 3, a % 5] {
    [0, 0]: "fizzbuzz",
    [0, _]: "fizz",
    [_, 0]: "buzz",
    _:      a
}
```

* `_` is a wildcard pattern that matches anything.
* Table patterns compare element by element.

#### **Patterns in `match`**

Patterns describe the *shape* or *property* of a value. A pattern either **matches** or it doesn’t; it does not introduce new variable bindings — it only checks structure or evaluates logic.

##### Wildcard

`_` matches **anything**:

```teeny
match x {
    _: "always matched"
}
```

##### Literal Patterns

Match values that are exactly equal:

```teeny
match x {
    0: "zero",
    "ok": "a string",
    _: "something else"
}
```

##### Table Patterns

Table patterns must match a table of the same shape:

```teeny
match [1, 2, 3] {
    [1, 2, 3]: "exact match",
    _:         "no match"
}
```

Nested patterns also work:

```teeny
match [1, [2, 3]] {
    [1, [2, 3]]: "nested match",
    _:          "no match"
}
```

Elements can be replaced with `_` to ignore parts:

```teeny
match [1, 2, 3] {
    [1, _, 3]: "first and last match",
    _:        "otherwise"
}
```

##### Logical Pattern Operators

You can combine patterns using logical operators:

1. OR (`||`)

Matches if either subpattern matches:

```teeny
match x {
    1 || 2: "one or two",
    _:     "other"
}
```

2. AND (`&&`)

Matches only if both patterns match the same value:

```teeny
match t {
    [_, 0] && [0, _]: "both patterns hold",
    _:               "otherwise"
}
```

3. NOT (`!`)

Matches if the pattern does *not* match:

```teeny
match x {
    ![0, _]: "not a pair starting with 0",
    _:      "otherwise"
}
```

##### Predicate Patterns (Function Literals)

If a pattern is a **function literal**, Teeny treats it as a predicate:

```teeny
match x {
    (v) => v % 2 == 0: "even",
    _:                 "odd or non-number"
}
```

This works as:

* Teeny calls the pattern function with the matched value.
* If the result is *truthy*, the pattern matches.
* Otherwise it does not.

> To avoid ambiguity, this only applies when you define the function *inline* in the pattern. A named function or variable referring to a function won’t be auto-called.

##### Combined Example

```teeny
a := 3; b := 5

match [a, b] {
    [0, 0]:                    "Both zero",
    [1, _] || [_, 1]:          "One of them is 1",
    ![_, [_, _]]:              "Second isn’t a pair",
    (xy) => xy[0] == 3:        "First element is 3",
    _:                         "Default"
}
```

## **`for` and `while`**

Loops in Teeny are also expressions.

### `for`

Use `for` to iterate over tables or strings:

```teeny
for x in [1, 2, 3] {
    println(x)
}
```

Structural unpacking works in loops too:

```teeny
pairs := [[1, "Alice"], [2, "Bob"]]

names :=
    for [id, name] in pairs {
        name
    }

println(names)  # ["Alice", "Bob"]
```

Since `for` is an expression, it returns a **table of results**:

```teeny
squares :=
    for x in 1..5 {
        x * x
    }

println(squares)  # [1, 4, 9, 16]
```

### `while`

`while` keeps running as long as its condition is truthy:

```teeny
i := 0

while i < 5 {
    println(i)
    i = i + 1
}
```

A `while` expression returns the **last value evaluated** inside its body.

### **Loop Control: `break` and `continue`**

You can use `break` or `continue` inside loops:

```teeny
for x in [1,2,3,4,5] {
    if x == 3 {
        continue
    }
    if x == 5 {
        break
    }
    println(x)
}
```

* `continue` skips to the next iteration.
* `break` stops the loop early.

Because loops are expressions, `break` and `continue` can carry values.

```teeny
result :=
    for x in [1,2,3] {
        if x == 2 {
            break "found 2"
        }
    }

println(result)  # [nil, "found 2"]
```