#!/bin/bash

# Check for changes in users directory
CHANGED_USERS=$(git diff --cached --name-only | grep -E '^ctim/(config|compose/local|requirements/base\.txt|requirements/local\.txt|contrib|users)/' | wc -l)

# Check for changes in ctia directory
CHANGED_CTIA=$(git diff --cached --name-only | grep -E '^ctim/(config|compose/local|requirements/base\.txt|requirements/local\.txt|ctim/contrib|ctim/ctia)/' | wc -l)

# Print reminders based on changes
if [ "$CHANGED_USERS" -ne 0 ]; then
    echo "Don't forget to run: docker compose -f local.yml run --rm django python manage.py test ctim.users.tests"
fi

if [ "$CHANGED_CTIA" -ne 0 ]; then
    echo "Don't forget to run: docker compose -f local.yml run --rm django python manage.py test ctim.ctia.tests"
fi
