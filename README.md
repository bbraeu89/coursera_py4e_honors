# coursera_py4e_honors
Python Code for the Honors Class of the Coursera Python For Everybody Specialization

The file entitled "retrieve_query_uniprot_json_and_create_SQLite.py" asks for a user input query term: this is a protein name as you would enter it in the searchbar of the Uniprot protein database (https://www.uniprot.org). The program then proceeds to create a SQLite database and will enter the following information for each entry:

  1. ID
  2. Uniprot code
  3. Organism name
  4. Organism lineage
  5. Protein amino acid sequence
  6. Protein amino acid sequeence length
  7. Average protein length for the lineage of the entry (allowing easy comparison between an entry's length and the     lineage average length)

The file entitled "plotting_length.py" generates a simple histogram of the database data. Here, the amino acid length is plotted and colored by lineage.

To illustrate this, I have chosen to plot the data using the query "March6". It quickly visualizes that Fungi lineage has the largest members of this protein class, with plants (Viridiplantae) and animals (Metazoa) having successively shorter proteins of this class. 
