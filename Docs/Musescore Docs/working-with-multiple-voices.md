# Working with multiple voices

## Overview

In notation, a **voice** is a single line of music on a staff. It is possible to notate more than one voice, with independent rhythms, on a single staff. Two voices on the same staff are normally indicated using opposing stems – an upper voice with stems up and a lower voice with stems down:

<figure><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2Fvm8pzbYAprD5Ujpw022Y%2Fvoices_hero.png?alt=media&#x26;token=ef89e943-1c21-49f6-8044-35e90d9afca2" alt="Music using two voices on a single staff"><figcaption></figcaption></figure>

In a four-part SATB arrangement on two staves, you would use voices 1 and 2 on the top staff for soprano and alto, and voices 1 and 2 on the bottom staff for tenor and bass:

<figure><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FC4QfbVRirMrk8RJl1WYl%2Fvoices_satb.png?alt=media&#x26;token=475da7eb-8ec6-4fc0-85f7-ceea4db3d43c" alt="Multiple voices in an SATB arrangement"><figcaption></figcaption></figure>

The default voice when starting note entry is voice 1. When you need a second voice, normally this will be voice 2. Voices 3 and 4 are less frequently used, but are sometimes necessary in complex polyphonic music or for the inner parts in dense keyboard textures.

## Entering music in multiple voices

