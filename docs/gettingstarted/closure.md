# **Closure**

In Teeny, **closures** are essentially functions, just like in other programming languages. Closures are first-class citizens, meaning they can be stored in variables, passed around, and called just like any other value.

## **Constructing a Closure**

Defining a closure in Teeny is easy and straightforward:

```teeny
fn (a, b) a + b
```

This closure takes two parameters, `a` and `b`, and returns their sum.

Alternatively, you can define a closure with a block body:

```teeny
fn (a, b, c) {
    [a, b, c]
}
```

In this example, the closure returns a table with the three parameters.

You can also use the arrow (`=>`) syntax for short closures:

```teeny
(x, y) => x + y
```

This is a concise way of writing simple function literals.

## **Recursion with `this`**

Since closures don't have a name (like a function in other languages), **Teeny** uses the special keyword `this` to refer to the closure itself. This allows recursion — a function calling itself.

For example, to implement the Fibonacci sequence using recursion:

```teeny
fib := fn (a) match a {
    1: 1,
    2: 1,
    _: this(a - 1) + this(a - 2)  # calling itself
}
```

Here, `this(a - 1)` and `this(a - 2)` allow the closure to call itself recursively to calculate Fibonacci numbers.

## **Default Parameters**

You can assign **default values** to function parameters. If a parameter isn't provided when the closure is called, the default value will be used.

```teeny
greet := fn (name = "Guest") "Hello, {name}!"
```

Now, calling `greet()` will use `"Guest"` as the default value:

```teeny
greet()  # "Hello, Guest!"
greet("Alice")  # "Hello, Alice!"
```

## **Named Parameters**

Teeny supports **named parameters**, allowing you to specify which argument corresponds to which parameter by name when calling a closure.

```teeny
sum := fn (a, b) a + b
sum(a = 5, b = 10)  # 15
```

This makes it clear which values are being passed to which parameters, and allows you to call the closure with arguments in any order:

```teeny
sum(b = 10, a = 5)  # 15
```

## **Returning a Closure**

You can also return closures from other closures. This is useful for creating higher-order functions.

```teeny
makeAdder := fn (x) {
    fn (y) x + y
}

add5 := makeAdder(5)
add5(3)  # 8
```

Here, `makeAdder` returns a new closure that adds the value `x` to its argument `y`.

## **Anonymous Closures**

Since closures are first-class citizens, they don’t always need to be assigned to variables. They can be used directly in places where expressions are expected:

```teeny
for x in [1, 2, 3] {
    ((y) => println(y * 2))(x)  # anonymous closure within the loop
}
```

In this example, the closure `y => println(y * 2)` is created and immediately invoked with `x`.