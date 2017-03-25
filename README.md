# Faculty notifier

This set of python code reads in data from Evergreen ILS, creates a Web site featuring new books, and sends emails notifying folks on campus when books in their disciplines arrive

## Installing Factulty notifier

Here's how to get this running for yourself:

1. Make sure that Python 2.7.x is running on your computer
2. Install the correct libraries.
```
pip install email lxml pyyaml
````
3. Correctly configure all the YAML files in the `conf` directory
4. Move the `public` directory to a directory that might be served up by a web server.

## Contributing to this software

1. Sign in to GitHub.
2. Click "Fork" to make your own working copy of the repo.
3. Follow the installation instructions.
4. Make your changes.
5. Submit a pull request to get your changes incorporated. This sounds complicated, but it's actually pretty simple:
  * Go to your forked repository.
  * Click the pull requests tab
  * Click New Pull Request.
  * Verify your changes, then click "Create pull request".

