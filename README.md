# Integration Tester
![You got da style?](https://github.com/Liamdoult/integration-tester/workflows/You%20got%20da%20style%3F/badge.svg)
![You got da tests?](https://github.com/Liamdoult/integration-tester/workflows/You%20got%20da%20tests%3F/badge.svg)

Provides an easy interface for integration testing.

This solution utilises docker containers to instantiate the application.

Currently supports:
- MongoDB


## Style
All code should follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). The repository includes automated scripts for testing your code style. To run the scripts enter:
``` bash
pip install yapf pylint pycodestyle
sh style.sh
```
This script will format the code using `yarf`, check with `pylint` and then check with `pycodestyle`. Please ensure you resolve any issues identified by any of the tools anr your PR will not be reviewed.

You may use `# pylint: disable=xxx` but please include a follow-up comment with reasoning.
