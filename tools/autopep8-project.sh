#!/bin/sh
<<<<<<< HEAD
find . -name "*.py" | xargs autopep8 -i --max-line-length=119

=======
find . -name "*.py" -or -name "config.py-example" | xargs autopep8 -i
>>>>>>> d95c7f9f75381c6bac64c7213dceb24c91ae9e74
