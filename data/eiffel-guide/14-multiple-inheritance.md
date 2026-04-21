---

title: "Multiple Inheritance"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Multiple Inheritance



We have already seen, that classes can inherit features from other classes and redefine them to change their behaviour. We have also seen that classes may defer features to be implemented in a child class. However, when inheriting from multiple classes we run into another problem: clashes.

If a class C inherits from two classes A and B, which both have a feature called f then we will need to rename or undefine the feature for at least one of the two classes. For this we can use the rename and undefine keywords similarly to redefine. Consider the following implementation of the before mentioned problem:

```eiffel
class
    A

feature
    f
        do
            -- Some code...
        end
    g
        do
            -- Some code...
        end

end
```

```eiffel
class
    B

feature
    f
        do
            -- Some different code...
        end
    g
        do
            -- Some different code...
        end

end
```

```eiffel
class
    C

inherit
    A
        rename
            f as A_f    -- The feature f inherited from A is now called A_f within C
        end

    B
        undefine
            g           -- The feature g inherited from B is no longer part of C
        end

feature

    ...

end
```

In the above example, the feature f inherited from B is still called f in C, the same goes for the feature g inherited from A. So in conclusion, the class C now has the features A_f (inherited from A), f (inherited from B) and g (inherited from A).

If the classes A and B were inheriting the features f and g from the same class instead of defining them themselves, then in fact there is no need to undefine or rename any of the features, as there is only one effective implementation for them.

