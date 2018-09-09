# mezzipyblog

Ever wanted to add [Jupyter](http://jupyter.org/) notebooks to your
[Mezzanine](http://mezzanine.jupo.org/) powered blog? This repository will
let you do this.

## Installation

* Let's assume you have Mezzanine installed. You've also got to install
jupyter in your virtual environment:

    ```pip install jupyter```

* Clone or download this repository somewhere where it would be detected by
a running Mezzanine instance. In particular, you should be able to edit
`INSTALLED_APPS` as so as to add mezzipynb before mezzanine.blog:

```python
INSTALLED_APPS = (
#...
    'mezzipyblog',
    "mezzanine.blog",
#...
)
```
* This package uses Mezzanine's[Field Injection](http://mezzanine.jupo.org/docs/model-customization.html)
functionality to add otebook capacity to this CMS's own blog model. To do
this, please add the following code somewhere else in settings.py:

```python
EXTRA_MODEL_FIELDS = (
  (
    "mezzanine.blog.models.BlogPost.notebook",
    "django.db.models.FileField",
    ("Notebook",),
    {"blank": True, "upload_to": "blog", 'max_length': 150},
  ),
)
```

* You will also need to modify your Mezzanine project's urls.py file. At the
top, place among the import statements:

```python
# Trailing slashes for urlpatterns based on setup.
_slash = "/" if settings.APPEND_SLASH else ""
from mezzipyblog import views
```

And below it, just after `# url("^$", mezzanine.blog.views.blog_post_list, name="home"),` is commented out:

```python
# url("^$", mezzanine.blog.views.blog_post_list, name="home"),
url("^blog/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/"
    "(?P<slug>.*)%s$" % _slash,
    views.blog_post_detail, name="blog_post_detail_day"),
url("^blog/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>.*)%s$" % _slash,
    views.blog_post_detail, name="blog_post_detail_month"),
url("^blog/(?P<year>\d{4})/(?P<slug>.*)%s$" % _slash,
    views.blog_post_detail, name="blog_post_detail_year"),
url("^blog/(?P<slug>.*)%s$" % _slash,
    views.blog_post_detail, name="blog_post_detail"),
```

* Finally, you will need to migrate the new blog model. Please run:

    ```python manage.py makemigrations```

* If you are prompted, please choose option 2. To finalise, run:

    ```python manage.py migrate```

## Usage

The "mezzipyblog" app works similar to Mezzanine's existing blog application.
The big difference is that admins can choose to upload Jupyter notebook files
(via the *Notebook* file input control). One difference with this app is that
*Content* is not necessary if *Notebook* is provided; some blog authors may
just want the notebook to speak for itself. It is also possible to publish
with **both** *Content* and *Notebook*.

## License

3-clause BSD.

## Author

Peter Murphy, 2018.
