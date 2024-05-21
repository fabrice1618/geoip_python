from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modeles import GeoIP, IPFrance

# (Assume you have already defined the GeoIP model and database connection)
if __name__ == "__main__":
    engine = create_engine('sqlite:///geoip.db')
    Session = sessionmaker(bind=engine)

    # Create a session to interact with the database
    session = Session()

    # Define the query using SQLAlchemy's query builder
    query = session.query(GeoIP.ip_from, GeoIP.ip_to, GeoIP.country_code.label('country_code'))

    # Order the results by ip_from
    query = query.order_by(GeoIP.ip_from)

    is_france = False
    # Fetch all results and print them
    for row in query.all():
        #print(row.country_code, row.ip_from, row.ip_to)
        if row.country_code == "FR":
            if not is_france:
                bloc_start = row.ip_from
                bloc_end = row.ip_to
                is_france = True
            else:
                bloc_end = row.ip_to
        else:
            if is_france:
                print("bloc", bloc_start, bloc_end)
                bloc = IPFrance(ip_from=bloc_start, ip_to=bloc_end)
                session.add(bloc)
                session.commit()

                bloc_start = 0
                bloc_end = 0

            is_france = False

    # Close the session when done
    session.close()
