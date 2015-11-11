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

from . import __version__

# set urls
default_url = 'http://www.ebi.ac.uk/pdbe/api/'

# api lookup tables
# PDB endpoint
pdb_endpoints = {
    'getSummary': {
        'doc': 'This call provides a summary of properties of a PDB entry, '
               'such as the title of the entry, list of depositors, date of '
               'deposition, date of release, date of latest revision, experimental '
               'method, list of related entries in case split entries, etc.\n'
               'pdbid: string',
        'url': 'pdb/entry/summary/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getMolecules': {
        'doc': 'This call provides the details of molecules (or entities in mmcif-speak) '
               'modelled in the entry, such as entity id, description, type, polymer-type '
               '(if applicable), number of copies in the entry, sample preparation method, '
               'source organism(s) (if applicable), etc.\n'
               'pdbid: string',
        'url': 'pdb/entry/molecules/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getPublications': {
        'doc': 'This call provides details of publications associated with an entry, such '
               'as title of the article, journal name, year of publication, volume, pages, '
               'doi, pubmed_id, etc. Primary citation is listed first.\n'
               'pdbid: string',
        'url': 'pdb/entry/publications/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getRelatedPublications': {
        'doc': 'This call provides details about publication obtained from EuroPMC. '
               'These are articles which cite the primary citation of the entry, or '
               'open-access articles which mention the entry id without explicitly citing '
               'the primary citation of an entry.\n'
               'pdbid: string',
        'url': 'pdb/entry/related_publications/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getExperiments': {
        'doc': 'This call provides details of experiment(s) carried out in determining the '
               'structure of the entry. Each experiment is described in a separate dictionary. '
               'For X-ray diffraction, the description consists of resolution, spacegroup, cell '
               'dimensions, R and Rfree, refinement program, etc. For NMR, details of spectrometer, '
               'sample, spectra, refinement, etc. are included. For EM, details of specimen, imaging, '
               'acquisition, reconstruction, fitting etc. are included.\n'
               'pdbid: string',
        'url': 'pdb/entry/experiment/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getNmrResources': {
        'doc': 'This call provides URLs of available additional resources for NMR entries. E.g., '
               'mapping between structure (PDB) and chemical shift (BMRB) entries.\n'
               'pdbid: string',
        'url': 'pdb/entry/nmr_resources/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getLigands': {
        'doc': 'This call provides a a list of modelled instances of ligands, i.e. "bound" '
               'molecules that are not waters.\n'
               'pdbid: string',
        'url': 'pdb/entry/ligand_monomers/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getModifiedResidues': {
        'doc': 'This call provides a list of modelled instances of modified amino acids or '
               'nucleotides in protein, DNA or RNA chains.\n'
               'pdbid: string',
        'url': 'pdb/entry/modified_AA_or_NA/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getMutatedResidues': {
        'doc': 'This call provides a list of modelled instances of mutated amino acids or '
               'nucleotides in protein, DNA or RNA chains. (Note that at present it does '
               'not provide information about mutated nucleotides.)\n'
               'pdbid: string',
        'url': 'pdb/entry/mutated_AA_or_NA/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getReleaseStatus': {
        'doc': 'This call provides status of a PDB entry (released, obsoleted, on-hold etc) '
               'along with some other information such as authors, title, experimental '
               'method, etc.\n'
               'pdbid: string',
        'url': 'pdb/entry/status/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getObservedRanges': {
        'doc': 'This call provides observed ranges, i.e. segments of structural coverage, '
               'of polymeric molecules that are modelled fully or partly.\n'
               'pdbid: string',
        'url': 'pdb/entry/polymer_coverage/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getSecondaryStructure': {
        'doc': 'This call provides details about residue ranges of regular secondary structure '
               '(alpha helices and beta strands) found in protein chains of the entry. For '
               'strands, sheet id can be used to identify a beta sheet.\n'
               'pdbid: string',
        'url': 'pdb/entry/secondary_structure/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getResidueListing': {
        'doc': 'This call lists all residues (modelled or otherwise) in the entry, except waters, '
               'along with details of the fraction of expected atoms modelled for the residue and '
               'any alternate conformers.\n'
               'pdbid: string',
        'url': 'pdb/entry/residue_listing/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getResidueListingChain': {
        'doc': 'This call lists all residues (modelled or otherwise) in the entry, except waters, '
               'along with details of the fraction of expected atoms modelled for the residue and '
               'any alternate conformers.\n'
               'pdbid: string',
        'url': 'pdb/entry/residue_listing/{{pdbid}}/chain/{{chainid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getBindingSites': {
        'doc': 'This call provides details on binding sites in the entry as per STRUCT_SITE records '
               'in PDB files (or mmcif equivalent thereof), such as ligand, residues in the site, '
               'description of the site, etc.\n'
               'pdbid: string',
        'url': 'pdb/entry/binding_sites/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getVariousUrls': {
        'doc': 'This call provides URLs and brief descriptions (labels) for PDB and mmcif files, '
               'biological assembly files, FASTA file for sequences, SIFTS cross reference XML '
               'files, validation XML files, X-ray structure factor file, NMR experimental '
               'constraints files, etc. Please note that these files are also available on https.\n'
               'pdbid: string',
        'url': 'pdb/entry/files/{{pdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
}

# Compounds Endpoint
compounds_endpoints = {
    'getSummary': {
        'doc': 'This call provides a summary of salient properties of a chemical groups defined '
               'in the PDB Chemical Component Dictionary, such as formula, formula weight, '
               'smiles (canonical, OpenEye), inchi, inchi-key, name, systematic names, '
               'Chembl id, creation date, revision date, etc.\n'
               'compid: string',
        'url': 'pdb/compound/summary/{{compid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getAtoms': {
        'doc': 'This set of calls provides information about atoms in a chemical groups defined '
               'in the PDB Chemical Component Dictionary. For each atoms, properties such as '
               'name, element symbol, ideal coordinates, stereochemistry, aromaticity (when '
               'applicable), etc. are available.\n'
               'compid: string',
        'url': 'pdb/compound/atoms/{{compid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getBounds': {
        'doc': 'This set of calls provides information about bonds in a chemical groups defined '
               'in the PDB Chemical Component Dictionary. For each bond, properties such as atom '
               'names, bond type, stereochemistry and aromaticity (when applicable) etc. '
               'are available.\n'
               'compid: string',
        'url': 'pdb/compound/bonds/{{compid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
    'getInPdbs': {
        'doc': 'This set of calls returns a list of PDB entries that contain the compound defined '
               'in the PDB Chemical Component Dictionary.\n'
               'compid: string',
        'url': 'pdb/compound/in_pdb/{{compid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
}

# EMDB Endpoint
emdb_endpoints = {
    'getInfo': {
        'doc': 'Following property-groups are available to query: '
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
               '    related_by_publication: returns list of entries that share the same publication\n'
               'property: string (from list); emdbid: string',
        'url': 'emdb/entry/:property_group/{{property}}/{{emdbid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
}

# SIFTS Endpoint
sifts_endpoints = {
    'getMappings': {
        'doc': 'Mappings (as assigned by the SIFTS process) from PDB structures to UniProt, Pfam, '
               'InterPro, CATH, SCOP, IntEnz and GO accessions (and vice versa).'
               'PDB id-code OR UniProt accession code OR Pfam accession code OR Interpro accession '
               'code OR CATH cathcode OR SCOP sunid OR IntEnz EC code OR GO accession\n'
               'id: string',
        'url': 'mappings/{{id}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbUniprot': {
        'doc': 'Mappings (as assigned by the SIFTS process) from PDB structures to UniProt.\n'
               'pdbid: string',
        'url': 'mappings/uniprot/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbInterpro': {
        'doc': 'Mappings (as assigned by the SIFTS process) from PDB structures to Interpro.\n'
               'pdbid: string',
        'url': 'mappings/interpro/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbPfam': {
        'doc': 'Mappings (as assigned by the SIFTS process) from PDB structures to Pfam.\n'
               'pdbid: string',
        'url': 'mappings/pfam/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbCath': {
        'doc': 'Mappings (as assigned by the SIFTS process) from PDB structures to CATH.\n'
               'pdbid: string',
        'url': 'mappings/cath/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbScop': {
        'doc': 'Mappings (as assigned by the SIFTS process) from PDB structures to SCOP.\n'
               'pdbid: string',
        'url': 'mappings/scop/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbGo': {
        'doc': 'Mappings (as assigned by the SIFTS process) from PDB structures to GO.\n'
               'pdbid: string',
        'url': 'mappings/go/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbEc': {
        'doc': 'Mappings (as assigned by the SIFTS process) from PDB structures to EC.\n'
               'pdbid: string',
        'url': 'mappings/ec/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getSequenceDomains': {
        'doc': 'Mappings from protein chains to both Pfam and InterPro as assigned by the '
               'SIFTS process.\n'
               'pdbid: string',
        'url': 'mappings/sequence_domains/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getStructuralDomains': {
        'doc': 'Mappings from protein chains to both SCOP and CATH as assigned by the '
               'SIFTS process.\n'
               'pdbid: string',
        'url': 'mappings/structural_domains/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getHomologene': {
        'doc': 'Homologene polypeptides for a given PDB entity id.\n'
               'pdbid: string; entity: string',
        'url': 'mappings/homologene/{{pdbid}}/{{entity}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getBestStructures': {
        'doc': 'The list of PDB structures mapping to a UniProt accession sorted by '
               'coverage of the protein and, if the same, resolution.\n'
               'uniprotid: string',
        'url': 'mappings/best_structures/{uniprotid}}',
        'method': ['GET', 'POST'],
        'content_type': 'application/json'
    },
}
# PISA Endpoint
pisa_endpoints = {
    'getVersion': {
        'doc': 'Returns PISA API command line program version number.',
        'url': 'pisa/version',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getNumberEntries': {
        'doc': 'Returns number of entries in the database.',
        'url': 'pisa/counts',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getPdbsList': {
        'doc': 'Returns a list of PDB codes in the PISA database.',
        'url': 'pisa/pdblist',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAsisList': {
        'doc': 'Returns a list of "asis" assembly identifiers. This complex represents by the '
               'coordinate section only of the PDB entry.\n'
               'pdbid: string',
        'url': 'pisa/asislist/{{pdbid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getNumberInterfaces': {
        'doc': 'Returns a list of "asis" assembly identifiers. This complex represents by the '
               'coordinate section only of the PDB entry.'
               'Assembly id code. This is 0 for the standard mmCIF files and '
               '1,2,3,4...XAU, PAU etc for the assembly mmCIF files.\n'
               'pdbid: string; assemblyid: string',
        'url': 'pisa/noofinterfaces/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAsisDetails': {
        'doc': 'Returns details of the requested "asis" assembly. This complex represents by the '
               'coordinate section only of the PDB entry.'
               'Assembly id code. This is 0 for the standard mmCIF files and '
               '1,2,3,4...XAU, PAU etc for the assembly mmCIF files.\n'
               'pdbid: string; assemblyid: string',
        'url': 'pisa/asis/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAsisInfo': {
        'doc': 'Returns "asis" assembly energetics summary. This complex represents by the coordinate '
               'section only of the PDB entry.'
               'String	Assembly id code. This is 0 for the standard mmCIF files and '
               '1,2,3,4...XAU, PAU etc for the assembly mmCIF files.\n'
               'pdbid: string; assemblyid: string',
        'url': 'pisa/asissummary/{{pdbid}}/{{assemblyid}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAsisInfoByComponent': {
        'doc': 'Returns "asis" assembly component, "energetics", "interfaces" or "monomers". Please '
               'refer to the PISA web page for the content of each component.'
               'String	Assembly id code. This is 0 for the standard mmCIF files and '
               '1,2,3,4...XAU, PAU etc for the assembly mmCIF files.\n'
               'pdbid: string; assemblyid: string; component: string (from list)',
        'url': 'pisa/asiscomponent/{{pdbid}}/{{assemblyid}}/{{component}}',
        'method': ['GET'],
        'content_type': 'application/json'
    },
    'getAssemblyDetails': {
        'doc': 'Returns details of the requested PISA assembly.'
               'Assembly id code. This is 0 for the standard mmCIF files and '
               '1,2,3,4...XAU, PAU etc for the assembly mmCIF files. '
               'Assembly PQS set, zero based. Index of assembly, zero based.\n'
               'pdbid: string; assemblyid: string; set: number; index: number',
        'url': 'pisa/assembly/:pdbid/:assemblyid/:set/:index',
        'method': ['GET'],
        'content_type': 'application/json'
    },
}
#
#
# monomer detail
# http://www.ebi.ac.uk/pdbe/api/pisa/monomerdetail/:pdbid/:assemblyid/:index
# Returns details of the requested PISA monomer.
# pdbid
# 3gcb
# String	PDB entry id code.
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.
# index
# 1
# Number	index of monomer, one based.
# Quotes	 RunCall	 Select	 Expand	 Collapse	 2+	 3+
#
# monomer component
# http://www.ebi.ac.uk/pdbe/api/pisa/monomercomponent/:pdbid/:assemblyid/:index/:component
# Returns components of the requested PISA monomer. Please refer to the PISA web page for the content of each component.
# pdbid
# 3gcb
# String	PDB entry id code.
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.
# component		FromList	component.
# index
# 1
# Number	index of monomer, one based.
# Quotes	 RunCall	 Select	 Expand	 Collapse	 2+	 3+
#
# assembly detail
# http://www.ebi.ac.uk/pdbe/api/pisa/assemblydetail/:pdbid/:assemblyid/:index
# Returns details of the requested PISA assembly.
# pdbid
# 3gcb
# String	PDB entry id code
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.
# index
# 0
# Number	index of assembly, zero based.
# Quotes	 RunCall	 Select	 Expand	 Collapse	 2+	 3+
#
# assembly component
# http://www.ebi.ac.uk/pdbe/api/pisa/assemblycomponent/:pdbid/:assemblyid/:index/:component
# Returns details of one component of the requested PISA assembly. Please refer to the PISA web page for the content of each component.
# pdbid
# 3gcb
# String	PDB entry id code
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.
# component		FromList	component.
# index
# 0
# Number	index of assembly, zero based.
# Quotes	 RunCall	 Select	 Expand	 Collapse	 2+	 3+
#
# interface detail
# http://www.ebi.ac.uk/pdbe/api/pisa/interfacedetail/:pdbid/:assemblyid/:index
# Returns details of the requested interface.
# pdbid
# 3gcb
# String	PDB entry id code
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.
# index
# 1
# Number	index of interface, one based.
# Quotes	 RunCall	 Select	 Expand	 Collapse	 2+	 3+
#
# interface component
# http://www.ebi.ac.uk/pdbe/api/pisa/interfacecomponent/:pdbid/:assemblyid/:index/:component
# Returns details of the requested interface component. Please refer to the PISA web page for the content of each component.
# pdbid
# 3gcb
# String	PDB entry id code
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.
# component		FromList	index of interface, one based.
# index
# 1
# Number	index of interface, one based.
# Quotes	 RunCall	 Select	 Expand	 Collapse	 2+	 3+
#
# analysis
# http://www.ebi.ac.uk/pdbe/api/pisa/analysis/:pdbid/:assemblyid
# Returns an anysis of the entry.
# pdbid
# 3gcb
# String	PDB entry id code
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.
# Quotes	 RunCall	 Select	 Expand	 Collapse	 2+	 3+
#
# list of monomers
# http://www.ebi.ac.uk/pdbe/api/pisa/monomerlist/:pdbid/:assemblyid
# Returns a list of monomers.
# pdbid
# 3gcb
# String	PDB entry id code
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.
# Quotes	 RunCall	 Select	 Expand	 Collapse	 2+	 3+
#
# list of PISA assemblies
# http://www.ebi.ac.uk/pdbe/api/pisa/assemblylist/:pdbid/:assemblyid
# Returns a list of assemblies.
# pdbid
# 3gcb
# String	PDB entry id code
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.
# Quotes	 RunCall	 Select	 Expand	 Collapse	 2+	 3+
#
# List of interfaces.
# http://www.ebi.ac.uk/pdbe/api/pisa/interface/:pdbid/:assemblyid
# Returns a list of interfaces with a summary of each interface.
# pdbid
# 3gcb
# String	PDB entry id code
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.
# Quotes	 RunCall	 Select	 Expand	 Collapse	 2+	 3+
#
# Interface details
# http://www.ebi.ac.uk/pdbe/api/pisa/interface/:pdbid/:assemblyid
# Returns details of the interface for given pdbid and assembly id.
# pdbid
# 3gcb
# String	PDB entry id code
# assemblyid
# 0
# String	Assembly id code. This is 0 for the standard mmCIF files and 1,2,3,4...XAU, PAU etc for the assembly mmCIF files.


# entire REST API
api_endpoints = {
    'PDB': pdb_endpoints,
    'COMPOUNDS': compounds_endpoints,
    'EMDB': emdb_endpoints,
    'SIFTS': sifts_endpoints,
    'PISA': pisa_endpoints,
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

# set user agent
ensembl_user_agent = {'User-Agent': 'pyPDBeREST v' + __version__}
ensembl_content_type = {'Content-Type': 'application/json'}
