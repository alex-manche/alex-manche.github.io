---
layout: page
title: publications
permalink: /publications/
description: Publications generated from a BibTeX library and synchronised from ORCID/DOI metadata.
nav: true
nav_order: 2
---

The bibliography below is generated from `_bibliography/papers.bib`. A scheduled GitHub Action can discover new DOI-bearing works from ORCID and Crossref, then refresh the BibTeX metadata automatically.

{% include bib_search.liquid %}

<div class="publications">
{% bibliography %}
</div>
