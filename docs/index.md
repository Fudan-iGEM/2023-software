---
hide:
  - navigation
  - toc
---
# RAP Documentation

![](https://badgen.net/badge/platform/Linux,macOS,Windows?list=%7C)
![](https://badgen.net/static/Python/3.10/blue)
![](https://badgen.net/static/vue/2.6+/green)
![](https://badgen.net/static/license/CC%20BY%204.0/blue)
![](https://badgen.net/docker/size/mistyfield/rap/0.4.1-beta)

<hr>
<center>
    <img src="assets/RAP_logo.png" alt="RAP_logo" style="zoom: 15%;" />
</center>


!!! tip "🤝 Seek for collaboration!"

    If your team needs to use multiple enzyme coupling to participate in a module, we 
    welcome the opportunity to collaborate with you and offer you help with wet and dry lab, 
    and we are in desire of your feedback and comment on RAP!
    If you are interested in RAP, don't feel hensitate to email to us [here](mailto:20301050198@fudan.edu.cn)!

[RAP](http://54.169.242.254:5000) is a software developed by iGEM 2023, Fudan Team for bottom-up design of Ribozyme-Assisted Polycistronic co-expression system (pRAP system). RAP mainly consists of three parts:

- **KineticHub**
- **RAP builder**
- **PartHub2**

## Features

RAP can be useful throughout the DBTL cycle. Among its key ingredients, RAP supports:

=== "Intuitive $k_{cat}$ Search"

    KineticHub allows you to retrieve more than 70,000 $k_{cat}$ records from 7,000+ EC numbers in a single click, and supports the addition of experimental data and the integration of deep learning methods to predict kcat. 

=== "One-Click pRAP system Sequence Building"

    Combined with the $k_{cat}$ of the enzyme, RAP Builder can automatically calculate optimal enzyme concentration for balanced linear biochemical reactions, and our Monte Carlo algorithm will derive the proper synthetic RBS, and automatically generate the sequence file in GeneBank format.

=== "Diversified Part Search"

    We upgraded PartHub and launched PartHub 2, which provides a more intuitive and easy-to-use user interface and designs a diversified recommendation algorithm based on graph learning with 60,000+ parts.

## Learn more
- [User Guide](get_started.md)
- [Installation](installation.md)
- [Wiki](https://2023.igem.wiki/fudan/software)

## Leave a comment to us!

Your comments and suggestions are vital to further refine and improve RAP, so feel free to click [here](http://54.169.242.254:5000/comment)!