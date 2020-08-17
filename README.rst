QQ UAV workflows
~~~~~~~~~~~~~~

A repository of workflows and processing tutorials using open source libs for UAV image processing.

These include subset examples for tutorial/demo purposes that are subsets of the UAV surveying project case-studies encountered during the Aberystwyth University / QinetiQ KTP project.

The Structure from Motion workflows use bash scripts, which can be run through the jupyter notebooks provided, please install the pre requisites which are:

.. code-block:: bash

   pip install bash_kernel

   python -m bash_kernel.install


Installation
~~~~~~~~~~~~~~~~~

Ensure you have QGIS (preferably 3), Google Earth and Cloud Compare for visualising things.

There will also be limited use of RSGIS-lib, Orfeo Tool Box (OTB), OSSIM & CGAL.

It is recommened these are installed via conda environments also (excluding OSSIM), allowing easy switching during jupyter sessions and no conflicts.

MicMac Sfm scripts

https://github.com/Ciaran1981/Sfm


Geospatial-learn

https://github.com/Ciaran1981/geospatial-learn

OSSIM

https://trac.osgeo.org/ossim/

RSGIS-lib:

https://www.rsgislib.org/download.html

OTB:

https://anaconda.org/orfeotoolbox/otb

CGAL:

You will need CGAL >= 5.0. 

The binaries may well be available for version 5.0+ on your OS (these are usually available via repo-unix-types or download-windows) and if so ensure you tick the appropriate flags for demos and plugins (this will vary dependent on your OS). 

If not you will have to compile from source.
https://doc.cgal.org/latest/Manual/installation.html

The main lib should compile easily enough, but the demos may be more of a character building experience - worth it if you wish to label your point clouds easily.

Best to use the CMAKE gui for this one.  


Order of use
~~~~~~~~~~~~~~~~~

If using this material for training / familiarisation purposes start by looking at the Sfm_guide.pdf as the contains a detailed account of the software/libs used herein. 

There is both proprietary and open source GUI-based workflows in the `documentation <https://drive.google.com/drive/folders/1gtK0wh7qD22FvruFi-DlZvXfw2S5F4AV?usp=sharing>`_ and for those who favour this, please look at those. 


If you've had enough of that, the Sfm_command_line notebook covers all the basics of scripts use and is probably best first.

Next, one of these which go a little further in terms of processing outputs and parameters

- Select-For-Forest.ipynb (Typical forest application to classify point cloud using PDAL and extract ground/canopy).

- Borthwrkflow.ipynb explores ortho mosaicking options and their effects on results after the SfM part

The remaining notebooks are related to generating mapping products or information for environmental monitoring. The details are in the notebooks themselves and are largely written in python:

- Crop_seg_pixel_stat_example.ipynb

- Aerial_imagery_landcover/Object_based_landcover.ipynb

- Point_Cloud_Classification_for_urban_mapping.ipynb



