---

title: "Exporting features"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Exporting features



By default all features defined in a class will be available to clients of the class. To prevent this, we can use {NONE} to keep features internal and inaccessible to clients. The Current keyword is considered a client. Hence, when using {NONE} for a feature, it will not be accessible using Current. This is similar to using private in Java for instance.

In fact, in Eiffel we can be very specific about which features are available to which clients, by specifying the class a client must have in order to access the feature. For this we once again use the curly brackets and list all the desired classes like so:

```eiffel
class
    A
feature   -- `s` will be available to all clients of the class.
    s
        ...
feature {NONE}   -- `u` and `v` will only be available internally.
    u, v
        ...
feature {A, B}   -- `x` will only be available to clients of the same type
    x            -- and to clients of the type `B`.
        ...
feature {C}   -- `y` and `z` will be available only to clients of the type C.
    y, z
        ...
end
```

One more thing to consider is, that creation procedures are not considered qualified calls. Therefore, when using a feature as a constructor, where it is exported to does not apply. if you would like to still specify which features are available to which classes, you can use the same notation, but with the create declaration.

