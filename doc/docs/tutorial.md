## Writing a clinical service with OPAL

This tutorial will walk you through the creation of a new OPAL service.

The application we're going to be building will help clinical users to manage the patients on a ward in a hospital.

<blockquote class="custom-quote"><p><i class="fa fa-user-md fa-3x"></i>
As a Doctor <br />
I want to know what's going on with the patients under my care<br />
So that I can treat them effectively and safely.
</p></blockquote>

### Bootstrapping a new project

We assume that you've already [Installed OPAL](installation.md). You can tell which version of opal is installed 
by running this command

    $ opal --version

At the start a new project, OPAL will bootstrap the initial project structure, including
a Djano project, some core datamodels (complete with JSON APIs) and a general application structure.

From the commandline: 

    $ opal startproject mynewapp

This will create a mynewap directory where your new project lives. 

Let's have a look at what that created for you:


    mynewapp/                   # Your project directory
        LICENSE                 # A dummy LICENSE file
        Procfile                # A procfile ready for deployment to e.g. Heroku
        README.md
        manage.py               # Django's manage.py script
        requirements.txt        # Requirements file ready for your project
        
        data/                   # A dummy directory for fixtures
        
        mynewapp/               # The actual python package for your application
             __init__.py
            flow.py             # How patients move through your services
            models.py           # Data models for your application 
            schema.py           # The list schemas for your application
            settings.py         # Helpfully tweaked Django settings
            tests.py            # Dummy unittests
            urls.py             # Django Urlconf
            wsgi.py             

            assets/             # Your static files directory
            templates/          # Your template directory
            migrations/         # Your Database migrations directory


### Test it out 

The scaffolding step has generated you a working project - so let's check that out

    cd mynewapp
    python manage.py runserver

If you now visit `http://localhost:8000` in your browser, you should see the standard login screen:

<img src="/img/tutorial-login.png" style="margin: 12px auto; border: 1px solid black;"/>

The scaffolding step created you a superuser, so try logging in with the credentials: 

* Username: _super_
* Password:  _super1_

When you log in you should be presented with a welcome screen that shows you the three
areas that are enabled by default - team lists, search and the admin area.

<img src="/img/tutorial-welcome.png" width="600" style="margin: 12px auto; border: 1px solid black;"/>

OPAL applications are a collection of single page Angular apps that talk to the Django
server-side layer via JSON APIs. The Team Lists and Search options here are two examples of
front-end Angular single page apps.

### Team lists

Most clinical services will need at some stage to generate a list of patients - so OPAL provides
this functionality enabled by default.

The [list view](/guides/list_views/) is a spreadhseet-style list of patients - try navigating
to the list view and adding a patient with the `add patient` button.

<img src="/img/tutorial-list.png" width="600" style="margin: 12px auto; border: 1px solid black;"/>

Each column contains a different type of information about a patient, while each
row represents one patient.

<blockquote><small>
Strictly speaking each row is an <a href="/guides/datamodel/">episode</a>
of care for a patient - but we'll come to that in a second.
</small></blockquote>

The columns you see initially are just a few of the standard clinical models that come with
OPAL - for instance the Diagnosis model in your new application inherits from a model that
looks a lot like this:

    class Diagnosis(EpisodeSubrecord):
        condition         = ForeignKeyOrFreeText(Condition)
        provisional       = models.BooleanField(default=False)
        details           = models.CharField(max_length=255, blank=True)
        date_of_diagnosis = models.DateField(blank=True, null=True)
    
        class Meta:
            abstract = True

### Lookup Lists

You will notice that the condition field has a custom field type - `ForeignKeyOrFreeText`.
This is a custom field type that we use with OPAL when we want to use a
[Lookup List](/guides/lookup_lists/).

Lookup Lists allow us to reference canonical lists of available terminology as a foreign key, while
also allowing synonymous terms, and a free text override. That means that we can ensure that 
we record high quality coded data, while allowing users an easy way to enter unusual edge
cases.

You'll need to import the data for a terminology before you can start to take advantage of that.
For now, let's use the reference data from elCID: 

    wget https://raw.githubusercontent.com/openhealthcare/elcid/master/data/lookuplists/lookuplists.json -P data/lookuplists


