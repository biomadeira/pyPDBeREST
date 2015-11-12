# pyPDBeREST
A python wrapper for the [PDBe REST API](http://www.ebi.ac.uk/pdbe/api/doc/), inspired by [pyEnsemblRest](https://github.com/pyOpenSci/pyEnsemblRest).

**DISCLAIMER** - This project is still not functional and under development.


### Setup

```
git clone https://github.com/biomadeira/pyPDBeREST.git 
cd pyPDBeREST
sudo python setup.py install
```

### Example usage
For a full set of examples see the [ipython notebook](Examples.ipynb). For the impatient see below.

### Quickstart

##### Endpoints
Loading the module...

```python
from pdbe import pyPDBeREST
p = pyPDBeREST()
```

Alternatively overriding the base url for the endpoints... 

```python
# using new ednpoints in the dev branch of the api
p = pyPDBeREST(base_url='http://wwwdev.ebi.ac.uk/pdbe/api/doc/')
```

Printing out all the available method endpoints...

```python
print(p.methods())
```

...and respective output.


```
Some output.
```


Printing out all the available endpoints...

```python
print(p.PDB.endpoints())
```

...and respective output.


```
Some output.
```


##### GET
Example of a GET query...

```python
p = pyPDBeREST.PDB.getSummary(pdbid='1cbs')
```

...and respective output.


```javascript
{ "some": "json" }
```


##### POST
Not all endpoints enable post requests. Those will raise a `PostNotSupported()` exception.
An example POST query...
 
```python
# up to 1000 pdb ids can be queried with post methods
p = pyPDBeREST.PDB.getSummary(pdbid=['1cbs', '2pah'])
```
 
...and respective JSON output.


```javascript
{ "some": "json" }
```


### Dependencies
See the necessary [requirements](requirements.txt) for this module.


### Contributing and Bug tracking
Feel free to fork, clone, share and distribute. If you find any bugs or issues please log them in the [issue tracker](https://github.com/biomadeira/pyPDBeREST/issues).


### License
GNU General Public License v3 (GPLv3). See [license](LICENSE.md) for details.

