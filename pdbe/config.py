#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    pyPDBeREST: A wrapper for the PDBe REST API.
    Copyright (C) 2015  Fábio Madeira

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# from . import __version__
# set user agent
# user_agent = {'User-Agent': 'pyPDBeREST v' + __version__}
user_agent = {'User-Agent': 'pyPDBeREST'}
content_type = {'Content-Type': 'application/json'}

# set urls
default_url = 'https://www.ebi.ac.uk/pdbe/'

# api lookup tables
var_types = {
    # pdb
    'pdbid': {
        'type': str,
        'doc': '4-character PDB id code. (e.g. 1cbs).\n'
               'For POST requests, data should contain one or more comma-separated ids.'
    },
    'chainid': {
        'type': str,
        'doc': 'PDB chain id. (e.g. A)'
    },
    # compounds
    'compid': {
        'type': str,
        'doc': 'Chemical component identifier, up to 3 characters long. (e.g. ATP)'
    },
    # emdb
    'property': {
        'type': str,
        'doc': 'One of the property groups from list. ',
        'list': ['all', 'summary', 'citations', 'publications', 'map', 'supplement',
                 'sample', 'vitrification', 'imaging', 'fitted', 'image_acquisition',
                 'processing', 'analysis', 'experiment', 'related_by_publication'],
    },
    'emdbid': {
        'type': str,
        'doc': 'EMDB entry identifier, starting with EMD- and followed by 4 digits '
               '(e.g. EMD-1200)'
    },
    # sifts
    'accession': {
        'type': str,
        'doc': 'PDB id-code OR UniProt accession code OR Pfam accession code OR '
               'Interpro accession code OR CATH cathcode OR SCOP sunid OR '
               'IntEnz EC code OR GO accession. (e.g. 1cbs, P29373)'
    },
    'entity': {
        'type': str,
        'doc': 'The entity id for the PDB id code. (e.g. 1)'
    },
    'uniprotid': {
        'type': str,
        'doc': 'UniProt accession. (e.g. P29373)'
    },
    # pisa
    'assemblyid': {
        'type': str,
        'doc': 'Assembly id code. This is 0 for the standard mmCIF files and '
               '1,2,3,4...XAU, PAU etc for the assembly mmCIF files. (e.g. 0)'
    },
    'set': {
        'type': int,
        'doc': 'Assembly PQS set, zero based.',
    },
    'assembly_index': {
        'type': int,
        'doc': 'Index of assembly, zero based.',
    },
    'assembly_component': {
        'type': str,
        'doc': 'Component from list.',
        'list': ['energetics', 'interfaces', 'monomers'],
    },
    'monomer_index': {
        'type': int,
        'doc': 'Index of monomer, one based.',
    },
    'monomer_component': {
        'type': str,
        'doc': 'Component from list.',
        'list': ['energetics', 'buriedsurfacearea', 'deltag'],
    },
    'interface_index': {
        'type': int,
        'doc': 'Index of interface, one based.',
    },
    'interface_component': {
        'type': str,
        'doc': 'Component from list.',
        'list': ['energetics', 'hbounds', 'disulphidebonds', 'disulfidebonds',
                 'covalentbonds', 'saltbridges', 'interfacingresidues'],
    },
    # ssm
    'ssm_index': {
        'type': int,
        'doc': 'Index of SSM match.',
    },
    # validation

    # search
    'query': {
        'type': str,
        'doc': 'Options string allowed by Solr syntax. Details about constructing '
               'Solr queries can be found from webpages such as this'
               'http://wiki.apache.org/solr/CommonQueryParameters.',
    },
}

