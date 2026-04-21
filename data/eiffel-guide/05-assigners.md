---

title: "Assigners"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Assigners



The variables of a class are read-only to its clients. To change their values, we can use a setter, a feature that takes the new value as an argument, like in the case of set_age below:

```eiffel
class
    PERSON
feature
    age: INTEGER
    set_age ( new_age: INTEGER )
        do
            age := new_age
        end
end
```

So, a client of the class would not be able to change the age by using Person.age := 21, as Person.age is read-only for clients. Instead it would call Person.set_age(21). However, if for some reasons you are feeling radical and want to use Person.age := 21, you can give age a so called assigner by using the assign keyword and specifying a setter.

```eiffel
class
    PERSON
feature
    age: INTEGER assign set_age
    set_age ( new_age: INTEGER )
        do
            age := new_age
        end
end
```

Now, Person.age := 21 is simply a shortcut for Person.set_age(21).

