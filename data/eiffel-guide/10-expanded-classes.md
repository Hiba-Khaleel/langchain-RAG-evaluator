---

title: "Expanded Classes"

source: https://eiffel-guide.com/

source_heading_level: 3

---



## Expanded Classes



Expanded classes differ from reference classes in that they do not contain references, but rather the actual values of their attributes. For this reason, we do not need to call create before using objects that are instances of the class. All attributes are automatically set to their default initial values when the object is defined.

If a and b are both instances of an expanded class, a := b will copy all of b (including its values) into a and create a new instance with the same values.

On the other hand, if a and b are both instances of a reference class, then a := b will copy the reference to the instance of the class represented by b into a. In other words, now a and b will reference the same instance and any change to a will be reflected in b.

