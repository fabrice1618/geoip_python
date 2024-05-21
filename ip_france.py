from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from modeles import IPFrance
from adresses import ip_to_int

def ip_france(ip_address):
    """
    Fonction optimisée pour déterminer si une adresse IP est en France en utilisant une table de plages d'IP françaises.

    Paramètres:
        ip_address (str): L'adresse IP à vérifier.

    Retourne:
        bool: True si l'adresse IP est dans une plage d'IP française, False sinon.
    """

    ip_int = ip_to_int(ip_address)

    # Créer une session et ouvrir une transaction
    session = Session()
    with session.begin_nested():
        # Utiliser une requête SQL optimisée avec un filtre indexé
        query = session.query(func.count()).filter(IPFrance.ip_from <= ip_int, IPFrance.ip_to >= ip_int)

        # Vérifier le nombre de résultats (un seul si l'adresse IP est dans une plage française)
        count = query.scalar()
        session.close()
        return (count == 1)
    

if __name__ == "__main__":
    engine = create_engine('sqlite:///geoip.db')
    Session = sessionmaker(bind=engine)

    ip_address = "8.8.8.8"  
    is_france = ip_france(ip_address)
    print(f"L'adresse IP {ip_address} est-elle en France ? : {is_france}")
