# %%
import db
import oracledb
import requests

# %%
host = 'patch-db.siu.edu'
service = 'PCH'
port = 1541
user = 'APPS'
pw = 'Oct09patch'
# or use an environmental variable...
# pw = os.getenv('oracle_pw')
# %%
def user_import():
    engine = db.connect_oracle(host_name=host, service_name = service, username= user, password=pw, port=port)

    xml_out = None

    with engine.connect() as connection:
        # Get the raw cx_Oracle connection from the SQLAlchemy engine
        raw_connection = connection.connection

        cursor = raw_connection.cursor()
        # Calling the PL/SQL procedure with an OUT CLOB parameter
        p_out = cursor.var(oracledb.CLOB)  # Declare the OUT parameter as CLOB
            
        # Execute the stored procedure
        cursor.callproc("APPS.SIUPO_JAGGAER_EBS_INTEGRTN_PKG.RUN_USER_XML", [p_out])

        # Retrieve the CLOB data
        xml_data = p_out.getvalue()
        print (xml_data)

        headers = {'Content-Type': 'application/xml'}
        response = requests.post('https://usertest-messages.sciquest.com/apps/Router/OrgUserImport',data=xml_out, headers=headers)
        print(response)

        # Check if the request was successful
        if response.status_code == 200:
            print("Response from the web service:", str(response.status_code))
        else:
            #Call Error procedure to log error info
            print("Error in POST request:", str(response.status_code), response.text)


def main():
    user_import()

if __name__ == "__main__":
    main()