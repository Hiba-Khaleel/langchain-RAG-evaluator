---

title: "Contracts"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Contracts



Contracts are a concept used in Eiffel to avoid bugs. Although these should be disabled in a production runtime, during development they can be quite useful. There are three types of assurance elements: preconditions (used in features), postconditions (used in features) and class invariants.

Preconditions are defined using the require keyword. They should contain a tag and a boolean expression. Postconditions are written the same way, but we use the ensure keyword. We can use the old notation to compare a variable's value to its value before the feature was executed. Here is an example that might be used in the BAKERY class we saw above:

```eiffel
number_of_available_cakes : INTEGER

buy_cakes (amount : INTEGER)

    require
        positive_amount: amount > 0    -- Check that amount is a positive number

    do
        number_of_available_cakes = number_of_available_cakes - amount

    ensure
        amount_reduced: number_of_available_cakes = old number_of_available_cakes - amount
            -- Check that the number of available cakes has decreased correctly

    end
```

Class invariants are checked every time an operation is performed on the class, such as calling a feature. We declare class invariants using the invariant keyword. In this example we will check that a variable is always positive:

```eiffel
class
    MY_CLASS

feature
    some_number : INTEGER
    some_feature
        do
            -- Some code here...
        end

invariant
    positive: some_number > 0

end
```

