#!/bin/bash

export PYTHONPATH=".:$PYTHONPATH"
export DJANGO_SETTINGS_MODULE="test_settings"

usage() {
    echo "USAGE: $0 [command]"
    echo "  test - run the waffle tests"
    echo "  lint - run flake8"
    echo "  shell - open the Django shell"
    echo "  makemigrations - create a schema migration"
    exit 1
}

CMD="$1"
shift

case "$CMD" in
    "test" )
        django-admin.py test waffle $@ ;;
    "lint" )
        flake8 waffle $@ ;;
    "shell" )
        django-admin.py shell $@ ;;
    "makemigrations" )
        django-admin.py makemigrations waffle $@ ;;
    "makemessages" )
        export DJANGO_SETTINGS_MODULE= && cd waffle && django-admin.py makemessages && cd - ;;
    "compilemessages" )
        export DJANGO_SETTINGS_MODULE= && cd waffle && django-admin.py compilemessages && cd - ;;
    "find_uncommitted_translations" )
        git diff --exit-code -G "^(msgid|msgstr)" || (echo "Please run ./run.sh makemessages and commit the updated django.po file." && false) ;;
    * )
        usage ;;
esac
