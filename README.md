# HasBin -- an interface for binning and classifying diagnostic genes

## getting started

1. Check out from git
2. Setup a virtualenv

   ```shell
   # From within the checked-out directory, create the venv (needs to be done once per checkout)
   virtualenv venv
   # activate the virtualenv (needs to be done for subsequent logins, as well):
   source venv/bin/activate
   # Install dependencies
   pip install -r requirements.txt
   ```

3. Setup the database:

   ```shell
   # Standard django setup (will ask for superuser account):
   python manage.py syncdb
   # Load the HUGO data:
   # you can get the hugo data with something like:
   #   curl -H'Accept:application/json' http://rest.genenames.org/fetch/status/Approved | gzip -c > hgnc.approved.json.gz
   # (other possibilities for status, like 'Entry+Withdrawn' could also be included
   python manage.py load_hugo hgnc.approved.json.gz  # and wait a half-minute or so...
   # more fixtures later?
   ```

4. Start the server:

   ```shell
   python manage.py runserver
   ```

## Organization:

The main models and other code are in the hasbin subdirectory.

The django "project" directory is proj_hasbin.

## Miscellaneous

If you want a list of approved hugo symbols and the gene names:

   ```shell
   echo -e ".mode tabs\nselect symbol, name from hasbin_hugogene where status='Approved';" | sqlite3 db.sqlite3 | tee /tmp/hgnc-symbols
   ```
