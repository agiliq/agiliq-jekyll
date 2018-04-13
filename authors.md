---
layout: default
permalink: /authors/
title: Authors
---


<div class="author-page">  
{% assign items_grouped = site.posts | group_by: 'author' %}
    {% for group in items_grouped %}
    <h3 class="author-name">{{group.name}}</h3>
       <ul>
        {% for item in group.items %}
           <li>
            <a href="{{item.url}}">{{item.title}}</a>
            </li>
        {% endfor %}
        </ul>
{% endfor %}
</div>