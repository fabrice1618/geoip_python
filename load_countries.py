from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modeles import GeoIP, Country

# (Assume you have already defined the GeoIP model and database connection)
if __name__ == "__main__":
    engine = create_engine('sqlite:///geoip.db')
    Session = sessionmaker(bind=engine)

    # Create a session to interact with the database
    session = Session()

    # Define the query using SQLAlchemy's query builder
    query = session.query(GeoIP.country_code, GeoIP.country_name).group_by(GeoIP.country_code)

    # Execute the query and fetch results
    for country_code, country_name in query.all():
        pays_existant = session.query(Country).filter(Country.country_code == country_code).first()
        if pays_existant is None:
            pays = Country(country_code=country_code, country_name=country_name)
            session.add(pays)
            print(f"Add: country Code: {country_code}, country Name: {country_name}")

    # Close the session when done
    session.commit()
    session.close()
