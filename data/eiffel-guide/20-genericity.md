---

title: "Genericity"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Genericity



This is a concept that is particularly useful when creating structures like lists. Using genericity we can define classes with generic types that can be specified later. Like this we can use the same class to make a list of strings and to make a list of integers for instance.

To use this in a class, the we can specify a generic parameter (ex. G) in in square brackets after the class name like so class MY_CLASS [G]. Then when defining an object of this class er must specify which class to use for the generic type like this: my_object: MY_CLASS[ STRING ]. This is a more detailed example of a generic class:

```eiffel
class MY_LIST [G] feature

    first : G
    last : G
    extend (new_element: G)
        do
            -- Add element to list...
        end

end
```

```eiffel
class SCHOOL feature

    list_of_students : MY_LIST[ STUDENT ]
    list_of_classes : MY_LIST[ MY_LIST[ STUDENT ] ]

end
```

