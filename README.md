# BRISC - BRIT Rapid Inventory of Specimen Collections

BRISC was developed at the Botanical Research Institute of Texas to facilitate the rapid inventory of over 1 million plant specimens in the BRIT Herbarium. BRISC is a Django web application which is designed to allow collections staff and volunteers to inventory the contents of a collection using wireless tablets and laptops.

Details of the BRIT inventory are available at http://www.brit.org/herbarium/inventory

BRISC is currently stable but should not yet be used in a production environment. Since the BRIT inventory was conducted with the server only accessible within the BRIT facility, no precautions were made to require login to protect the quality of the data from bots or mischievous humans.

## Quick Start
The following steps will be familiar to anyone accustomed to running Django apps, but more detailed instructions are forthcoming.

```
git clone https://github.com/jbest/brisc.git
virtualenv env
source env/bin/activate
pip install -r requirements-local.txt
python manage.py runserver 127.0.0.1:8000
go to http://127.0.0.1:8000
```


The majority of the taxon names were generously provided by Tropicos (Tropicos.org, Missouri Botanical Garden, 08 Apr 2016, www.tropicos.org). 