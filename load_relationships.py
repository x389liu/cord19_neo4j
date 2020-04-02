import argparse
import pandas as pd
from neo4j import GraphDatabase


def add_gene_disease(tx, gene_id, disease_id, pmids):
    tx.run("MATCH (gene:Gene {id: $gene_id}) "
           "MATCH (disease:Disease {id: $disease_id}) "
           "MERGE (gene)-[:RELATE {pmids: $pmids}]->(disease)",
           gene_id=gene_id, disease_id=disease_id, pmids=pmids.split('|'))


def add_chem_disease(tx, chem_id, disease_id):
    tx.run("MATCH (chem:Chemical {id: $chem_id}) "
           "MATCH (disease:Disease {id: $disease_id}) "
           "MERGE (chem)-[:RELATE]->(disease)",
           chem_id=chem_id, disease_id=disease_id)


def add_chem_gene(tx, chem_id, gene_id, pmids, organism, organism_id, interaction, interaction_actions):
    tx.run("MATCH (chem:Chemical {id: $chem_id}) "
           "MATCH (gene:Gene {id: $gene_id}) "
           "MERGE (chem)-[:RELATE {pmids: $pmids, organism: $organism, organism_id: $organism_id, \
           interaction: $interaction, interaction_actions: $interaction_actions}]->(gene)",
           chem_id=chem_id, gene_id=gene_id, pmids=pmids, organism=organism,
           organism_id=organism_id, interaction=interaction, interaction_actions=interaction_actions.split('|'))


def main():
    parser = argparse.ArgumentParser(description='Program for importing relationships into neo4j.')
    parser.add_argument('--gene-disease', default='', type=str, help='import Gene–Disease Associations')
    parser.add_argument('--gene-disease-nrows', default=1000, type=int,
                        help='number of Gene–Disease Associations to import')
    parser.add_argument('--chem-disease', default='', type=str, help='import Chemical–Disease Associations')
    parser.add_argument('--chem-disease-nrows', default=1000, type=int,
                        help='number of Chemical–Disease Associations to import')
    parser.add_argument('--chem-gene', default='', type=str, help='import Gene–Chemical–Interaction Relationships')
    parser.add_argument('--chem-gene-nrows', default=1000, type=int,
                        help='number of Gene–Chemical–Interaction Relationships to import')
    args = parser.parse_args()

    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        if args.gene_disease:
            gene_disease_df = pd.read_csv(args.gene_disease, dtype=str, sep='\t', nrows=args.gene_disease_nrows)
            for index, row in gene_disease_df.iterrows():
                session.write_transaction(add_gene_disease, row['GeneID'], row['DiseaseID'], row['pmids'])
        if args.chem_disease:
            chem_disease_df = pd.read_csv(args.chem_disease, dtype=str, sep='\t', nrows=args.chem_disease_nrows)
            for index, row in chem_disease_df.iterrows():
                session.write_transaction(add_chem_disease, row['ChemicalID'], row['DiseaseID'])
        if args.chem_gene:
            chem_gene_df = pd.read_csv(args.chem_gene, dtype=str, sep='\t', nrows=args.chem_gene_nrows)
            for index, row in chem_gene_df.iterrows():
                session.write_transaction(add_chem_gene, row['ChemicalID'], row['GeneID'], row['pmids'],
                                          row['Organism'], row['OrganismID'], row['Interaction'],
                                          row['InteractionActions'])
    driver.close()


main()
