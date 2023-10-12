# KineticHub
KineticHub is a database containing $k_{cat}$ for more than 70,000 record with 7000+ EC numbers.
## Motivation
After establishing the idea for RAP Builder, we found that there was no database specifically for $k_{cat}$ and other kinetic constants of enzymes, and that searching for kinetic constants like $k_{cat}$ in general enzyme databases was not easy. Therefore, we worked on building a database platform dedicated to searching for enzyme reaction kinetic parameters. To create a user interface that is intuitive and to meet the needs of users for more advanced database use, we use MySQL to build the database itself and provide an intuitive web UI and RESTful API to meet the user's advanced development needs.

## Establishment of KineticHub
The first step in the optimization of intracellular metabolism using the pRAP system is to determine the optimal enzyme concentration. For this purpose, we designed a model for calculating the optimal enzyme concentration, which is based on the following assumptions. We provide a summary of the notation.

| Variable    | Description                                                 |
| :---------- | :---------------------------------------------------------- |
| $flux_n$    | flux of  $reaction_n$                                       |
| $[S_n]$     | concentration of the substrate of $reaction_n$              |
| $k_{m,n}$   | $k_m$ value of $reaction_n$                                 |
| $v_n$       | velocity value of $reaction_n$                              |
| $k_{cat,n}$ | $k_{cat}$ value of $reaction_n$                             |
| $A_n$       | ratio of product to substrate stoichiometry of $reaction_n$ |
| $c_n$       | optimal concentration of the enzyme of $reaction_n$         |

### Assumption 1

We expect the optimal state of intracellular metabolism to be flux-balanced, so we should take steady-state constraint into consideration, which can be expressed as:

$$
flux_1 = flux_2 = ... = flux_n
$$

The significance of this assumption is that it prevents metabolic stress caused by flux imbalance and permits the cell to be in a state of flux balance.

### Assumption 2

The substrate should not be overstacked and should be kept more stationary, which we denote here as follows:

$$
\frac{[S_1]}{k_{m,1}} = \frac{[S_2]}{k_{m,2}} = ... = \frac{[S_n]}{k_{m,n}}
$$

From the Michaelis-Menten equation we could find:

$$
v_n = \frac{k_{cat,n}c_n[S_n]}{k_{m,n}+[S_n]}=\frac{k_{cat,n}c_n}{\frac{k_{m,n}}{[S_n]}+1}
$$

and $flux_n$ could be expressed as:

$$
flux_n = v_n \times A_n
$$

Combining these equations and **Assumption 1** we can conclude:

$$
c_n\propto\frac{1}{A_nk_{cat,n}}
$$

Therefore, we can calculate the optimal enzyme concentration based on the $k_{cat}$ of the enzyme. It is important to note that the purpose of regulating RBS strength here is to regulate the relative proportional coordination between exogenously imported reactions, and the regulation of the absolute strength of the cascade reaction coupled to intracellular metabolism is controlled by the induction intensity. Since there is no database that specializes on the $k_{cat}$ of the enzyme, we created **KineticHub** to obtain the $k_{cat}$ of the enzyme and determine the optimal enzyme concentration. For a more detailed implementation please read our documentation and the [source code](https://gitlab.igem.org/2023/software-tools/fudan/-/tree/main/webUI).