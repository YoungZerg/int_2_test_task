import psycopg2
import config
import logging
from config import error_counter_global


logging.basicConfig(level=logging.INFO, filename='scanner.log', filemode='a',
                                format="""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%(asctime)s [%(levelname)s]\n%(message)s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n""")


def write_to_bd(ip_addr: str, os_type: str, kernel: str, architecture: str) -> None:
       try:
           logging.info(f"Connecting to database")
           connection = psycopg2.connect(
               host=config.db_host,
               user=config.db_user,
               password=config.db_pass,
               database=config.db_name
           )
           connection.autocommit = True
           #with connection.cursor() as cursor:
           #    cursor.execute(
           #        """CREATE TABLE hostsdata(
           #            id serial PRIMARY KEY,
           #            ip_addr VARCHAR(30) NOT NULL,
           #            os_type VARCHAR(60) NOT NULL,
           #            kernel VARCHAR(60) NOT NULL,
           #            architecture VARCHAR(60) NOT NULL);"""
           #    )
           
           with connection.cursor() as cursor:
               cursor.execute(
                   """INSERT INTO hostsdata (ip_addr, os_type, kernel, architecture)
                      VALUES (%s, %s, %s, %s)
                   """, (ip_addr, os_type, kernel, architecture))
               logging.info("Data was successfully stored")
       except Exception as ex:
           global error_counter_global
           error_counter_global = 2
           logging.error(f"Error occured while connecting to database: {ex}")
       finally:
           if connection:
               connection.close()
               logging.info("Connection to database was closed")