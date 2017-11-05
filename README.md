# CONTRIBUTING.md
Follow the following instructions to contribute to our system.

Fork the repo first, then execute the following commands:
```
git clone <url of your fork repo>
cd mess
virtualenv messenv
source messenv/bin/activate
pip install django
pip install beautifulsoup
pip install bs4
cd automation
python manage.py runserver &
```

In case you don't have virtualenv:
```
pip install virtualenv
```

In case you don't want to use virtualenv:
```
git clone <url of your fork repo>
cd mess
[sudo] pip install django
[sudo] pip install beautifulsoup
[sudo] pip install bs4
python manage.py runserver &
```

Now your development server should be ready. Commit and push your changes to your repo and when you've made a considerable change, make a PR.

Happy Contributing!
