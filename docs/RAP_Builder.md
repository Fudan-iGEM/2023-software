As shown in workflow, after calculating the optimal enzyme concentration through KineticHub, the corresponding regulatory elements need to be designed through RAP Builder to form the sequence of the pRAP system. We developed a thermodynamic model and Monte Carlo algorithm for the design of the corresponding regulating elements. There are two modes in RAP Builder: RBS design mode and stem-loop design mode. We provide a summary of the notation.



| Variable                 | Description                                                  |
| :----------------------- | :----------------------------------------------------------- |
| $[G_n]$                  | gene concentration of $reaction_n$                           |
| $[mR_{n}]$               | mRNA concentration of $reaction_n$                           |
| $[P_{n}]$                | protein concentration of $reaction_n$                        |
| $\alpha_{p,n}$           | translation initiation rate of $reaction_n$                  |
| $\alpha_{m,n}$           | transcription initiation rate $reaction_n$                   |
| $\delta_{n}$             | mRNA degradation rate of $reaction_n$                        |
| $\lambda$                | growth rate of the cell                                      |
| $c_n$                    | optimal concentration of the enzyme of $reaction_n$          |
| $\Delta G_{total,n}$     | total free energy change of $reaction_n$                     |
| $\Delta G_{mRNA:rRNA,n}$ | free energy change when16S rRNA cofolds and hybridizes with the mRNA subsequence at the 16S rRNA-binding site of $reaction_n$ |
| $\Delta G_{start,n}$     | free energy change when anticodon hybridizes to the start codon of $reaction_n$ |
| $\Delta G_{spacing,n}$   | energetic penalty for a nonoptimal distance between the 16S rRNA-binding site and the start codon of $reaction_n$ |
| $\Delta G_{standby,n}$   | free energy change when the standby site is folded of $reaction_n$ |
| $\Delta G_{mRNA,n}$      | the free energy change when mRNA is folded of of $reaction_n$ |
| $\Delta G_{stem-loop,n}$ | the free energy change when stem-loop is folded of of $reaction_n$ |
| $R$                      | gas constant                                                 |
| $T$                      | culture temperature                                          |

Protein concentration is affected by both translation initiation rate and mRNA degradation rate. We adopted and designed a cell-scale dynamic model of transcription and translation[^1]. Here are some of the assumptions that RAP Builder is based on.

<div style="text-align: center;">
    <img src="https://static.igem.wiki/teams/4765/wiki/czy/rap-builder-model.png" style='width:100%'>
</div>


## Assumption 1

The dynamics of transcription and translation can be expressed as follows:

$$
\frac{d[mR_{n}]}{dt} = \alpha_{m,n}[G_n]-\delta_n[mR_n]
$$

$$
\frac{d[P_n]}{dt} = \alpha_{p,n}[mR_n]-\lambda[P_n]
$$

If we consider steady-state constraint, both $\frac{d[mR_{n}]}{dt}$ and $\frac{d[P_n]}{dt}$ are equal to $0$. We could conclude:
$$
\alpha_{m,n}[G_n]=\delta_n[mR_n]
$$

$$
\alpha_{p,n}[mR_n]=\lambda[P_n]
$$

Combining these two equations we can represent the relationship between protein concentration and transcription as well as translation below:

$$
c_n = \frac{\alpha_{p,n}}{\delta_n} \cdot \frac{\alpha_{m,n}[G_n]}{\lambda}
$$

## Assumption 2

Since the enzymes under pRAP system are all expressed under the same promoter, the gene concentration and transcription initiation rate are the same between reactions:

$$
[G_1] = [G_{2}] = ... = [G_n]
$$

$$
\alpha_{m,1} = \alpha_{m,2} = ... = \alpha_{m,n}
$$

Thus the concentration of protein is determined by $\alpha_{p,n}$ and $\delta_n$. RBS design mode quantitative controls $\alpha_{p,n}$ while the stem-loop design mode quantitative controls $\delta_n$.

**For RBS design mode:**

$$
\delta_1 = \delta_2 =...= \delta_n
$$

Based on **Assumption 1**, we can notice:

