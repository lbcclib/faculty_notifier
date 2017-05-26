# Faculty notifier

This set of python code reads in data from Evergreen ILS, creates a Web site featuring recently purchased books, and sends emails notifying folks on campus when books in their disciplines arrive.

## Installing Factulty notifier

Here's how to get this running for yourself:

1. Make sure that Python 2.7.x is running on your computer
2. Install the correct libraries.
```
pip install email lxml pyyaml
````
3. Move the `public` directory to a directory that might be served up by a web server.

## Configuring this software for your unique institution

1. Correctly configure all the YAML files in the `conf` directory
2. Add the correct email addresses to `faculty_notifications.py`.  Your institution almost certainly has different departments and interests than ours does, so you will also probably have to modify existing or create new regular expressions.
3. You may wish to send books to certain folks based on some characteristic other than call number ranges.  To do this:
    1. Add some code to the `__init__` method in the `Book` class to make sure that all Book objects contain enough data to identify them.  
    2. Using the `SpanishInterestGroup` class as an example, add an inherited class to `department.py`.
    3. Add the name of your new inherited class to the appropriate `import` statement in `faculty_notifications.py`
    4. Also in `faculty_notifications.py`, append an object of your new class to the `departments` list.

## Contributing to this software

1. Sign in to GitHub.
2. Click "Fork" to make your own working copy of the repo.
3. Follow the installation instructions.
4. Make your changes.
5. Submit a pull request to get your changes incorporated. This sounds complicated, but it's actually pretty simple:
    1. Go to your forked repository.
    2. Click the pull requests tab
    3. Click New Pull Request.
    4. Verify your changes, then click "Create pull request".