The principles of entering notes and rests are the same regardless of which voice you are in (see [entering-notes-and-rests](https://handbook.musescore.org/basics/entering-notes-and-rests "mention")).

Each voice has its own color in the UI. The note entry cursor changes color to reflect the current voice, and notes and rests (and many other items) will be highlighted in the color of their respective voice when you select them. This is useful when inputting and editing as it gives you an immediate visual indicator of the voice the music belongs to.

{% hint style="info" %}
You can change each voice's color in **Preferences -> Advanced**.
{% endhint %}

While you are in note entry mode, you can switch to a different voice by clicking one of the voice selection buttons in the top toolbar:

<figure><picture><source srcset="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FqRN8UkZMjLf20xd6iGd6%2Fvoices-toolbar-dark.png?alt=media&#x26;token=57b4dac2-f07c-4c22-bc29-bb40b5328457" media="(prefers-color-scheme: dark)"><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FF2SUS4sm7EVsd8QKGNAV%2Fvoices-toolbar-light.png?alt=media&#x26;token=b352fcd7-a38f-4487-aeb3-2e36eb5ce2e2" alt="" width="222"></picture><figcaption></figcaption></figure>

You can also use the keyboard shortcuts <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>1</kbd>–<kbd>4</kbd>.

{% hint style="info" %}
By default, only the buttons for voices 1 and 2 are shown in the toolbar. To use the others, first reveal them by clicking the <picture><source srcset="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2F1sMpHFntZ5DT6N4gHFjn%2Fbutton-cog-dark.svg?alt=media&#x26;token=8f887732-e876-4411-8a03-06991843bc9b" media="(prefers-color-scheme: dark)"><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FpNRabkhIKjFCeXGr3HfV%2Fbutton-cog-light.svg?alt=media&#x26;token=2f43f53c-b3ab-49be-8183-32bd16b73b0b" alt="" data-size="line"></picture> cog button in the toolbar and then clicking the <img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FoyU8Vo7KfHL27PfBmj3c%2Fbutton-visibility-eye-dark.svg?alt=media&#x26;token=351974ae-29e3-47af-834e-e782881ff171" alt="" data-size="line"> eye button next to **Voice 3** and **Voice 4** in the menu.
{% endhint %}

If you select a note or rest before entering note entry mode, you will enter note entry mode in the same voice as that note or rest.

## Editing music in multiple voices

### Moving notes between voices

To move notes or rests to another voice:

1. Select the notes you’d like to move (individually, or as a list or range).
2. Click the button for the voice in which you’d like them to be moved.

You can also use the shortcuts <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>1</kbd>–<kbd>4</kbd> (Win) or <kbd>Cmd</kbd>+<kbd>Alt</kbd>+<kbd>1</kbd>–<kbd>4</kbd> (Mac).

{% hint style="info" %}
You can move any number of notes, even from multiple voices at once, into a voice. If there are notes at the same position with the same rhythm they will combine into chords. If there are differing rhythms, some notes may be left in their original voice as MuseScore Studio will not be able to know what you intend.
{% endhint %}

### Exchanging voices

You can swap the music of any pair of voices by selecting one of the options from **Tools -> Voices** (e.g. **Exchange voice 1-2**). This only works with range selections, and on whole measures (or ranges of measures). If only part of a measure is included in the range, the whole measure will be swapped.

### Adjusting rests

It is often necessary to remove redundant rests in secondary voices. This can be done in two ways:

* Hiding the rest, by selecting it and unchecking **Visible** in **Properties** (or using the shortcut <kbd>V</kbd>).
* Deleting the rest, by selecting it and pressing <kbd>Del</kbd>.

{% hint style="info" %}
Voice 1 is the 'reference' voice and must remain rhythmically complete. As such, rests in voice 1 can be hidden, but not deleted.
{% endhint %}

In a single voice, rests appear in the middle of the staff, but in multiple voices, rests for voice 1 are moved up at least one space and rests for voice 2 are moved down at least one space. This offset helps to show which voice they belong to. In practice, they are usually displaced further out to avoid colliding with notation in the other voice.

Where there are rests of the same duration in more than one voice simultaneously, MuseScore Studio can merge them together automatically:

<figure><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2Fnx5BlgMBXm80U0FuQs6r%2Fvoices-merge_rests.png?alt=media&#x26;token=eac4d3aa-0008-41d8-a6bf-05fd36585e91" alt="" width="375"><figcaption><p>Rests unmerged (left) and merged (right)</p></figcaption></figure>

The behavior of rests in multiple voices can be controlled using these options in **Format -> Style -> Rests**:

<figure><picture><source srcset="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FKrjdFAzkyNw2CFTgjXOG%2Fvoices-rests_styles-dark.png?alt=media&#x26;token=b3f01765-5ec0-4d94-8b55-48ccb44d8d28" media="(prefers-color-scheme: dark)"><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FBunpX71lurGZu4Sz873i%2Fvoices-rests_styles-light.png?alt=media&#x26;token=6ff7304c-c714-49eb-9653-54aaf70d1463" alt="" width="248"></picture><figcaption></figcaption></figure>

* **Default vertical offset:** Choose between 1 space and 2 spaces for the initial displacement of rests when in multiple voices.
* **Merge matching rests:** Merge rests of the same duration that occur simultaneously in more than one voice (see image above).

These options affect all staves in the scores. If you want to turn rest merging on or off for specific staves, you can do this via [staff-part-properties](https://handbook.musescore.org/notation/instruments-staves-and-systems/staff-part-properties "mention"):

1. Right-click the staff and choose **Staff/Part properties** from the menu.
2. Change **Merge matching rests** to **On** or **Off**. The default, **Auto**, will follow the score-wide setting.

{% hint style="info" %}
'Merged' rests are actually overlaid on top of each other, but they are all still there. If you want to see more than one rest in a specific place you can achieve this by moving them manually.
{% endhint %}

Rests can also be moved manually like other items. Just select a rest and press <kbd>Up</kbd> or <kbd>Down</kbd>, or change **Properties -> Appearance -> Offset**.

### Stem direction

When music is in a single voice, the direction of stems varies according to the vertical positions of the notes (see [#default-stem-direction](https://handbook.musescore.org/notation/rhythm-meter-and-measures/stems-and-flags#default-stem-direction "mention")). When there is more than one voice, all music in voices 1 and 3 will have stems up, and all music in voices 2 and 4 will have stems down.

You can still change the stem direction of any notes by selecting them and pressing <kbd>X</kbd> (or pressing the <picture><source srcset="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FsCWM1lIvNJtZDwSG2Jc6%2Fbutton-flip_direction-dark.svg?alt=media&#x26;token=6a718332-9cc1-48a6-b207-5d0dec5fd449" media="(prefers-color-scheme: dark)"><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FZQridKXx4N4RdylxP8GX%2Fbutton-flip_direction-light.svg?alt=media&#x26;token=e6316ca0-6ce3-477d-940f-39d028688650" alt="" data-size="line"></picture> **Flip direction** button in the note input toolbar).

When there are simultaneous notes on one staff in different voices but which have the same stem direction, MuseScore will combine them together so that it looks like they form a single chord, with a shared stem:

<figure><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FVFO5TcePQpJpefjM4W5s%2Fvoices-combined_equation.png?alt=media&#x26;token=255dd02e-e911-4172-8db5-7084430c0be7" alt="" width="375"><figcaption></figcaption></figure>

This is achieved by offsetting certain notes and overlaying the stems, but it is still actually two chords. If you want a different arrangement, it can be difficult to undo this. Therefore you can turn this behavior off by unchecking **Format -> Style -> Combine voices that share the same stem direction**. This will, instead, simply overlay the two chords directly over each other:

<figure><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2Fx7kXp28BRP29CDI1y4w9%2Fvoices-combined_off.png?alt=media&#x26;token=d0137c54-66ba-4582-8211-76b8c8598838" alt="" width="266"><figcaption></figcaption></figure>

This is not very beautiful, but it is a much simpler starting point from which you can manually offset the voices the way you need them, like this:

<figure><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FHADjeRmY4XEiNrd2qY7R%2Fvoices-combined_manual.png?alt=media&#x26;token=1b033bb2-dfda-4e64-ac4a-adeb137a979e" alt="" width="266"><figcaption></figcaption></figure>

You can also control this for specific chords in the score via Properties (under **Note -> Head -> Show more**):

<figure><picture><source srcset="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FdsXszJnV1UK3k6vZ1B4T%2Fvoices-combine_property-dark.png?alt=media&#x26;token=ecc9c6e9-d1a0-446c-a629-7f82a7e77268" media="(prefers-color-scheme: dark)"><img src="https://3455969201-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FP81HaeapLzzJGtG6DSwH%2Fuploads%2FaWzskeuk9JbEF5iVdsvw%2Fvoices-combine_property-light.png?alt=media&#x26;token=4baa7401-73ec-476a-ba85-fa704141f5e6" alt="" width="297"></picture><figcaption></figcaption></figure>

## Playback

Note that it is not currently possible to assign different sounds or VSTs to different voices within the same instrument. If you need to do this, they must be separate instruments.