from django.shortcuts import render
from mezzanine.blog.models import BlogPost, BlogCategory
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
import nbformat
from nbconvert import HTMLExporter
from django.utils.safestring import mark_safe

def getipynbbodyandresources(filename):
    """ Takes an IPynbNotebook file (filename) - and returns HTML converted
    contents. """
    with open(filename, "rb") as f:
        contents = f.read().decode("UTF-8")
        theNotebook = nbformat.reads(contents, as_version=4)
        html_exporter = HTMLExporter()
        html_exporter.template_file = 'basic'
        (body, resources) = html_exporter.from_notebook_node(theNotebook)
        return (body, resources,)

# Handles Mezzanine blog pages (with embedded IPython/Jupyter notebook files).

def blog_post_detail(request, slug, year=None, month=None, day=None,
                     template="blog/blog_post_detail.html",
                     extra_context=None):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    blog_posts = BlogPost.objects.published(
                                     for_user=request.user).select_related()
    blog_post = get_object_or_404(blog_posts, slug=slug)
    if (blog_post.notebook) and (blog_post.notebook.path[-6:] == '.ipynb'):
        (notebody, noteresources) = getipynbbodyandresources(blog_post.notebook.path)
    else:
        (notebody, noteresources) = ("", "")
    related_posts = blog_post.related_posts.published(for_user=request.user)
    context = {"blog_post": blog_post, "editable_obj": blog_post,
               "related_posts": related_posts, "notebody": mark_safe(notebody)}
    context.update(extra_context or {})
    templates = [u"blog/blog_post_detail_ipynb.html", template]
    return TemplateResponse(request, templates, context)
