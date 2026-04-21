---

title: "Reference vs. Expanded Classes"

source: https://eiffel-guide.com/

source_heading_level: 2

---



# Reference vs. Expanded Classes



In Eiffel there is a key differentiation between reference and expanded classes. By default a class is of the reference type. To declare a class as expanded, we use the expanded keyword before class.

As the name would suggest a reference class sets itself apart in that its attributes are references to other objects, either of classes defined by the developer or built-in classes such as STRING or REAL. As such, an object of a the reference type does not contain any actual values apart from addresses. It only contains references to where the values are stored in the memory. In C or C++ references would be referred to as pointers. An expanded class on the other hand does not contain references, but the actual values. This key difference has an effect on how we create and use classes.

Another difference, is that when used as an argument, data of an expanded type is passed by value, while data of reference types are passed by reference, since the object consists of addresses.

