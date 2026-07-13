# Van Conversion Layout Optimiser

This project approaches van conversion layout as a 2D bin-packing optimisation problem. 

This Python tool algorithmically determines the most space-efficient floor plan for a medium-sized panel van, ensuring that essential items fit perfectly without overlapping.

This tool is designed to help anyone interested in van conversions to visualise layouts best utilising space and needs.

## Core Features
* **Custom Vehicle Dimensions:** Users can input their van's specific dimensions.
* **Item Placement:** Users can define the items they want to include in their van conversion, specifying dimensions and quantities.
* **Visual Output:** The tool generates a visual representation of the optimal layout, making it easier to understand how items fit within the available space.

## Versions
* **v0.1:** Initial release with manual placement of items and basic layout visualisation.
* **v0.2:** Introduced a simple algorithm, placing items by area into the first free spot.
* **v0.3:** Implement a mass constraint, where the centre of mass of the layout is calculated and items are placed to keep the centre of mass as close to the centre of the van as possible.