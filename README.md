![REToolboxTitle](https://github.com/NSACloud/RE-Toolbox/assets/46909075/53788f20-bd6d-425e-b35d-3eca69ed8e0a)

This is a companion addon to make working with RE Engine files quicker and easier.

![REToolboxPreview](https://github.com/NSACloud/RE-Toolbox/assets/46909075/8e4dd54f-d330-47d9-8281-e48713504b2e)


### [Download RE Toolbox](https://github.com/NSACloud/RE-Toolbox/archive/refs/heads/main.zip)

## Features
 - Adds utilities for RE Engine mesh files to automate some of the more tedious tasks, such as splitting connected uv islands or renaming meshes.
 - Controls visibility of other RE Engine addons so that the sidebar is less cluttered.
 - Batch exporting of files imported with other RE Engine addons.
 
 More features to come.


## Requirements
* [Blender 2.93 or higher](https://www.blender.org/download/)

## Installation
Download the addon from the "Download RE Toolbox" link at the top or click Code > Download Zip.

In Blender, go to Edit > Preferences > Addons, then click "Install" in the top right.

Navigate to the downloaded zip file for this addon and click "Install Addon". The addon should then be usable.

To update this addon, navigate to Preferences > Add-ons > RE Toolbox and press the "Check for update" button.

## Change Log

### V3 - 5/20/2024

* Added "Create Mesh Collection" button. It creates a collection for an RE Engine mesh and sets up LOD collections.
* Added "Split Sharp Edges" button. This edge splits edges that are marked as sharp in Blender so that the sharp edge is not lost when the mesh is exported.
* All operators now apply to every object in scene unless objects are selected. In which case, the operator will only apply to the selected objects.
  
<details>
  <summary>Older Version Change Logs</summary>

### V2 - 4/29/2024

* Fixed issue where "Solve Repeated UVs" didn't always work 100% of the time.
* Mesh normals are now better preserved when using "Solve Repeated UVs".

 </details>
See Also:

https://github.com/NSACloud/RE-Mesh-Editor

