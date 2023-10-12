# Quickstart of RAP
## Get started
!!! success "since v0.1.0-beta"

    RAP is now available at [http://54.169.242.254:5000](http://54.169.242.254:5000)!


The full execution of RAP requires only four steps!

## Visit Home Page of RAP

   Upon visiting our [live demo](http://54.169.242.254:5000/home) or `Home` page of RAP deployed through docker, you will see the page below:

   <div style="text-align: center;">
       <img src="https://static.igem.wiki/teams/4765/wiki/czy/rap-home.png" style='width:80%'>
   </div>

## Run Step 1: KineticHub

   The first step in constructing a pRAP system using RAP is to calculate the optimal enzyme concentration by KineticHub. The first step involves two tasks, i.e., searching target reaction and enzyme record for the reaction and constructing a cascade reaction, optimal ratio of enzymes based on the data will be returned after these two tasks.

   First, in the `KineticHub > Search Enzyme` page, please enter the query and the type of keyword you want to retrieve.

   Here are some examples of query and the corresponding keyword types:

   | Keword Type | Meaning & Format                                             | Query           |
   | ----------- | ------------------------------------------------------------ | --------------- |
   | EC number   | EC number of the reaction (e.g. x.y.z.w), it's fine to just enter part of the EC number | 1.1.1.101       |
   | Name        | The name of the reaction                                     | Nadh peroxidase |
   | Type        | Reaction type                                                | Oxidation       |
   | Substrate   | One of the possible substrate of the reaction                | alcohol         |
   | Product     | One of the possible product of the reaction                  | NADPH           |

   In order to search for the target enzyme more accurately, it is most recommended to use EC number to search for the enzyme. you will be presented with the interface:

   <div style="text-align: center;">
       <img src="https://static.igem.wiki/teams/4765/wiki/czy/kinetichub-result-czy.png" style='width:80%'>
   </div>


   After clicking `Get Kcat`, the interface will be represented like:

   <div style="text-align: center;" id="fig-5">
       <img src="https://static.igem.wiki/teams/4765/wiki/czy/kcat-result-czy.png" style='width:80%'>
   </div>


   Here you can get the species from which the enzyme is derived and its kinetic parameters in different environments with references, and you can check the appropriate record for your project and click on the plus icon. After that, return to the search results page, and you'll see that the flask icon in the upper right corner has added a little red dot.

   You have successfully imported one reaction! Now you need to add the remaining other reactions following this process.

???+ question "🤔If you haven't found the proper $k_{cat}$?"

    If you haven't found the proper $k_{cat}$? You can add relevant experimental data into KineticHub to use it in `KineticHub > Add Enzyme` , if you don't you can use one of the machine learning based prediction methods online [here](https://turnup.cs.hhu.de/KCAT_pred_single) or using the [colab ipynb scripts](https://colab.research.google.com/gist/MistyField/3dd7af5e179b661c821c3b46c71d1b34/kcat_prediction.ipynb) we provide!

After that, in the `KineticHub > Build reactions` page, please enter the ratio of product to substrate stoichiometry for your reactions according to EC number and then click `Submit` button.

   <div style="text-align: center;">
       <img src="https://static.igem.wiki/teams/4765/wiki/czy/rap-builder-czy.png" style='width:80%'>
   </div>

## Run Step 2: RAP Builder

   In `RAP Builder` page, you can select design mode (RBS or stem-loop design mode) and input the sequence of the enzyme. Then you can click `Submit` button to run RAP Builder! After completion of RAP Builder, the results will be automatically downloaded, containing a sequence file in `GeneBank` format and an annotation in `csv` format.

   <div style="text-align: center;">
       <img src="https://static.igem.wiki/teams/4765/wiki/czy/rap-builder-demo-czy.png" style='width:80%'>
   </div>

## **Search Part in PartHub 2**

   To search Part with Parthub, you can navigate to the `PartHub 2` page. Subsequently, please input your search query and select the appropriate keyword type as required.

   <div style="text-align: center;">
       <img src="https://static.igem.wiki/teams/4765/wiki/czy/parthub-search.png" style='width:80%'>
   </div>

The examples and meaning of the search terms corresponding to search types is as follows:

| keyword type | Meaning & Format                                             | Example           |
| :----------- | :----------------------------------------------------------- | :---------------- |
| ID           | The id of the part (e.g. BBa_xxxxxxxx). It is fine to enter a search term with or without BBa_ | K3790012          |
| Name         | The name of the part in Registry of Standard Biological Parts | GFP               |
| Sequence     | The sequence of the part (if it exists). The search term can only be the combination of [a, t, g, c, A, T, G, C] | TTAACTTTAAGAAGGAG |
| Designer     | The name of the person who designed the part                 | Weiwen Chen       |
| Team         | The name of the team which designed the part                 | Fudan             |
| Content      | The content of the part in Registry of Standard Biological Parts | carotene          |

You have the option to peruse the search results and access the Part you are interested.

   <div style="text-align: center;">
       <img src="https://static.igem.wiki/teams/4765/wiki/czy/parthub-result.png" style='width:80%'>
   </div>


By clicking on a search result, you will be presented with the network structure of the Part. You can scroll to zoom the canvas and drag to move the nodes. Furthermore, clicking on a node will display detailed information about the Part, while double-clicking will lead you to the dedicated Part page. On this page, you will also have the convenience of directly downloading the GeneBank format sequence for the selected Part.

   <div style="text-align: center;">
       <img src="https://static.igem.wiki/teams/4765/wiki/parthub-demo.gif" style='width:80%'>
   </div>

!!! success ""

    🎉**You have successfully built your pRAP system!**


