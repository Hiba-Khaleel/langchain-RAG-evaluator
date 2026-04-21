---

title: "Reference Classes"

source: https://eiffel-guide.com/

source_heading_level: 3

---



## Reference Classes



When we define an object of a certain class, the computer will allocate memory to hold that class's attributes. However, in the case of a reference class, this allocated memory will only hold the references or addresses to the objects containing the actual values. So by default all attributes of a class will be set to Void, as the objects that the class refers to, do not exist yet. To create these we must always call create before using a new instance.

It is possible to test if an object x has been initialised yet by using the expression x = Void.

It is good style to use constructors to initialise attributes to the correct values and ensure that any class invariants are fulfilled. To enforce the use of constructors, we can specify features as possible constructors using the create keyword like so:

```eiffel
class
    MY_CLASS
create
    my_feature
feature
    my_feature (some_argument : STRING)
        do
            -- Do something here...
        end
end
```

An instance my_object of the class would then be initialised like so:

```eiffel
create my_object.my_feature("Hello World!")
```

You may specify as many constructors as you want. However, as soon as at least one constructor has been specified, a constructor must be used when creating a new instance. If no constructors are specified, then simply creating an object without adding a constructor will invoke default_create, which is a feature that is automatically added to every class without constructors and by default does nothing.

