---

title: "Agents"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Agents



Particularly in event-driven programming, it can be useful to represent a feature using an object. For this we can use agents. We create an agent by using the agent keyword followed by the features we want to pass. To call the feature encapsulated by an agent object we use my_agent.call() if we expect no return value. To receive a return value we use my_agent.item() instead.

The following example is similar to a situation that might occur when programming a GUI. When run, the application prints "The button was clicked!".

```eiffel
class
    APPLICATION

create
    run

feature

    run
        local
            button : BUTTON
        do
            create button.set_click_handler( agent click_event )
            button.click
        end

    click_event
        do
            Io.put_string ("The button was clicked!")
        end

end
```

```eiffel
class
    BUTTON

create
    set_click_handler

feature

    click_handler : PROCEDURE [APPLICATION, TUPLE[]]

    set_click_handler ( handler: PROCEDURE [APPLICATION, TUPLE[]] )
        do
            click_handler := handler
        end

    click
        do
            click_handler.call
        end

end
```

To pass arguments to the feature when calling it through an agent we pass a tuple (denoted by square brackets) with all the arguments when invoking the agent. For this to work, we must also change the creation of the agent. To pass three arguments, we would create the agent using my_agent := agent my_feature(?, ?, ?) and then call it with a.call([argument_1, argument_2, argument_3]).

The type of an my_agent from above would be PROCEDURE[ T, TUPLE[ ARG1, ARG2, ARG3 ] ], where T is the class my_feature belongs to and ARG1, ARG2 and ARG3 are the types of argument_1, argument_2 and argument_3 respectively.

If the encapsulated feature is to return a value, then the type is actually FUNCTION[ T, TUPLE[ ARG1, ARG2, ARG3 ], RETURN_TYPE ].

