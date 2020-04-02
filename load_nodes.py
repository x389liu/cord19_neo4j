import argparse
import pandas as pd
from neo4j import GraphDatabase


def add_gene(tx, gene_name, gene_id, gene_symbol):
    tx.run("MERGE (gene:Gene {symbol: $gene_symbol, name: $gene_name, id: $gene_id})",
           gene_symbol=gene_symbol, gene_name=gene_name, gene_id=gene_id)


def add_chem(tx, chem_name, chem_id):
    tx.run("MERGE (chem:Chemical {name: $chem_name, id: $chem_id})",
           chem_name=chem_name, chem_id=chem_id)


def add_disease(tx, disease_name, disease_id):
    tx.run("MERGE (disease:Disease {name: $disease_name, id: $disease_id})",
           disease_name=disease_name, disease_id=disease_id)


def main():
    parser = argparse.ArgumentParser(description='Program for importing nodes into neo4j.')
    parser.add_argument('--gene', default='', type=str, help='import Gene Nodes')
    parser.add_argument('--gene-allrows', action='store_true', default=False, help='import all Gene Nodes')
    parser.add_argument('--gene-nrows', default=1000, type=int, help='number of Gene Nodes to import')
    parser.add_argument('--chem', default='', type=str, help='import Chemical Nodes')
    parser.add_argument('--chem-allrows', action='store_true', default=False, help='import all Chemical Nodes')
    parser.add_argument('--chem-nrows', default=1000, type=int, help='number of Chemical Nodes to import')
    parser.add_argument('--disease', default='', type=str, help='import Disease Nodes')
    parser.add_argument('--disease-allrows', action='store_true', default=False, help='import all Disease Nodes')
    parser.add_argument('--disease-nrows', default=1000, type=int, help='number of Disease Nodes to import')
    args = parser.parse_args()

    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        if args.gene:
            if args.gene_allrows:
                gene_df = pd.read_csv(args.gene, dtype=str, sep='\t')
            else:
                gene_df = pd.read_csv(args.gene, dtype=str, sep='\t', nrows=args.gene_nrows)
            for index, row in gene_df.iterrows():
                session.write_transaction(add_gene, row['GeneName'], row['GeneID'], row['GeneSymbol'])
        if args.chem:
            if args.chem_allrows:
                chem_df = pd.read_csv(args.chem, dtype=str, sep='\t')
            else:
                chem_df = pd.read_csv(args.chem, dtype=str, sep='\t', nrows=args.chem_nrows)
            for index, row in chem_df.iterrows():
                session.write_transaction(add_chem, row['ChemicalName'], row['ChemicalID'])
        if args.disease:
            if args.disease_allrows:
                disease_df = pd.read_csv(args.disease, dtype=str, sep='\t')
            else:
                disease_df = pd.read_csv(args.disease, dtype=str, sep='\t', nrows=args.disease_nrows)
            for index, row in disease_df.iterrows():
                session.write_transaction(add_disease, row['DiseaseName'], row['DiseaseID'])
    driver.close()


main()
