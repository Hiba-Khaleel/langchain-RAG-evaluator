---

title: "Introduction"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Introduction



Welcome to this guide about the Eiffel programming language. It is designed to be a basic reference to help beginners get acquainted with the language. Some knowledge of other programming languages might be considered very useful. This should not be seen as a course or tutorial. Please help improve and maintain this page through GitHub (https://github.com/carlfriess/eiffel-guide/). To get started, let's have a look at this simple hello world:

```eiffel
class
    HELLO_WORLD

create
    say_it

feature
    say_it
        do
            Io.put_string ("Hello World!")
        end

end
```

```
Hello World!
```

