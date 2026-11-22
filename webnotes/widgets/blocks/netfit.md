::: {.widget name="netfit"}
Move the number of hidden neurons $H$ of a network with one layer. It is trained for 4000 steps of Adam, a form of gradient descent, with the mean of the squared error in place of the sum of [(10.1)](#eq-10-1), to reproduce $\sin(3\pi x)$. With one to three neurons the network cannot follow the six extrema of the target, and from four neurons on it follows all of them. With more neurons the loss goes down on the whole, but not at every step of $H$. This is the statement that the architecture fixes which functions the network can represent.
:::
