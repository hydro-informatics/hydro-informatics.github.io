---
title: Glossary 
tags: [formatting, special_layouts]
sidebar: mydoc_sidebar
permalink: mydoc_glossary.html
toc: false
folder: mydoc
---


Glossary items are stored in `_data/glossary.yml`. For every glossary item create a page and use definition list formatting, like this:

richtext
: {{site.data.glossary.richtext}}


Here is the code:

```
{% raw %}richtext
: {{site.data.glossary.richtext}}{% endraw %}
```

The glossary also works as a link in the top navigation bar.

## Horizontally styled definiton lists

You can also change the definition list (`dl`) class to `dl-horizontal`. This is a Bootstrap specific class. If you do, the styling looks like this:

<dl class="dl-horizontal">

<dt id="richtext">richtext</dt>
<dd>{{site.data.glossary.richtext}}</dd>

</dl>

For this type of list, you must use HTML. The list would then look like this:

```html
{% raw %}<dl class="dl-horizontal">

<dt id="richtext">richtext</dt>
<dd>{{site.data.glossary.richtext}}</dd>

</dl>{% endraw %}
```

If you squish your screen small enough, at a certain breakpoint this style reverts to the regular `dl` class.

{% include links.html %}
