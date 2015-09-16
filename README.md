# ca.berlin.freifunk.net

## Development

Install and use virtualenv with:

```
virtualenv env
. env/bin/activate
```

Install dependencies with pip:

```
pip install -r requirements.txt
```


Setup the database

Open a python terminal and run
```
from app import db
db.create_all()
```

Run the application
```
python app.py
```
