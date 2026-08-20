---
layout: page
title: code
permalink: /repositories/
description: Open-source and research software.
nav: true
nav_order: 4
---

{% if site.data.repositories.github_users %}
## GitHub
{% for user in site.data.repositories.github_users %}
{% include repository/repo_user.liquid username=user %}
{% endfor %}
{% endif %}

{% if site.data.repositories.github_repos %}
## Featured repositories
{% for repo in site.data.repositories.github_repos %}
{% include repository/repo.liquid repository=repo %}
{% endfor %}
{% endif %}
