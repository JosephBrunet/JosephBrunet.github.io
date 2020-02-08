---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}
You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>

{% include base_path %}


2020
------
+ Brunet J., Pierrat B., and Badel P. Review of current advances in the mechanical description and quantification of aortic dissection mechanisms.
*IEEE Reviews in Biomedical Engineering, 2020*<br>
[Paper](/files/2019_paper.pdf)

2019
------
+ Brunet J., Pierrat B., Maire E., Adrien, J., and Badel P. A combined experimental-numerical lamellar-scale approach of tensile rupture in arterial medial tissue using X-ray tomography.
*Journal of the mechanical behavior of biomedical materials, 2019*<br>
[Paper](https://www.google.com)

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
