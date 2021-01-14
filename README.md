# pelican-revealmd

Reveal-md allows you to write reveal.js presentations in markdown, in the same way you write markdown
posts for pelican.

```markdown
Title: My awesome presentation
Date: 2018-08-08
Category: talks
Summary: This is my summary

# Presentation

With reveal.js!

# Second slide

With whatever you want here
```

# Showing your work on your website

Pelican does render markdown into html, but for revealjs a different set of changes need to be taken into consideration, hence, this plugin will help as long as you follow some steps:

Save your file as `my_presentation.revealjs`, add

```python
PLUGINS = ["revealmd"]
```

to your `pelicanconf.py` and your presentation will be automatically rendered for you using the required `pandoc` utility installed on your system.

You also need to use the provided html template instead of trying to embed the presentation within the templates provided by your theme. Revealmd provides a revealmd html template for this purpose, but in your configuration file, the templates path needs to be specified:

```python
EXTRA_TEMPLATES_PATHS = [
    "path/to/revealmd/templates",  # eg: "plugins/revealmd/templates"
]
```

If you use git to manage your site, you could do something like

```
git submodule add https://github.com/iranzo/pelican-revealmd.git plugins/revealmd
```

to install the plugin

# Additional information

The process of conversion and showing the presentation might alter it (will not directly show as good as with reveal-md), this happens because:

- This plugin does use `pandoc`, the conversion it performs might alter the data, for example, losing horizontal-vertical slides and others.
