pyPDBeREST
==========

|Twitter: @biomadeira| |Build Status| |Coverage Status| |License|

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

\`\`\`javascript { “2pah”: [ { “related\_structures”: [],
“split\_entry”: [], “title”: “TETRAMERIC HUMAN PHENYLALANINE
HYDROXYLASE”, “release\_date”: “19991006”, “experimental\_method”: [
“X-ray diffraction” ], “experimental\_method\_class”: [ “x-ray” ],
“revision\_date”: “20110713”, “entry\_authors”: [ “Stevens, R.C.”,
“Fusetti, F.”, “Erlandsen, H.” ], “deposition\_site”: “BNL”,
“number\_of\_entities”: { “polypeptide”: 1, “dna”: 0, “ligand”: 1,
“dna/rna”: 0, “rna”: 0, “sugar”: 0, “water”: 0,

.. _PDBe REST API: http://www.ebi.ac.uk/pdbe/api/doc/
.. _pyEnsemblRest: https://github.com/pyOpenSci/pyEnsemblRest
.. _notes: Examples.ipynb

.. |Twitter: @biomadeira| image:: https://img.shields.io/badge/contact-@biomadeira-blue.svg?style=flat
   :target: https://twitter.com/biomadeira
.. |Build Status| image:: https://secure.travis-ci.org/biomadeira/pyPDBeREST.png?branch=master
   :target: http://travis-ci.org/biomadeira/pyPDBeREST
.. |Coverage Status| image:: https://coveralls.io/repos/biomadeira/pyPDBeREST/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/biomadeira/pyPDBeREST?branch=master
.. |License| image:: http://img.shields.io/badge/license-GPLv3-brightgreen.svg?style=flat
   :target: https://github.com/biomadeira/pyPDBeREST/blob/master/LICENSE.md
