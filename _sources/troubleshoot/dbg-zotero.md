# Zotero Utilities

## Auto-merge Multiple Duplicates

Merging duplicates in Zotero can be done by a mouse click, but only by a mouse click and item-by-item. This can take a lot of time when merging large libraries. Here is a workaround to auto-merge multiple duplicates in Zotero.

```{admonition} Make sure all duplicates have the same Item Type
:class: important

To make the following auto-merge code work smoothly, go over your duplicate items and look for any marked duplicates that have different item types. Next, harmonize the item types of duplicate pairs (i.e., change the Item Type of one of the concerned entries). This is a bit tedious, but does not take too long and much faster than merging each duplicate additionally by mouse click.
```

* Open the Zotero application on your computer (not in the browser)
* Go to the **Duplicate Items** entry of your library
* Highlight all (press `CTRL` and `A` keys)
* Go to **Tools** (top menu) > **Developer** > **Run JavaScript**, copy-paste the following code block into the **Code** field, and click **Run**


```
var DupPane = Zotero.getZoteroPanes();

for(var i = 0; i < 999; i++) {
  try {
    await new Promise(r => setTimeout(r, 50));
    DupPane[0].mergeSelectedItems();
    Zotero_Duplicates_Pane.merge();
  } catch (e) {
    console.log(e);
  }
}
```

The code block makes at maximum 999 iterations, which can be increased by increasing the iteration number in the for loop of the JavaScript code.


This response is inspired by discussions in the [Zotero Forum](https://forums.zotero.org/discussion/40457/merge-all-duplicates).
