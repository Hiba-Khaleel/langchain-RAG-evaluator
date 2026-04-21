---

title: "Control Structures"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Control Structures



In Eiffel the syntax for an if/elseif/else structure is as follows (notice: there are no brackets, and no then following the else):

```eiffel
if meaning_of_life = 42
then
    -- code if true
elseif meaning_of_life = 43
then
    -- code if only second condition is true
else
    -- code if all previous conditions are false
end
```

Eiffel also provides switch-like Statements called inspect, where a variable is compared to various values. The else condition is the default condition that applies when no case matches the input.

```eiffel
inspect input_integer
   when 2 then
        -- Code when input_integer equals 2
   when 3, 5 then
        -- Code when input_integer equals 3 or 5
   when 7..9 then
        -- Code when input_integer equals 7 or 8 or 9
   else
        -- Code when input_integer does not equal 2, 3, 5, 7, 8 nor 9
end
```

Unlike switch statements in other languages, in Eiffel the code following a matching case is not evaluated and there is no break statement in Eiffel.

