.. _starting-installation:

============
Installation
============

After ensuring that the :ref:`requirements <starting-requirements>` are
met, installing Waffle is a simple process.


Getting Waffle
==============

Waffle is `hosted on PyPI`_ and can be installed with ``pip`` or
``easy_install``:

.. code-block:: shell

    $ pip install django-waffle
    $ easy_install django-waffle

Waffle is also available `on GitHub`_. In general, ``master`` should be
stable, but use caution depending on unreleased versions.

.. _hosted on PyPI: http://pypi.python.org/pypi/django-waffle
.. _on GitHub: https://github.com/jsocol/django-waffle


.. _installation-settings:

Settings
========

Add ``waffle`` to the ``INSTALLED_APPS`` setting, and
``waffle.middleware.WaffleMiddleware`` to ``MIDDLEWARE_CLASSES``, e.g.::

    INSTALLED_APPS = (
        # ...
        'waffle',
        # ...
    )

    MIDDLEWARE_CLASSES = (
        # ...
        'waffle.middleware.WaffleMiddleware',
        # ...
    )


.. _installation-settings-templates:

Jinja Templates
---------------

.. versionchanged:: 0.11

If you're using Jinja2 templates, Waffle provides a Jinja2 extension
(``waffle.jinja.WaffleExtension``) to :ref:`use Waffle directly from
templates <templates-jinja>`. How you install this depends on which
adapter you're using.

With django-jinja_, add the extension to the ``extensions`` list::

    TEMPLATES = [
        {
            'BACKEND': 'django_jinja.backend.Jinja2',
            'OPTIONS': {
                'extensions': [
                    # ...
                    'waffle.jinja.WaffleExtension',
                ],
                # ...
            },
            # ...
        },
        # ...
    ]

With jingo_, add it to the ``JINJA_CONFIG['extensions']`` list::

    JINJA_CONFIG = {
        'extensions': [
            # ...
            'waffle.jinja.WaffleExtension',
        ],
        # ...
    }


Database Schema
===============

Waffle includes `Django migrations`_ for creating the correct database
schema. If using Django >= 1.7, simply run the ``migrate`` management
command after adding Waffle to ``INSTALLED_APPS``:

.. code-block:: shell

    $ django-admin.py migrate

If you're using a version of Django without migrations, you can run
``syncdb`` to create the Waffle tables.

.. _Django migrations: https://docs.djangoproject.com/en/dev/topics/migrations/
.. _django-jinja: https://pypi.python.org/pypi/django-jinja/
.. _jingo: http://jingo.readthedocs.org/
