---
layout: page
title: projects
permalink: /projects/
description: Selected research and scientific-software projects.
nav: true
nav_order: 3
display_categories: [software, research]
horizontal: false
---

{% if site.enable_project_categories and page.display_categories %}
  {% for category in page.display_categories %}
  <h2>{{ category }}</h2>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  {% for project in sorted_projects %}
    {% include projects.liquid %}
  {% endfor %}
  {% endfor %}
{% else %}
  {% assign sorted_projects = site.projects | sort: "importance" %}
  {% for project in sorted_projects %}
    {% include projects.liquid %}
  {% endfor %}
{% endif %}
