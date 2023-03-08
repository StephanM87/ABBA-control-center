from light_cas_automator.biocathub_adapter.model.biocatalyst import Reactant, Reaction, Enzyme
import requests


def test_model():

    BA = Reactant(role = "substrate", smiles="C1=CC(=CC(=C1)O)C=O", name="3-OH-BA", concentration=15, unit="mmol/L")
    PAC = Reactant(role = "product", smiles="CC(=O)C(C1=CC=CC=C1)O", name="3-OH-PAC", concentration=0, unit="mmol/L")
    PACP = Reactant(role = "substrate", smiles="CC(=O)C(C1=CC=CC=C1)O", name="3-OH-PAC", concentration=0, unit="mmol/L")
    metaraminol = Reactant(role = "product", smiles="CC(C(C1=CC(=CC=C1)O)O)N", name="Metaraminol", concentration=0, unit="mmol/L")

    Reaction1 = Reaction(name="transamination", educts=[BA], products=[PAC])
    Reaction2 = Reaction(name="transamination", educts=[PACP], products=[metaraminol])

    enzyme = Enzyme(name="carboligase", reaction=Reaction1, organism="Cv", concentration=1)
    print(enzyme.dict())

    print(enzyme.dict())
    headers = {'Content-type': 'application/json'} 

    req = requests.post("http://127.0.0.1:5000/retrobiohub/lightCas", data=enzyme.json(), headers=headers)
    print(req)
    