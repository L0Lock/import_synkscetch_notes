# Import Synkscetch Notes

Addon for Blender to import notes from Syncsketch.com

## Installation

- Download [import_synkscetch_notes.py](https://raw.githubusercontent.com/L0Lock/import_synkscetch_notes/main/import_synkscetch_notes.py);
- open it in Blender's *text editor*;
- Execute it with the Run button

## Usage

From Syncsketch, download the "Maya Grease Pencile File" of your notes:

![Syncsketch download](https://user-images.githubusercontent.com/16049822/189382632-60cbac33-639a-40e7-8b32-a14c338060ce.png)

It will download a `shot_name.greasepencil.zip` file.

After installing the importer, go in the regular Import menu:

![import menu](https://user-images.githubusercontent.com/16049822/189382090-c6d17928-d9c2-4e42-8aed-9596cc2f4a53.png)

Click it, navigate to your zip file, and it will automatically clear any remaining background image from your active camera and setup your Syncsketch notes.

## Limitations & future development:

- [ ] Currently not an addon, hard to install once for good;
- [ ] Removes all preceeding background images of your camera. Ideally it should only delete the ones made by the importer itself;
- [ ] Could be nice to somehow import written notes;
- [ ] Maybe try to convince Syncsketch's devs to add a new download specific to Blender with only the frames and written notes in a .CSV.
