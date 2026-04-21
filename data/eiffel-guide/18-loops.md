---

title: "Loops"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Loops



This is the typical syntax for a simplified from loop (comparable to for loops in other languages):

```eiffel
from
    i := 0
until
    i >= 10
loop
    -- do something
    i := i + 1
end
```

Notice, that in Eiffel loops are evaluated until the conditional becomes true rather than while the conditional is true, which is common in most other languages (Ex. for-loop in C, Java, etc.).

It is also possible to add contracts to a from loop. The two options here are to specify a variant expression and an invariant expression. The variant must decrease by at least 1 after each cycle of the loop, while the invariant remains the same. Here is an example:

```eiffel
from
    i := 0
    n := 10
invariant
    n > 0
until
    i >= 10
loop
    i := i + 1
variant
    n-i
end
```

The contracts in loops are designed to prevent bugs such as endless loops. As such the variant is supposed to be an estimation of the number of iterations.

There also exists an "across"-loop, which goes through an iterable object (such as a list), and creates a cursor. Make sure that the object is in fact iterable. For this all elements must have a feature called next and the iterated object should have the features first and last. The cursor points to the next element of the iterated object at each execution of the loop. Since it is a cursor, you must access the actual elements by using my_cursor.item.

```eiffel
across list_of_customers as customer loop
    Io.put_string (customer.item.name)
    Io.new_line
end
```

For instance, an integer interval is an iterable object.

```eiffel
across 1 |..| 5 as it loop
    Io.put_integer (it.item)
    Io.new_line
end
```