<blockquote><small>
By convention, we store data in the <code>./data/lookuplists</code> directory of our project.
</small></blockquote>

Now let's import the data:

    python manage.py load_lookup_lists -f data/lookuplists/lookuplists.json

Now try adding a new diagnosis to your patient - as you start to type in the condition field,
you'l see that the conditions we just imported appear as suggestions: 

<img src="/img/tutorial-conditions.png" style="margin: 12px auto; border: 1px solid black;"/>

### Add your own data models

So far we've begun to get a sense of the batteries-included parts of OPAL, 
but before long, you're going to need to create models for your own needs.

Most OPAL models are [Subrecords](/guides/datamodel/) - they relate to either a patient, or
an episode (an episode is for example, an admission to hospital).

Let's see how that works by creating a TODO list model that is assigned to
episodes of care. In your `mynewapp/models.py` : 

    class TODOItem(models.EpisodeSubrecord):
        job       = fields.CharField(max_length=200)
        due_date  = fields.DateField(blank=True, null=True)
        details   = fields.TextField(blank=True, null=True)
        completed = fields.BooleanField(default=False)
          
This is simply a Django model, apart from the parent class `models.EpisodeSubrecord` 
which provides us with some extra functionality: 

* A relationship to an episode, linked to a patient
* JSON APIs for creating, retrieving and updating it
* Ensuring that the OPAL Angular layer knows it exists

Next, we're going to let OPAL take care of the boilerplate that we'll need to use this
model in our application. From the commandline: 

    $ opal scaffold mynewapp

Let's take a look at what that did: 

* It created a south migration (Migrations live in `mynewapp/migrations`)
* It created a detail template `mynewapp/templates/records/todo_item.html`
* It created a form template `mynewapp/templates/modals/todo_item_modal.html`

#### Detail template

The default detail template simply displays each field on a new line:

    <span ng-show="item.job">[[ item.job ]] <br /></span>
    <span ng-show="item.due_date">[[ item.due_date  | shortDate ]] <br /></span>
    <span ng-show="item.details">[[ item.details ]] <br /></span>
    <span ng-show="item.completed">[[ item.completed ]] <br /></span>

#### Form template

The default form template will display each field on a new line, with some basic
appropriate form field types set.
It uses the OPAL form helpers templatetag library.

    {% extends 'modal_base.html' %}
    {% load forms %}
    {% block modal_body %}
      <form class="form-horizontal">
       {% input  label="Job" model="editing.job"  %}
       {% datepicker  label="Due Date" model="editing.due_date"  %}
       {% textarea  label="Details" model="editing.details"  %}
       {% checkbox  label="Completed" model="editing.completed"  %}
      </form>
    {% endblock %}

#### Adding TODOs to our Team Lists

Now let's add our TODO list model as a column in the Spreadsheet-like list view.

The columns for team lists are set in `mynewapp/schemas.py` as a list of models.

Open mynewapp/schemas.py and edit the `list_columns` variable to add `models.TODOItem` as
the final item:

    list_columns = [
        models.Demographics,
        models.Location,
        models.Allergies,
        models.Diagnosis,
        models.PastMedicalHistory,
        models.Treatment,
        models.Investigation,
        models.TODOItem
    ]

Refresh the lists page in your browser, and you'll see your new column on the end - add a
TODO item, noting how we automatically get appropriate form types like datepickers and
checkboxes.

### Set an Icon for your model

You'll notice that your new column is the only one without an icon - we set the icon by
adding the following property to your `TODOItem` class: 

        _icon = 'fa fa-th-list'

### JSON APIs 

OPAL automatically creates self-documenting JSON APIs for your interacting with the data
in your application. You can inspect these APIs interactively at the url: 

    http://localhost:8000/api/v0.1/


<img src="/img/tutorial-api.png" style="margin: 12px auto; border: 1px solid black;"/>

### What next?

This is just a glimpse at the full range of functionality that comes with OPAL - there is
much more to discover in the [Topic Guides](/guides/topic-guides/).