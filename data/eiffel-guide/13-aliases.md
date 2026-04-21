---

title: "Aliases"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Aliases



When using a custom class to store data, it can be useful to use operators in order to compare objects of that class. For this we must define a feature that performs the comparison and is an alias for an operator. We use the alias keyword after the feature name to choose the operator. In this example, people will be compared according to their age:

```eiffel
class
    PERSON

feature
    name: STRING
    age: INTEGER

    older_than alias ">" (other: PERSON) : BOOLEAN
        do
            Result := (age > other.age)
        end

end
```

If we now had an instance of the class called Joe with the age 36 and another called Tom with the age 24, then Joe > Tom is true, while Tom > Joe is false.

