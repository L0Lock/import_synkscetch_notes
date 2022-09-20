# Import Synkscetch Notes

Addon for Blender to import and manage notes or comments from Syncsketch.com

## Installation

- Download the [latest release](https://github.com/L0Lock/import_synkscetch_notes/releases/latest);
- In Blender, go to *Edit* > *Preferences* > *Addons* category;
- Hit the *Install* button and select the `import_synkscetch_notes_versionNumber.zip`
- Enable the addon

The addon preferences allow you to chose in which tab of the viewport's sidebar will be located the *Syncsketch Feedback* panel. By default, it is located in the *Animation* tab:

![Addon location and preferences](https://user-images.githubusercontent.com/16049822/191252764-ff78b734-1375-4111-8a28-da1ff38f00f2.png)


## Usage

### Downloading notes and comments on Syncsketch.com

In this addon, "notes" are the raw sketches draw on your syncsketch reviews, "comments" are the text comments written on the side.

On Syncsketch, you can download the "Maya Grease Pencile File" as your notes, and the "Item notes as CSV" as your comments:

![Syncsketch download](https://user-images.githubusercontent.com/16049822/191250840-009a6271-8658-4a1f-aa3e-1579f207c988.png)

You will end up with a `shot_name.greasepencil.zip` and a `.CSV` file.

### Loading notes and comments

You can either use the import menu under *File* > *Import*:

![import menu](https://user-images.githubusercontent.com/16049822/191251450-6f8e6928-e6ea-4a28-a4e8-bbc9d92c18f9.png)

Or you can go in the *3d Viewport* > *Sidebar* > *Animation* tab > *Syncsketch Feedback* panel, and use the import buttons to load your notes and comments:

![panel UI](https://user-images.githubusercontent.com/16049822/191252992-0c1f96e4-2ade-4b07-93aa-1817487cb0e1.png)


