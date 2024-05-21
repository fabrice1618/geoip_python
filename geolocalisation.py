from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modeles import GeoIP
from adresses import ip_to_int

def geolocalisation_ip(ip_address):
    """
    Fonction qui utilise la table geoip pour retourner les informations de localisation d'une adresse IP dans une chaîne de caractères.

    Paramètres:
        ip_address (str): L'adresse IP pour laquelle on souhaite obtenir les informations de localisation.

    Retourne:
        dict: Un dictionnaire contenant les informations de localisation de l'adresse IP, ou None
    """

    # Convert the IP address to an integer for efficient lookup
    ip_int = ip_to_int(ip_address)

    # Query the geoip table to find the matching IP range
    session = Session()
    geoip_entry = session.query(GeoIP).filter(GeoIP.ip_from <= ip_int, GeoIP.ip_to >= ip_int).first()
    session.close()

    if geoip_entry:
        # Extract information
        loc = dict()
        loc['country_code'] = geoip_entry.country_code
        loc['country_name'] = geoip_entry.country_name
        loc['region_name'] = geoip_entry.region_name
        loc['city_name'] = geoip_entry.city_name
        loc['latitude'] = geoip_entry.latitude
        loc['longitude'] = geoip_entry.longitude
        return loc
    else:
        return None  # IP address not found in the table
    

if __name__ == "__main__":
    engine = create_engine('sqlite:///geoip.db')
    Session = sessionmaker(bind=engine)

    ip_address = "8.8.8.8"  
    localisation_info = geolocalisation_ip(ip_address)
    print(f"Informations de localisation pour l'adresse IP {ip_address}:")
    print(localisation_info)
