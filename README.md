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
    - `cover_images.yml` will probably need no changes
    - `email.yml` is set up to be friendly to gmail addresses.  It might take some development to support cases in which a user's SMTP username is different than the user's email address
    - `email.yml` also includes a setting called `link`.  This will provide a link in the email to an HTML document in your public directory.  Change it to whatever URL will take folks to your `public` directory.
    - `evergreen.yml` is an important file to change.  `num_items_to_fetch` will depend on how often you add new items to your system, and how often you plan to send out emails (it's best not to have too much repitition, but you also don't want to miss out on items that might be of interest to folks).  `shelving_location` should be the shelving location the database ID of the shelving location your patrons are interested in (e.g. Adult Nonfiction might be represented by the number 143). `opac_host` must be a valid hostname from somewhere in your consortium.  And the `org_unit` is your org unit's shortname (e.g. ABCLIB).
    - `output.yml` includes a setting called `json_output_path`, which is where the script will generate a JSON file containing the new books.  This path needs to be somewhere within your `public` directory, and also in a directory where the user you'll run the script as has write permissions.  By default, the HTML file looks for a JSON file in the same folder with the name `newbooks.json`, so the easiest configuration is to set this value to `/path/to/public/directory/newbooks.json`.
    - `departments.yml` lists all the departments, what call number ranges they like, and what email addresses are included.  At minimum, you should add the correct email addresses to `departments.yml`. If multiple people will receive one notification, you can just add them as separate members of an array.  Your institution almost certainly has different departments and interests than ours does, so you will also probably have to modify existing or create new regular expressions.
4. You may wish to send books to certain folks based on some characteristic other than call number ranges.  To do this:
    1. Add some code to the `__init__` method in the `Book` class to make sure that all Book objects contain enough data to identify them.  
    2. Using the `SpanishInterestGroup` class as an example, add an inherited class to `department.py`.
    3. Add the name of your new inherited class to the appropriate `import` statement in `faculty_notifications.py`
    4. Also in `faculty_notifications.py`, append an object of your new class to the `departments` list.

## Running this software

1. `cd` to the directory that contains `faculty_notifications.py`
2. Run `python faculty_notifications.py`

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

