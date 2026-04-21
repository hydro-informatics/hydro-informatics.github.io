(debug-tex)=
# LaTeX & Citation Management (Zotero)

Online LaTeX editors, such as Overleaf, offer convenient, real-time collaboration and cloud-based compilation, but advanced features like handling larger documents or extensive team collaboration often require a paid subscription. In contrast, working locally with a dedicated editor like TeXstudio (see {ref}`LaTeX installation <install-tex>`) allows you to edit and compile documents without depending on an internet connection while writing/compiling and without incurring subscription costs. This page is intended to provide guidance on effectively using LaTeX in a local environment.


## Plaintext and word counting

To estimate the number of words in a LaTeX manuscript using TeXstudio, begin by creating a plain text version of your document. Under the **Tools** menu, select **Convert to Abridged Plaintext**, which opens a new untitled tab containing your text without LaTeX commands. This stripped-down file is also suitable for sharing with collaborators who prefer (richtext) word processors. Next, choose **Analyse Text...** from the Tools menu and click the Count button. TeXstudio will display the number of paragraphs (that is, words) in your text and even provide a frequency analysis of specific terms. This functionality can be valuable for refining the manuscript writing style, for instance by identifying an overuse of transitional words like "however".

## Citation management with Zotero and Better BibTeX

### Get and set up Zotero and the Better BibTeX plugin

Better BibTeX is a plugin for Zotero that enhances its reference management capabilities for LaTeX users. It provides tools for generating, managing, and customizing BibTeX and BibLaTeX entries, making it a valuable citation tool within LaTeX environments. Better BibTeX offers several functionalities that make it a preferred choice:

- Citation key management allows custom citation key generation, offering more control over key formatting.
- Automatic export and continuously updated BibTeX and BibLaTeX exports ensure that the bibliography is always in sync with the Zotero library.
- Handling of special characters prevents BibTeX / BibLaTeX errors.
- Cite-as-you-write support for TeX (e.g., TeXstudio) and even Markdown editors.


To install Better BibTeX for Zotero, follow these steps:

1. Ensure you have the latest version of Zotero installed on your system. You can download it from the [Zotero website](https://www.zotero.org).

2. Download Better BibTeX:
   - Go to the official [Better BibTeX GitHub repository](https://github.com/retorquere/zotero-better-bibtex).
   - Download the latest release of the plugin -- make sure to choose the `.xpi` file of the lates release.

3. Install the plugin in Zotero:
   - Open Zotero
   - In Zotero, navigate to *Tools* in the top menu and select *Add-ons*
   - In the Add-ons Manager, click the gear icon in the top-right corner and choose *Install Add-on From File*
   - Locate the downloaded `.xpi` file and click *Open* - Zotero will install the plugin.
   - Restart Zotero to activate the plugin.

4. Configure Better BibTeX:
   - After installation, you will find Better BibTeX settings in the Zotero Preferences (Windows) or Settings (Linux) menu under the *Better BibTeX* tab.
   - Set up your citation key format and export preferences according to your workflow; our recommendation:
     ```
     auth.lower + year + shorttitle(1,1).lower
     ```

5. Export and use:
   - To export a bibliography, select the desired references in Zotero, right-click, and choose *Export Items*
   - Select *Better BibTeX* as the export format; note that the *Better BibLaTeX* may not produce the desired functionality and cause untraceable error messages when compiling a `.tex` file.
   - Optionally, check the *keep updated* box in the next window

For the domains of water resources reasearch and hydraulic engineering, you may want to work with our hydro-informatics.com library: [https://www.zotero.org/groups/4917569/hydro-informatics/library](https://www.zotero.org/groups/4917569/hydro-informatics/library).

(debug-zotero)=
### Auto-merge multiple duplicates

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



## Report writing template

For detailed installation instructions, working with TexStudio, and setting up LaTeX documents, please have a look at our LaTeX thesis template at [https://github.com/Ecohydraulics/latex-thesis-template](https://github.com/Ecohydraulics/latex-thesis-template).

## Bibliography

When working with LaTeX, bibliography management typically involves using a .bib file that contains all your references, which you cite within the `.tex` document using `\cite{...}` (or similar) commands. To transform these citations and references into a properly formatted bibliography, you iteratively run a tool like BibTeX after compiling your LaTeX document. **Note that TexStudio does these iterations automatically during compiling**, so these descriptions only explain why you may see the compiling process restart several times even though you only pressed the "Compile" button once.

BibTeX reads the `.aux` file of a previous compiling of the `.tex` document, locates the relevant entries in the `.bib` file, and then creates a `.bbl` file containing only the cited references, now formatted according to the style rules defined by a bibliography style file ( for instance, a `.bst` file when using BibTeX). These style files control the appearance and arrangement of citations and references, including how authors, titles, and journal names are displayed. Once the `.bbl` file is generated, LaTeX incorporates it into the final PDF document during the next compilation run. The `.bbl` file thus is a fully formatted subset of the `.bib` database, ensuring that the PDF document displays only the actually cited references, arranged and styled according to the chosen formatting guidelines.

To manage your reference database and generate a `.bib` file, we recommend using tools like [Zotero](https://www.zotero.org/) (with additional tips in the {ref}`Zotero Tips <debug-zotero>` section). Our [LaTeX thesis template](https://github.com/Ecohydraulics/latex-thesis-template) provides more guidance on working with Zotero and managing the `.bib` file.
