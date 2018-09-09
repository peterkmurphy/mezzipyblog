from copy import deepcopy
from django.contrib import admin
from mezzanine.core.admin import (DisplayableAdmin, OwnableAdmin,
                                  BaseTranslationModelAdmin)
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost
from django.forms import ValidationError, ModelForm
from mezzanine.core.models import (
    Orderable, ContentTyped, SitePermission, CONTENT_STATUS_PUBLISHED)
from django.utils.translation import ugettext_lazy as _

# If we are going to load IPython/Jupyter notebooks, then we need to check that
# the content is valid.

import json

mandatorykeys = ['cells', 'metadata', 'nbformat', 'nbformat_minor']

def isvalidipynb(contents):
   """ Returns True if contents are that of a valid IPython notebook;
   returns False otherwise. Basically, must be a JSON object with the
   mandatory keys provided above.
   """
   try:
       data = json.loads(contents)

# Check whether keys are in there or not.

       datakeys = data.keys()
       for item in mandatorykeys:
           if item not in datakeys:
               return False;

# If there's an error with JSON Decoding, it's obviosly not JSON.

   except(json.decoder.JSONDecodeError):
       return False

# If the JSON data is not an object, it will throw an exception.

   except(AttributeError):
       return False

# Makes it here - it's ok/

   return True;

blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
blog_fieldsets[0][1]["fields"].insert(-2, "notebook")

class MezzIPynbAdminForm(ModelForm):

    def clean_content(form):
        status = form.cleaned_data.get("status")
        content = form.cleaned_data.get("content")
        notebook = form.cleaned_data.get("notebook")

# In the admin, users can provide a notebook file OR textual content;
# Unlike the normal Mezzanine blog, users don't have to provide text if
# a notebook isn't provided.

        if status == CONTENT_STATUS_PUBLISHED and not content and not notebook:
            raise ValidationError(_("This field is required if status "
                                    "is set as published and no notebook is "
                                    "provided." ))
        if notebook:
            notebookconts = notebook.read()
            notebookvalid = isvalidipynb(notebookconts)

# An exception is thrown if the file is not a valid notebook.

            if not notebookvalid:
                raise ValidationError(_("The file provided is not a "
                                        "valid Jupyter notebook."))
        return content

class MezzIPynbAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets
    form = MezzIPynbAdminForm


admin.site.unregister(BlogPost)
admin.site.register(BlogPost, MezzIPynbAdmin)
