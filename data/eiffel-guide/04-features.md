---

title: "Features"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Features



In Eiffel, the Methods and Attributes (Variables) of a class are called features. We can define them by using the keyword feature followed by the features name within a class. We specify the features type or return type by using a colon followed by the types name. If a feature is a function and takes arguments we can list them in brackets together with their types. The keyword do is used to denote where the code of the function starts, followed by end at the end.

```eiffel
class
    BAKERY

feature

    number_of_cakes : INTEGER
        -- A variable containing an integer

    name_of_my_favourite_cake : STRING
        -- A variable containing a string

    price_of_one_cake : REAL
        -- A variable containing a floating point number

    buy_cake (price : REAL; flavour : STRING)   -- A function accepting arguments
        do
            -- Some code here...
        end

    is_cake_available : BOOLEAN   -- A function returning true or false
        do
            Result := number_of_cakes > 0
        end

end
```

The return value of a feature is set by assigning it to the Result variable. Unlike other languages, the return statement does not exist.

Also notice that, when defining a feature, arguments are separated using semi-colons. However, when calling the feature, they are separated by means of a comma.

Features may also use local variables which are internal to the function. However, they must be declared with their type before the do keyword using the local keyword. For example:

```eiffel
class
    MY_CLASS
feature
    my_feature
        local
            my_variable_1 : INTEGER
            my_variable_2 : STRING
        do
            -- Some code here...
        end
end
```

