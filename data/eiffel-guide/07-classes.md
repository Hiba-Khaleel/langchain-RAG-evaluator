---

title: "Classes"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Classes



The simplest way to define a class in Eiffel is just to name it and give it some features. It may even inherit features from other classes. For this we can list all of the desired classes after stating the inherit keyword. Using the redefine keyword features may be specified for classes that should be redefined in this class and not inherited.

```eiffel
class
    MY_CLASS

inherit
    SOME_OTHER_CLASS
        redefine
            some_inherited_feature
        end

feature
    some_feature
        do
            [...]
        end
    some_inherited_feature

[...]

end
```

When redefining a feature, it can be helpful to call its old version. So, within the redefinition, the keyword Precursor is set to the old version and calls can be made like this: Precursor("Some argument"). If you would like to use a version from a specific parent, you can add curly brackets: Precursor { SOME_PARENT } ("Some argument")

In the case of MY_CLASS, when we want to create an instance of the class, we first need to define the object and specify its type. Then, we use the create keyword to initialise the object, before making other calls to it. A client of the class might look like this:

```eiffel
feature
    example
        local
            New_object: MY_CLASS
        do
            create New_object
            New_object.some_feature
        end
```

