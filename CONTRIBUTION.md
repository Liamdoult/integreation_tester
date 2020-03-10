# Contributing

- When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change. 
- Please note we have a [code of conduct](https://github.com/Liamdoult/integration-tester/blob/master/CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

## TLDR Section:
This section is for those more experienced with GitHub and contributions. However, everything mentioned here is covered below in the _in-depth section_.

### Style
All code should follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). An automated script for formatting and enforcing styles has been implemented with bash. Please resolve all issues raised by the script prior to making a PR.

    sh scripts/style.sh

_NB_: This script makes in-place changes to the code.

### Tests
All tests are written using pytest and can be run using distribution tools.

    python setup.py test

### Contribution Steps
1. Fork
2. Create Branch
3. Make changes
4. Run `sh scripts/style.sh`
5. Run `python setup.py test`
6. Push fork
7. Create PR and link issue

## In-depth Section
This section serves as a detailed reference to the above "TLDR" section. This section is for beginners who have never contributed before and experienced contributors who might want clarification.

### Forking
Forking a repository to your local GitHub is a common first step to contributing to many repositories. Forking the repository creates a copy of the main repository on your personal GitHub profile. This allows you to control the settings and permissions of an exact copy of the main repository. Automatically this change in owner ship allows you to create your own branch and make pushes to GitHub (your personal copy of the repository). If you are not familiar with `Forking` and how you will be able to contribute to the main repository, this will be explained in the _Pull Request Process_ section. 

To fork the repository you can click on the `fork` button and follow the steps.

![image](https://user-images.githubusercontent.com/12427907/76245795-7214ab00-6234-11ea-9212-ea8127e1c636.png)

### Cloning
Once you have forked the repository, you will need to download the code so that you can make the changes on your local machine. This "downloading" is referred to as "cloning". If you are using Linux, gitbash or Windows Subsystem for Linux you can run:

    git clone https://github.com/<user_name>/integration-tester

_NB_: Don't forget to replace `<user_name>` with your GitHub username.

Once you have cloned the repository you will have a folder `integration-tester`. The final step is to create a branch to make your changes on:

    git checkout -b <meaningful-branch-name>

You are now ready to make your changes to the codebase.

### Style
This project makes use of the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). Luckily we have a script to simplify this process. This script will automatically format your code as much as it can according. However, it may not be able to resolve all issues. For these issues you will have to manually resolve the issues.
To run the script you will need to install the following formatting tools:

    pip install yapf pylint pycodestyle

Once the tools are installed you can run the script by running:

    sh scripts/style.sh


This script will format the code using `yarf`, check with `pylint` and then check with `pycodestyle`. 

A correct output from the system should appear like this:

![image](https://user-images.githubusercontent.com/12427907/76245587-0e8a7d80-6234-11ea-9917-70e94917aa15.png)

If not you should have an output with an error message like this:

![image](https://user-images.githubusercontent.com/12427907/76245694-3bd72b80-6234-11ea-9db4-39856dd0c188.png)

It is important to resolve these issues prior to pushing code as your Pull Request will not be reviewed.


### Tests
Now that you have got some style lets make sure the code is working correctly. In this project we make use of _pytest_. If you are not someone who practices Test Driven Development you will need to write your tests at this point. Once the tests are written you need to make sure the test suite passes on all tests. For this you will require docker running.
To run the test suite:

    python setup.py test

This will install everything needed and run the entire suite.

If your tests are all passing you can go ahead and create a Pull request.


### Pull Request Process

Before you can make a PR (Pull Request) you need to make sure you have completed all the required tasks aside from making your changes and testing them.

PR checklist:
1. Style test passes
2. Test suite passes
3. Documentation updated

Once you are certain everything is ready, you can begin the process of creating your PR. You can start by pushing your local branch to the forked repository.

    git push origin <branch_name>

Where `<branch_name>` is the name of the branch you created and checked out.

Once you have successfully pushed the branch you can go to the forked GitHub page. You can find this at `https://www.github.com/<username>/integration-tester`
You can now create a PR to LiamDoult/integration-test master branch.
