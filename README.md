# cord19_neo4j

`cord19_neo4j` provides tools to load COVID-19 related scientific relationships to the Graph database `neo4j`.

The original dataset is COVID-19 Open Research Dataset ([CORD-19](https://pages.semanticscholar.org/coronavirus-research)),
and its entities and relations have been extracted by [BLENDER Lab](http://blender.cs.illinois.edu/covid19/).
We load the extracted information to `neo4j` to build knowledge graph.

## Setup

Clone cord19_neo4j:

```
git clone https://github.com/x389liu/cord19_neo4j
```

Download extracted entities and relationships [here](http://blender.cs.illinois.edu/covid19/).

Rename column names for `chemicals_diseases_relation.csv`:

```
sed -i.bak $'1s/.*/ChemicalID\tDiseaseName\tDiseaseID\tpmids/' chemicals_diseases_relation.csv
```

(TODO: contact dataset contributor to update column names)

### neo4j

Start a neo4j instance via Docker with the command:

```
docker run -d --name neo4j --publish=7474:7474 --publish=7687:7687 \
    --volume=`pwd`/neo4j:/data \
    -e NEO4J_dbms_memory_pagecache_size=2G \
    -e NEO4J_dbms_memory_heap_initial__size=1G \
    -e NEO4J_dbms_memory_heap_max__size=4G \
    neo4j
```

neo4j should should be available shortly at http://localhost:7474/ with the default username/password of neo4j/neo4j. 
You will be prompted to change the password, this is the password you will pass to load program.

## Running

### Load Nodes

```
# import top 1000 Gene Nodes
python load_nodes.py --gene /path/to/genes.csv --gene-nrows 1000 --password [neo4j_password]

# import all Gene Nodes
python load_nodes.py  --gene /path/to/genes.csv --gene-allrows --password [neo4j_password]

# import top 1000 Chemical Nodes
python load_nodes.py --chem /path/to/genes.csv --chem-nrows 1000 --password [neo4j_password]

# import all Chemical Nodes
python load_nodes.py  --chem /path/to/chemicals.csv --chem-allrows --password [neo4j_password]

# import top 1000 Disease Nodes
python load_nodes.py --disease /path/to/diseases.csv --disease-nrows 1000 --password [neo4j_password]

# import all Disease Nodes
python load_nodes.py  --disease /path/to/diseases.csv --disease-allrows --password [neo4j_password]

```

By default, the program imports top 1000 nodes, and the neo4j password is `password`.

Open http://localhost:7474/ to view the loaded nodes in neo4j.

### Load Relationships

```
# import top 1000 Gene–Disease Associations
python load_relationships.py --gene-disease /path/to/genes_diseases_relation.csv --gene-disease-nrows 1000 --password [neo4j_password]

# import all Gene–Disease Associations
python load_relationships.py --gene-disease /path/to/genes_diseases_relation.csv --gene-disease-allrows --password [neo4j_password]

# import top 1000 Chemical–Disease Associations
python load_relationships.py --chem-disease /path/to/chemicals_diseases_relation.csv --chem-disease-nrows 1000 --password [neo4j_password]

# import all Chemical–Disease Associations
python load_relationships.py --chem-disease /path/to/chemicals_diseases_relation.csv --chem-disease-allrows --password [neo4j_password]

# import top 1000 Gene–Chemical–Interaction Relationships
python load_relationships.py --chem_gene /path/to/chem_gene_ixns_relation.csv --chem_gene-nrows 1000 --password [neo4j_password]

# import all Gene–Chemical–Interaction Relationships
python load_relationships.py --chem_gene /path/to/chem_gene_ixns_relation.csv --chem_gene-allrows --password [neo4j_password]
```

By default, the program imports top 1000 relationships, and the neo4j password is `password`.

Open http://localhost:7474/ to view the loaded relationships in neo4j.

## Neo4j Queries

The following queries can be run against the knowledge graph in neo4j to discover sub-graphs of interest.

```
# Gene–Disease Associations
MATCH ((g:Gene) -- (d:Disease))
RETURN g, d
LIMIT 25

# Chemical–Disease Associations
MATCH ((c:Chemical) -- (d:Disease))
RETURN c, d
LIMIT 25

# Gene–Chemical–Interaction Relationships
MATCH ((g:Gene) -- (c:Chemical))
RETURN g, c
LIMIT 25

# Delete all nodes and relationships
MATCH (n) DETACH DELETE n
```