$$
\alpha_{p,n}\propto\frac{1}{A_nk_{cat,n}}
$$

**For stem-loop design mode:**

$$
\alpha_{p,1} = \alpha_{p,2} = ... = \alpha_{p,n}
$$

Based on **Assumption 1**, we can notice:

$$
\delta_{n}\propto A_nk_{cat,n}
$$

## Assumption 3

Let's start with the RBS design mode. We employ a Gibbs free energy based thermodynamic model to predict the RBS intensity[^2]. If we decompose translation into individual processes, we can calculate $\Delta G_{total,n}$ like this:

$$
\Delta G_{total,n} = \Delta G_{final,n} - \Delta G_{initial,n}\\= \Delta G_{mRNA:rRNA,n} + \Delta G_{start,n} + \Delta G_{spacing,n} - \Delta G_{standby,n} - \Delta G_{mRNA,n}
$$

And the translation initiation rate could be presented by Boltzmann weight ($exp(\Delta G_{total,n}/ RT)$) through an empirical formula:

$$
\alpha_{p,n} = K \cdot exp(-\beta \Delta G_{total,n})
$$

where $K$ and $\beta$ are experimentally determined constants[^2]. The Monte Carlo algorithm enables us to predict and generate the synthetic RBS (see in Usage).

## Assumption 4

Then comes the stem-loop design mode, similar to the RBS design mode, where we develop a model based on the Gibbs free energy to predict the stem-loop intensity.

We investigate and validate the correlation between $\Delta G_{stem-loop,n}$ and mRNA degradation rate $\delta_{n}$ through the experiment. Initially, we designed several synthetic stem-loops with distinct $\Delta G_{stem-loop,n}$ values and subsequently determined the protein concentration by individually assessing their associated fluorescent protein intensities. In accordance with Assumption 2, we employed Support Vector Regression (SVR)[^3] to establish the connection between $\Delta G_{stem-loop,n}$ and $\delta_{n}$.

Support Vector Regression (SVR) learns a non-linear function through the utilization of the kernel trick. In other words, it learns a linear function within the space created by the specific kernel, which corresponds to a non-linear function in the original space.

We designed our experiments by placing GFP ([StayGold](http://parts.igem.org/Part:BBa_K4162001)) in the first position of the pRAP system, RFP ([mScarlet](http://parts.igem.org/Part:BBa_K4765022)) in the last position. The stem-loop at the 3' end of GFP was then continually changed and the fluorescence intensity ratio of GFP to RFP was measured to determine mRNA degradation rate corresponding to different stem-loops. For more information about our experiment validation, please click [here](http://parts.igem.org/Part:BBa_K4765129).

<div style="text-align: center;">
    <img src="https://static.igem.wiki/teams/4765/wiki/results-wyj/ribozyme-czy.jpg" style='width:80%'>
</div>


The dataset we used can be accessed [here](https://static.igem.wiki/teams/4765/wiki/czy/summary-20231011.pdf).

<div style="text-align: center;">
    <img src="https://static.igem.wiki/teams/4765/wiki/czy/result.svg" style='width:60%'>
</div>


In conclusion, the experiment validates the accuracy of RAP and demonstrates that the mRNA degradation rate corresponding to the stem-loop can be accurately predicted using SVR.

## References
[^1]: Balakrishnan, R., Mori, M., Segota, I., Zhang, Z., Aebersold, R., Ludwig, C., & Hwa, T. (2022). Principles of gene regulation quantitatively connect DNA to RNA and proteins in bacteria. *Science (New York, N.Y.)*, *378*(6624), eabk2066. https://doi.org/10.1126/science.abk2066
[^2]: Salis, H. M., Mirsky, E. A., & Voigt, C. A. (2009). Automated design of synthetic ribosome binding sites to control protein expression. *Nature Biotechnology*, *27*(10), Article 10. https://doi.org/10.1038/nbt.1568 ↩
[^3]: Drucker, H., Burges, C. J. C., Kaufman, L., Smola, A., & Vapnik, V. (1996). Support vector regression machines. *Proceedings of the 9th International Conference on Neural Information Processing Systems*, 155–161.