## Conceptual Church Map (CCM) Guidance

The geopackage comprises 4 layers, which will all be activated by default.

It is suggested that users toggle the visibility of the layer named 'ccm_room_outlines' (third from top) to off.

The layers are structured as follows (from base to top):

- _background_ - this is the neutral-coloured backdrop, set to this colour for maximum contrast and accessibility for the schemes chosen for default display.

- _ccm_spaces_base_ - this layer provides the underpinning spatial layout and default styles.

- _ccm_room_outline_ - this is a mirror layer of the above, to allow for heatmapping or similar visualisation techniques distinct from the core spatial layout. By default all the values are set to show a shaded grid - and it is advised that this layer be toggled off when a map is first generated.

- _ccm_points_ - this layer provides a fixed corresponding point feature for each conceptual space, manually arranged to provide optimum visibility against spatial labels.


Each conceptual space has been assigned a categorisation from the following, with default polygonal line and point styles which can be modified to suit user needs :

- _Core_ - main building outline

- _Internal_ - spaces always found within a main building

- _External_ - spaces typically found outwith or adjoining a main building

- _Altar_ - a distinct space

- _Unknown_ - for use when there is a level of ambiguity, uncertainity, or mistrust in sources

- _Spare_ - hidden by default through invisible styles, this provides an addition space that can be tailored to any other defined space if of importance to a design (e.g. 'Library', 'Rafters', 'Cloakroom', 'Kitchen')

- _Cloisters - Cardinal_ - N/E/S/W distinctions within the Cloisters conceptual space
