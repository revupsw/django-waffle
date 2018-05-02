.. _about-contributing:
.. highlight:: shell

======================
Contributing to Waffle
======================

Waffle is pretty simple to hack, and has a decent test suite! Here's how
to patch Waffle, add tests, run them, and contribute changes.

**Please** `open a new issue`_ to discuss a new feature before beginning
work on it. Not all suggestions are accepted. The :ref:`Goals
<about-goals>` may help guide which features are likely to be accepted.


Set Up
======

Setting up an environment is easy! You'll want ``virtualenv`` and
``pip``, then just create a new virtual environment and install the
requirements::

    $ mkvirtualenv waffle
    $ pip install -r requirements.txt

Done!


Writing Patches
===============

Fork_ Waffle and create a new branch off master for your patch. Run the
tests often::

    $ ./run.sh test

Try to keep each branch to a single feature or bugfix.

.. note::

    To update branches, please **rebase** onto master, do not merge
    master into your branch.


Submitting Patches
==================

Open a pull request on GitHub!

Before a pull request gets merged, it should be **rebased** onto master
and squashed into a minimal set of commits. Each commit should include
the necessary code, test, and documentation changes for a single "piece"
of functionality.

To be mergable, patches must:

- be rebased onto the latest master,
- be automatically mergeable,
- not break existing tests (TravisCI_ will run them, too),
- not change existing tests without a *very* good reason,
- add tests for new code (bug fixes should include regression tests, new
  features should have relevant tests),
- not introduce any new flake8_ errors (run ``./run.sh lint``),
- include updated source translations (run ``./run.sh makemessages`` and ``./run.sh compilemessages``),
- document any new features, and
- have a `good commit message`_.

Regressions tests should fail without the rest of the patch and pass
with it. 


.. _open a new issue: https://github.com/jsocol/django-waffle/issues/new
.. _Fork: https://github.com/jsocol/django-waffle/fork
.. _TravisCI: https://travis-ci.org/jsocol/django-waffle
.. _flake8: https://pypi.python.org/pypi/flake8
.. _good commit message: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
