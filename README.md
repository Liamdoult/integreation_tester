# Integration Tester

![Python tests](https://github.com/Liamdoult/integration-tester/workflows/Python%20tests/badge.svg)

Reduce the development time of tests through the reduction in mocking and reduce the runtime of tests through reducing the restarts of containers.

The objective of this project is to reduce the time it takes to develop tests through reducing the quantity of mocks. This is achieved by bringing integration tests to the development environment.

Utilising Docker, this tool automatically runs, resets, stops and cleans the containers allowing the developer to test their code on real services as opposed to mockups.

## Supported Services
Currently supports:
- MongoDB
- Redis
- RabbitMQ

## Installation
Currently the application can only be installed directly from GitHub:

    pip install https://github.com/Liamdoult/integration-tester

## Example Use
``` python
import integration_tester

driver = integration_tester.MongoDriver()

driver.wait_until_ready()
# test code
driver.reset()
```

## Contribution
If you wish to contribute to the project please see the [contribution](https://github.com/Liamdoult/integration-tester/blob/master/CONTRIBUTION.md) documentation and the [Code of Conduct](https://github.com/Liamdoult/integration-tester/blob/master/CODE_OF_CONDUCT.md).
