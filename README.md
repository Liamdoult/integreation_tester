# Integreation Tester

Provides an easy interface for integreation testing.

This solution utilises docker containers to instatiate the application.

Currently supports:
- MongoDB


## Style
All code should follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). The repository includes automated scripts for testing your code style. To run the scripts enter:
``` bash
pip install yapf pylint pycodestyle
sh style.sh
```
THis script will format the code using yarf, check with pylint and then check with pycodestyle. Please ensure you relove any issues identified by any of the tools anr your PR will not be reviewed.

You may use `# pylint: disable=xxx` but please include a follow-up comment with reasoning.