# PDB endpoint
pdb_endpoints = {
    'getSummary': {
        'doc': 'Summary.\n'
               'This call provides a summary of properties of a PDB entry, '
               'such as the title of the entry, list of depositors, date of '
               'deposition, date of release, date of latest revision, experimental '
               'method, list of related entries in case split entries, etc.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/summary/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getMolecules': {
        'doc': 'Molecules in the entry (alias /entry/entities).\n'
               'This call provides the details of molecules (or entities in mmcif-speak) '
               'modelled in the entry, such as entity id, description, type, polymer-type '
               '(if applicable), number of copies in the entry, sample preparation method, '
               'source organism(s) (if applicable), etc.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/molecules/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getPublications': {
        'doc': 'Publications associated with the entry (alias /entry/citations).\n'
               'This call provides details of publications associated with an entry, such '
               'as title of the article, journal name, year of publication, volume, pages, '
               'doi, pubmed_id, etc. Primary citation is listed first.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/publications/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getRelatedPublications': {
        'doc': 'Related publications.\n'
               'This call provides details about publication obtained from EuroPMC. '
               'These are articles which cite the primary citation of the entry, or '
               'open-access articles which mention the entry id without explicitly citing '
               'the primary citation of an entry.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/related_publications/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getExperiments': {
        'doc': 'Experiment(s).\n'
               'This call provides details of experiment(s) carried out in determining the '
               'structure of the entry. Each experiment is described in a separate dictionary. '
               'For X-ray diffraction, the description consists of resolution, spacegroup, cell '
               'dimensions, R and Rfree, refinement program, etc. For NMR, details of spectrometer, '
               'sample, spectra, refinement, etc. are included. For EM, details of specimen, imaging, '
               'acquisition, reconstruction, fitting etc. are included.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/experiment/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getNmrResources': {
        'doc': 'NMR Resources(s).\n'
               'This call provides URLs of available additional resources for NMR entries. E.g., '
               'mapping between structure (PDB) and chemical shift (BMRB) entries.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/nmr_resources/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getLigands': {
        'doc': 'Ligands.\n'
               'This call provides a a list of modelled instances of ligands, i.e. "bound" '
               'molecules that are not waters.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/ligand_monomers/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getModifiedResidues': {
        'doc': 'Modified residues.\n'
               'This call provides a list of modelled instances of modified amino acids or '
               'nucleotides in protein, DNA or RNA chains.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/modified_AA_or_NA/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getMutatedResidues': {
        'doc': 'Mutated residues.\n'
               'This call provides a list of modelled instances of mutated amino acids or '
               'nucleotides in protein, DNA or RNA chains. (Note that at present it does '
               'not provide information about mutated nucleotides.)',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/mutated_AA_or_NA/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getReleaseStatus': {
        'doc': 'Release status.\n'
               'This call provides status of a PDB entry (released, obsoleted, on-hold etc) '
               'along with some other information such as authors, title, experimental '
               'method, etc.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/status/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getObservedRanges': {
        'doc': 'Observed ranges.\n'
               'This call provides observed ranges, i.e. segments of structural coverage, '
               'of polymeric molecules that are modelled fully or partly.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/polymer_coverage/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getSecondaryStructure': {
        'doc': 'Secondary structure.\n'
               'This call provides details about residue ranges of regular secondary structure '
               '(alpha helices and beta strands) found in protein chains of the entry. For '
               'strands, sheet id can be used to identify a beta sheet.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/secondary_structure/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getResidueListing': {
        'doc': 'List of residues with modelling information.\n'
               'This call lists all residues (modelled or otherwise) in the entry, except waters, '
               'along with details of the fraction of expected atoms modelled for the residue and '
               'any alternate conformers.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/residue_listing/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getResidueListingChain': {
        'doc': 'List of residues with modelling information for a particular PDB chain.\n'
               'This call lists all residues (modelled or otherwise) in the entry, except waters, '
               'along with details of the fraction of expected atoms modelled for the residue and '
               'any alternate conformers.',
        'var': {'pdbid': var_types['pdbid'],
                'chainid': var_types['chainid']},
        'url': 'api/pdb/entry/residue_listing/{{pdbid}}/chain/{{chainid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getBindingSites': {
        'doc': 'Binding sites.\n'
               'This call provides details on binding sites in the entry as per STRUCT_SITE records '
               'in PDB files (or mmcif equivalent thereof), such as ligand, residues in the site, '
               'description of the site, etc.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/binding_sites/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getVariousUrls': {
        'doc': 'URLs of various files associated with a PDB entry.\n'
               'This call provides URLs and brief descriptions (labels) for PDB and mmcif files, '
               'biological assembly files, FASTA file for sequences, SIFTS cross reference XML '
               'files, validation XML files, X-ray structure factor file, NMR experimental '
               'constraints files, etc. Please note that these files are also available on https.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pdb/entry/files/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
}

# Compounds Endpoint
compounds_endpoints = {
    'getSummary': {
        'doc': 'Summary.\n'
               'This call provides a summary of salient properties of a chemical groups defined '
               'in the PDB Chemical Component Dictionary, such as formula, formula weight, '
               'smiles (canonical, OpenEye), inchi, inchi-key, name, systematic names, '
               'Chembl id, creation date, revision date, etc.',
        'var': {'compid': var_types['compid']},
        'url': 'api/pdb/compound/summary/{{compid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getAtoms': {
        'doc': 'Atoms.\n'
               'This set of calls provides information about atoms in a chemical groups defined '
               'in the PDB Chemical Component Dictionary. For each atoms, properties such as '
               'name, element symbol, ideal coordinates, stereochemistry, aromaticity (when '
               'applicable), etc. are available.',
        'var': {'compid': var_types['compid']},
        'url': 'api/pdb/compound/atoms/{{compid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getBounds': {
        'doc': 'Bounds.\n'
               'This set of calls provides information about bonds in a chemical groups defined '
               'in the PDB Chemical Component Dictionary. For each bond, properties such as atom '
               'names, bond type, stereochemistry and aromaticity (when applicable) etc. '
               'are available.',
        'var': {'compid': var_types['compid']},
        'url': 'api/pdb/compound/bonds/{{compid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getInPdbs': {
        'doc': 'PDB entries containing the compound.\n'
               'This set of calls returns a list of PDB entries that contain the compound defined '
               'in the PDB Chemical Component Dictionary.',
        'var': {'compid': var_types['compid']},
        'url': 'api/pdb/compound/in_pdb/{{compid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
}

# EMDB Endpoint
emdb_endpoints = {
    'getInfo': {
        'doc': 'EMDB entry properties.\n'
               'Following property-groups are available to query:\n'
               '    all: all information (except "analysis" and "related_by_publication") about '
               'the entry\n'
               '    summary: entry summary information\n'
               '    citations: entry publication information\n'
               '    publications: entry publication information\n'
               '    map: entry map information\n'
               '    supplement: information about additional files deposited with the entry\n'
               '    sample: entry sample information\n'
               '    vitrification: specimen vitrification information\n'
               '    imaging: entry imaging information\n'
               '    fitted: information about PDB models fitted into the EM structure\n'
               '    image_acquisition: imaging acquisition information\n'
               '    processing: image processing and reconstruction information\n'
               '    analysis: advance numerical analysis about the structure\n'
               '    experiment: bundle of "vitrification", "imaging", "fitted", "image_acquisition", '
               'and "processing" calls\n'
               '    related_by_publication: returns list of entries that share the same publication',
        'var': {'property': var_types['property'],
                'emdbid': var_types['emdbid']
                },
        'url': 'api/emdb/entry/{{property}}/{{emdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
}

# SIFTS Endpoint
sifts_endpoints = {
    'getMappings': {
        'doc': 'SIFTS Mappings.\n'
               'Mappings (as assigned by the SIFTS process) from PDB structures to UniProt, Pfam, '
               'InterPro, CATH, SCOP, IntEnz and GO accessions (and vice versa).'
               'PDB id-code OR UniProt accession code OR Pfam accession code OR Interpro accession '
               'code OR CATH cathcode OR SCOP sunid OR IntEnz EC code OR GO accession',
        'var': {'accession': var_types['accession']},
        'url': 'api/mappings/{{accession}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbUniprot': {
        'doc': 'SIFTS Mappings (PDB -> UniProt).\n'
               'Mappings (as assigned by the SIFTS process) from PDB structures to UniProt.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/mappings/uniprot/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbInterpro': {
        'doc': 'SIFTS Mappings (PDB -> InterPro).\n'
               'Mappings (as assigned by the SIFTS process) from PDB structures to Interpro.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/mappings/interpro/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbPfam': {
        'doc': 'SIFTS Mappings (PDB -> Pfam).\n'
               'Mappings (as assigned by the SIFTS process) from PDB structures to Pfam.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/mappings/pfam/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbCath': {
        'doc': 'SIFTS Mappings (PDB -> CATH).\n'
               'Mappings (as assigned by the SIFTS process) from PDB structures to CATH.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/mappings/cath/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbScop': {
        'doc': 'SIFTS Mappings (PDB -> SCOP).\n'
               'Mappings (as assigned by the SIFTS process) from PDB structures to SCOP.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/mappings/scop/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbGo': {
        'doc': 'SIFTS Mappings (PDB -> GO).\n'
               'Mappings (as assigned by the SIFTS process) from PDB structures to GO.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/mappings/go/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbEc': {
        'doc': 'SIFTS Mappings (PDB -> EC).\n'
               'Mappings (as assigned by the SIFTS process) from PDB structures to EC.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/mappings/ec/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getSequenceDomains': {
        'doc': 'Mappings to sequence domain resources (i.e. Pfam and InterPro).\n'
               'Mappings from protein chains to both Pfam and InterPro as assigned by the '
               'SIFTS process.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/mappings/sequence_domains/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getStructuralDomains': {
        'doc': 'Mappings to structural domain resources (i.e. SCOP and CATH).\n'
               'Mappings from protein chains to both SCOP and CATH as assigned by the '
               'SIFTS process.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/mappings/structural_domains/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getHomologene': {
        'doc': 'Homologene.\n'
               'Homologene polypeptides for a given PDB entity id.',
        'var': {'pdbid': var_types['pdbid'],
                'entity': var_types['entity']
                },
        'url': 'api/mappings/homologene/{{pdbid}}/{{entity}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getBestStructures': {
        'doc': 'Best Structures.\n'
               'The list of PDB structures mapping to a UniProt accession sorted by '
               'coverage of the protein and, if the same, resolution.',
        'var': {'uniprotid': var_types['uniprotid']},
        'url': 'api/mappings/best_structures/{{uniprotid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
}
# PISA Endpoint
pisa_endpoints = {
    # general
    'getVersion': {
        'doc': 'PISA API version.\n'
               'Returns PISA API command line program version number.',
        'var': {},
        'url': 'api/pisa/version',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getNumberEntries': {
        'doc': 'PISA API counts of number of entries.\n'
               'Returns number of entries in the database.',
        'var': {},
        'url': 'api/pisa/counts',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbsList': {
        'doc': 'PISA API pdblist.\n'
               'Returns a list of PDB codes in the PISA database.',
        'var': {},
        'url': 'api/pisa/pdblist',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    # asis - assembly ids
    'getAsisList': {
        'doc': 'List of asis assembly ids for a given PDB code.\n'
               'Returns a list of "asis" assembly identifiers. '
               'This complex represents by the coordinate section only of the PDB entry.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/pisa/asislist/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAsisDetails': {
        'doc': 'Asis details.\n'
               'Returns details of the requested "asis" assembly. '
               'This complex represents by the coordinate section only of the PDB entry.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid']
                },
        'url': 'api/pisa/asis/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAsisSummary': {
        'doc': 'Summary information for asis assembly.\n'
               'Returns "asis" assembly energetics summary. '
               'This complex represents by the coordinate section only of the PDB entry.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid']
                },
        'url': 'api/pisa/asissummary/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAsisComponent': {
        'doc': 'Information on asis assembly divided by component.\n'
               'Returns "asis" assembly component, "energetics", "interfaces" or "monomers". '
               'Please refer to the PISA web page for the content of each component.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid'],
                'assembly_component': var_types['assembly_component']
                },
        'url': 'api/pisa/asiscomponent/{{pdbid}}/{{assemblyid}}/{{assembly_component}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    # assemblies
    'getAssembly': {
        'doc': 'Details of a given assembly.\n'
               'Returns details of the requested PISA assembly.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid'],
                'set': var_types['set'],
                'assembly_index': var_types['assembly_index'],
                },
        'url': 'api/pisa/assembly/{{pdbid}}/{{assemblyid}}/{{set}}/{{assembly_index}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAnalysis': {
        'doc': 'Analysis.\n'
               'Returns an analysis of the entry.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid']
                },
        'url': 'api/pisa/analysis/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAssembliesList': {
        'doc': 'List of assemblies.\n'
               'Returns a list of assemblies.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid']
                },
        'url': 'api/pisa/assemblylist/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAssemblyDetails': {
        'doc': 'Assembly details.\n'
               'Returns details of the requested PISA assembly.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid'],
                'assembly_index': var_types['assembly_index']
                },
        'url': 'api/pisa/assemblydetail/{{pdbid}}/{{assemblyid}}/{{assembly_index}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAssemblyComponent': {
        'doc': 'Assembly component.\n'
               'Returns details of one component of the requested PISA assembly. '
               'Please refer to the PISA web page for the content of each component.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid'],
                'assembly_index': var_types['assembly_index'],
                'assembly_component': var_types['assembly_component']
                },
        'url': 'api/pisa/assemblycomponent/{{pdbid}}/{{assemblyid}}/{{assembly_index}}/{{assembly_component}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },

    # monomers
    'getMonomersList': {
        'doc': 'List of monomers.\n'
               'Returns a list of monomers.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid']
                },
        'url': 'api/pisa/monomerlist/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getMonomerDetails': {
        'doc': 'Monomer details.\n'
               'Returns details of the requested PISA monomer.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid'],
                'monomer_index': var_types['monomer_index']
                },
        'url': 'api/pisa/monomerdetail/{{pdbid}}/{{assemblyid}}/{{monomer_index}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getMonomerComponent': {
        'doc': 'Monomer component.\n'
               'Returns components of the requested PISA monomer. '
               'Please refer to the PISA web page for the content of each component.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid'],
                'monomer_index': var_types['monomer_index'],
                'monomer_component': var_types['monomer_component']
                },
        'url': 'api/pisa/monomercomponent/{{pdbid}}/{{assemblyid}}/{{monomer_index}}/{{monomer_component}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    # interfaces
    'getInterfaces': {
        'doc': 'Interfaces.\n'
               'Returns details of the interface for given pdbid and assembly id.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid']
                },
        'url': 'api/pisa/interface/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getNumberInterfaces': {
        'doc': 'The number of interfaces calculated by PISA.\n'
               'Returns number of interfaces for a given pdbid/assemblyid.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid']
                },
        'url': 'api/pisa/noofinterfaces/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getInterfacesList': {
        'doc': 'List of interfaces.\n'
               'Returns a list of interfaces with a summary of each interface.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid']
                },
        'url': 'api/pisa/interfacelist/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getInterfaceDetails': {
        'doc': 'Interface details.\n'
               'Returns details of the requested interface.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid'],
                'interface_index': var_types['interface_index']
                },
        'url': 'api/pisa/interfacedetail/{{pdbid}}/{{assemblyid}}/{{interface_index}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getInterfaceComponent': {
        'doc': 'Interface component.\n'
               'Returns details of the requested interface.',
        'var': {'pdbid': var_types['pdbid'],
                'assemblyid': var_types['assemblyid'],
                'interface_index': var_types['interface_index'],
                'interface_component': var_types['interface_component']
                },
        'url': 'api/pisa/interfacecomponent/{{pdbid}}/{{assemblyid}}/{{interface_index}}/{{interface_component}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
}

# SSM Endpoint
ssm_endpoints = {
    'getVersion': {
        'doc': 'Fold API version.\n'
               'Returns Fold API command line program version number.',
        'var': {},
        'url': 'api/ssm/version',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getMatchStandard': {
        'doc': 'Fold API matchstandard.\n'
               'Returns details of match using standard parameters.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/ssm/matchstandard/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getNumberMatches': {
        'doc': 'Fold API noofmatches.\n'
               'Returns number of matches.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/ssm/noofmatches/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getMatchSummary': {
        'doc': 'Fold API matchsummary.\n'
               'Returns summary of matches.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/ssm/matchsummary/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getMatchDetail': {
        'doc': 'Fold API matchdetail.\n'
               'Returns details of match.',
        'var': {'pdbid': var_types['pdbid'],
                'ssm_index': var_types['ssm_index']
                },
        'url': 'api/ssm/matchdetail/{{pdbid}}/{{ssm_index}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
}

# Validation Endpoint
validation_endpoints = {
    'getGlobalRelativePercentiles': {
        'doc': 'Global and relative percentiles of entry-wide validation metrics.\n'
               'Metrics here are the ones recommended by validation task force. '
               'Global is against whole PDB archive and relative is against entries of '
               'comparable resolution.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/global-percentiles/entry/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getGlobalAbsolutePercentilesSummary': {
        'doc': 'Summary of global absolute percentiles.\n'
               'These scores are harmonic means of absolute percentiles of geometric '
               'metrics (e.g. ramachandran, clashscore, sidechains), reflections-based '
               'metrics (Rfree, RSRZ) and both these kinds of metrics taken together. '
               'Wherever a constitutent percentile is 0, the harmonic mean is defined to '
               'be 0. When constituent percentiles are all unavailable, the harmonic mean '
               'is null.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/summary_quality_scores/entry/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getGlobalPercentilesDetails': {
        'doc': 'A little more detail than global percentiles.\n'
               'This is still a very high level summary, but covers metrics of interest not '
               'included in percentiles, or a little more detail than just percentile.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/key_validation_stats/entry/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getDiffractionRefinementDescriptors': {
        'doc': 'Descriptors of diffraction data and refinement - a bit like table-1.\n'
               '',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/xray_refine_data_stats/entry/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getRamachandranSidechainOutliers': {
        'doc': 'Ramachandran and sidechain outliers in protein chains.\n'
               'This call returns backbone and sidechain outliers in protien chains, as '
               'calculated by Molprobity as part of wwPDB validation pipeline.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/protein-ramachandran-sidechain-outliers/entry/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getBackboneSidechainQuality': {
        'doc': 'Backbone and sidechain quality of all protein residues.\n'
               'This call returns Ramachandran status (favoured, outlier, etc.), '
               'phi-psi values, sidechain status (rotamer name or outlier) as reported '
               'by Molprobity component of the wwPDB validation pipeline.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/rama_sidechain_listing/entry/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getSuitePuckerRnaOutliers': {
        'doc': 'Suite and pucker outliers in RNA chains.\n'
               'This call returns RNA backbone outliers, i.e. non-rotameric suites and unusual '
               'puckers, as calculated by Molprobity as part of wwPDB validation pipeline.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/RNA_pucker_suite_outliers/entry/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getOutlierTypesResidues': {
        'doc': 'A list of outlier types found in residues.\n'
               'A residue can have many types of geometric or experimental-data-based outliers. '
               'This call lists all kinds of outliers found in a residue. For residues with no '
               'recorded outlier, there is no information returned.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/residuewise_outlier_summary/entry/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getGeometryOutliers': {
        'doc': 'Residues with geometric outliers in protein, DNA, RNA chains.\n'
               'Lists residues in protein, DNA, RNA chains that contain various types '
               'of geometry outliers.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/protein-RNA-DNA-geometry-outlier-residues/entry/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getVanDerWaalOverlaps': {
        'doc': 'A list of van der Waal overlaps in unit-id notation.\n'
               'Lists pairs of atoms (in unit-id convention) that have van der Waal '
               'clash according to MolProbity.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/vdw_clashes/entry/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getAllOutliersUnitId': {
        'doc': 'All outliers in unit-id notation.\n'
               'Lists outliers of all types using the unit-id notation to describe atoms '
               'or residues involved.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/validation/outliers/all/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
}

# Topology Endpoint
topology_endpoints = {
    'getTopology': {
        'doc': '2D secondary structure layout for protein chains in the entry.\n'
               'Returns coordinates for drawing secondary structure diagrams using one of '
               'the PDBsum packages maintained by Roman Laskowski.',
        'var': {'pdbid': var_types['pdbid']},
        'url': 'api/topology/entry/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getTopologyPerChain': {
        'doc': '2D secondary structure layout for a particular protein chain in the entry.\n'
               'Returns coordinates for drawing secondary structure diagrams using one of '
               'the PDBsum packages maintained by Roman Laskowski.',
        'var': {'pdbid': var_types['pdbid'],
                'chainid': var_types['chainid']
                },
        'url': 'api/topology/entry/{{pdbid}}/chain/{{chainid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
}

# Search Endpoint
search_endpoints = {
    'getSearch': {
        'doc': 'Search on Solr instance based on polymeric entities in the PDB.\n'
               'A document in this Solr instance represents a polymeric entity of type '
               'protein, DNA, RNA or sugar. Output from the call depends on the query sent '
               'to Solr. Query parameters are well documented in Solr documentation.\n'
               'Check http://www.ebi.ac.uk/pdbe/api/doc/search.html for more information',
        'var': {'query': var_types['query']},
        'url': 'search/pdb/select?{{query}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
}

# entire REST API
api_endpoints = {
    'PDB': pdb_endpoints,
    'COMPOUNDS': compounds_endpoints,
    'EMDB': emdb_endpoints,
    'SIFTS': sifts_endpoints,
    'PISA': pisa_endpoints,
    'SSM': ssm_endpoints,
    'VALIDATION': validation_endpoints,
    'TOPOLOGY': topology_endpoints,
    'SEARCH': search_endpoints,
}

# http status codes
http_status_codes = {
    200: ('OK', 'Request was a success. Only process data from the service when you receive this code'),
    400: ('Bad Request',
          'Occurs during exceptional circumstances such as the service is unable to find an ID.'
          'Check if the response Content-type was JSON. If so the JSON object is an exception hash '
          'with the message keyed under error'),
    404: ('Not Found', 'Indicates a badly formatted request. Check your URL'),
    415: ('Unsupported Media Type',
          'The server is refusing to service the request because the entity of the request is in a '
          'format not supported by the requested resource for the requested method'),
    429: ('Too Many Requests',
          'You have been rate-limited; wait and retry. The headers X-RateLimit-Reset, X-RateLimit-Limit '
          'and X-RateLimit-Remaining will inform you of how long you have until your limit is reset and'
          ' what that limit was. If you get this response and have not exceeded your limit then check if '
          'you have made too many requests per second.'),
    500: ('Internal Server Error',
          'This error is not documented. Maybe there is an error in user input or REST server could have '
          'problems. Try to do the query with curl. If your data input and query are correct, contact the '
          'pdbe team'),
    503: ('Service Unavailable', 'The service is temporarily down; retry after a pause'),
}
