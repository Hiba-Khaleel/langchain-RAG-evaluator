---

title: "Once-executed features"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Once-executed features



Although quite rarely used, in Eiffel a feature can be specified to only be executed once then save its return value and simply return it immediately at every subsequent call. To do this, simply use the once keyword instead of do.

```eiffel
feature
    first_name: STRING
    last_name: STRING
    full_name: STRING
        once
            first_name := "John"
            last_name := "Doe"
            Result := first_name + " " + last_name
        end
```

This can be useful for initialisation. A setup feature could implement the initialisation of an object but be called from multiple other features. By using once, we can guarantee that it will only perform the initialisation once regardless of who calls it and how many times it is called.

It is also possible to specify in which context the feature should be considered as called. This is particularly important when using multiple threads or processes. For instance, you may want to execute a feature only once for each Process, once for each Thread or for every object instance. To specify this, use the once keys "PROCESS", "THREAD" and "OBJECT". These are specified as strings and in brackets after the once keyword like so: once ("PROCESS"). The default once key is "THREAD".

