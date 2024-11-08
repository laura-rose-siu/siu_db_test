import oracledb
import requests
oracledb.init_oracle_client(lib_dir="/usr/lib/oracle/19.25/client64/lib")  #Directory on ea-int server
#oracledb.init_oracle_client(lib_dir="C:\instantclient_23_5")

def user_import():
    # Establishing a connection to the Oracle database
    connection = oracledb.connect(
        user='APPS', 
        password='Oct09patch', 
        dsn="patch-db.siu.edu:1541/PCH"  
    )
    
    # Creating a cursor
    cursor = connection.cursor()

    try:
        # Calling the PL/SQL procedure with an OUT CLOB parameter
        p_out = cursor.var(oracledb.CLOB)  # Declare the OUT parameter as CLOB
        
        cursor.callproc("APPS.SIUPO_JAGGAER_EBS_INTEGRTN_PKG.RUN_USER_XML", [p_out])

        # Retrieve the CLOB data
        user_xml = p_out.getvalue()

    finally:
        cursor.close()

    # Define the URL of the web service
    url = "https://usertest-messages.sciquest.com/apps/Router/OrgUserImport"
     
    # Make the POST request
    try:
        response = requests.post(url, data=user_xml)
        #print(response)

        # Check if the request was successful
        if response.status_code == 200:
            print("Response from the web service:", str(response.status_code))
        else:
            #Call Error procedure to log error info
            print("Error in POST request:", str(response.status_code), response.text)
        
    finally:
        connection.close()

def main():
    user_import()

if __name__ == "__main__":
    main()