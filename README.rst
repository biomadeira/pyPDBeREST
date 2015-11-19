pyPDBeREST
==========

|Build Status| |Coverage Status| |License| |Twitter: @biomadeira|

A python wrapper for the `PDBe REST API`_, inspired by `pyEnsemblRest`_.

Setup
~~~~~

::

    git clone https://github.com/biomadeira/pyPDBeREST.git 
    cd pyPDBeREST
    sudo python setup.py install

Example usage
~~~~~~~~~~~~~

For a full set of examples and more details on all functionality see
these `notes`_. For the impatient see below.

Quickstart
~~~~~~~~~~

.. code:: python

    # loading the module...
    from pdbe import pyPDBeREST
    p = pyPDBeREST()

Alternatively overriding the base url for the endpoints…

.. code:: python

    # using the dev branch of the api
    p = pyPDBeREST(base_url='http://wwwdev.ebi.ac.uk/pdbe/')

Printing out all the available method endpoints…

.. code:: python

    print(p.endpoints())

::

    The following endpoints are available:
        EMDB
        SSM
        SEARCH
        SIFTS
        COMPOUNDS
        TOPOLOGY
        VALIDATION
        PDB
        PISA

Printing out all the available endpoints for one of the top level
methods…

.. code:: python

    print(p.PDB.endpoints())

::

    The following endpoints are available:
        getReleaseStatus
        getBindingSites
        getObservedRanges
        getRelatedPublications
        getResidueListingChain
        getNmrResources
        getExperiments
        getSecondaryStructure
        getVariousUrls
        getModifiedResidues
        getSummary
        getResidueListing
        getPublications
        getLigands
        getMutatedResidues
        getMolecules

GET
'''

.. code:: python

    # example of a GET query...
    data = p.PDB.getSummary(pdbid='1cbs')
    print(data)

.. code:: javascript 

    {
        "2pah": [
            {
                "related_structures": [], 
                "split_entry": [], 
                "title": "TETRAMERIC HUMAN PHENYLALANINE HYDROXYLASE", 
                "release_date": "19991006", 
                "experimental_method": [
                    "X-ray diffraction"
                ], 
                "experimental_method_class": [
                    "x-ray"
                ], 
                "revision_date": "20110713", 
                "entry_authors": [
                    "Stevens, R.C.", 
                    "Fusetti, F.", 
                    "Erlandsen, H."
                ], 
                "deposition_site": "BNL", 
                "number_of_entities": {
                    "polypeptide": 1, 
                    "dna": 0, 
                    "ligand": 1, 
                    "dna/rna": 0, 
                    "rna": 0, 
                    "sugar": 0, 
                    "water": 0, 
                    "other": 0
                }, 
                "processing_site": "RCSB", 
                "deposition_date": "19980526", 
                "assemblies": [
                    {
                        "assembly_id": "1", 
                        "form": "homo", 
                        "preferred": true, 
                        "name": "tetramer"
                    }
                ]
            }
        ]
    }


POST
''''

Not all endpoints enable post requests. Those will raise a
``NotImplementedError()`` exception.

.. code:: python

    # an example POST query...
    # up to 1000 pdb ids can be queried with post methods
    data = p.PDB.getSummary(pdbid='1cbs, 2pah', method='POST')
    print(data)

.. code:: javascript

    {
        "1cbs": [
            {
                "related_structures": [], 
                "split_entry": [], 
                "title": "CRYSTAL STRUCTURE OF CELLULAR RETINOIC-ACID-BINDING PROTEINS I AND II IN COMPLEX WITH ALL-TRANS-RETINOIC ACID AND A SYNTHETIC RETINOID", 
                "release_date": "19950126", 
                "experimental_method": [
                    "X-ray diffraction"
                ], 
                "experimental_method_class": [
                    "x-ray"
                ], 
                "revision_date": "20090224", 
                "entry_authors": [
                    "Kleywegt, G.J.", 
                    "Bergfors, T.", 
                    "Jones, T.A."
                ], 
                "deposition_site": null, 
                "number_of_entities": {
                    "polypeptide": 1, 
                    "dna": 0, 
                    "ligand": 1, 
                    "dna/rna": 0, 
                    "rna": 0, 
                    "sugar": 0, 
                    "water": 1, 
                    "other": 0
                }, 
                "processing_site": null, 
                "deposition_date": "19940928", 
                "assemblies": [
                    {
                        "assembly_id": "1", 
                        "form": "homo", 
                        "preferred": true, 
                        "name": "monomer"
                    }
                ]
            }
        ], 
        "2pah": [
            {
                "related_structures": [], 
                "split_entry": [], 
                "title": "TETRAMERIC HUMAN PHENYLALANINE HYDROXYLASE", 
                "release_date": "19991006", 
                "experimental_method": [
                    "X-ray diffraction"
                ], 
                "experimental_method_class": [
                    "x-ray"
                ], 
                "revision_date": "20110713", 
                "entry_authors": [
                    "Stevens, R.C.", 
                    "Fusetti, F.", 
                    "Erlandsen, H."
                ], 
                "deposition_site": "BNL", 
                "number_of_entities": {
                    "polypeptide": 1, 
                    "dna": 0, 
                    "ligand": 1, 
                    "dna/rna": 0, 
                    "rna": 0, 
                    "sugar": 0, 
                    "water": 0, 
                    "other": 0
                }, 
                "processing_site": "RCSB", 
                "deposition_date": "19980526", 
                "assemblies": [
                    {
                        "assembly_id": "1", 
                        "form": "homo", 
                        "preferred": true, 
                        "name": "tetramer"
                    }
                ]
            }
        ]
    }


Looking for more?
'''''''''''''''''

For a full set of examples and more details on all functionality see
these `notes`_.

Dependencies
~~~~~~~~~~~~

|Python: versions|

See the necessary `requirements`_ for this module.

Contributing and Bug tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Feel free to fork, clone, share and distribute. If you find any bugs or
issues please log them in the `issue tracker`_.

License
~~~~~~~

GNU General Public License v3 (GPLv3). See `license`_ for details.

.. _notes: Examples.ipynb
.. _PDBe REST API: http://www.ebi.ac.uk/pdbe/api/doc/
.. _pyEnsemblRest: https://github.com/pyOpenSci/pyEnsemblRest
.. _requirements: requirements.txt
.. _issue tracker: https://github.com/biomadeira/pyPDBeREST/issues
.. _license: LICENSE.md

.. |Build Status| image:: https://secure.travis-ci.org/biomadeira/pyPDBeREST.png?branch=master
   :target: http://travis-ci.org/biomadeira/pyPDBeREST
.. |Coverage Status| image:: https://coveralls.io/repos/biomadeira/pyPDBeREST/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/biomadeira/pyPDBeREST?branch=master
.. |License| image:: http://img.shields.io/badge/license-GPLv3-brightgreen.svg?style=flat
   :target: https://github.com/biomadeira/pyPDBeREST/blob/master/LICENSE.md
.. |Twitter: @biomadeira| image:: https://img.shields.io/badge/contact-@biomadeira-blue.svg?style=flat
   :target: https://twitter.com/biomadeira
.. |Python: versions| image:: https://img.shields.io/badge/python-2.7,_3.3,_3.4,_3.5,_pypy,_pypy3-blue.svg?style=flat
   :target: http://travis-ci.org/biomadeira/pyPDBeREST
   
