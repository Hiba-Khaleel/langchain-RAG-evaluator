---

title: "Deferred Classes"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Deferred Classes



Above we had a look at how classes can inherit and export features. Deferred classes have the capability to specify features without defining them, so that children of the class must themselves define them.

As soon as a class contains at least one deferred feature, it must be declared as deferred (notice the deferred keyword before class). A feature can be declared as deferred by using the deferred keyword, followed immediately by the end statement. A deferred feature does not have to be declared as redefined in a child class.

```eiffel
deferred class
    MY_CLASS

feature
    some_feature: STRING
    another_feature
        deferred
        end

end
```

