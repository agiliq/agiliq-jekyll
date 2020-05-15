---
layout: default
permalink: /authors/
title: Authors
---


<div class="author-page">  
{% assign items_grouped = site.posts | group_by_exp:"post", "post.author | downcase" %}
    {% for group in items_grouped %}
    <h3 class="author-name" id="{{group.name|slugize}}">{{group.name}}</h3>
       <ul>
        {% for item in group.items %}
           <li>
            <a href="{{item.url}}">{{item.title}}</a>
            </li>
        {% endfor %}
        </ul>
{% endfor %}
</div>