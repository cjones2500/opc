import couchdb
import getpass
import copy

 
address = "http://localhost:8080" #network address of the database
#This address has been ssh tunnelled from port 5984 to port 8080.
#This is only a temporary measure due the SNO+ VPN at SNOLAB
#CouchDb operates from port 5984 
dbname = "resistor"    #name of the couchdb database
username = "snotdaq"   #username for access to the couchdb database
new_field = "run_range"  #new field to add update
new_value = [0,-1]       #new value to add in the new field   

# Retrieve database from couch
couch = couchdb.Server(address)
couch.resource.credentials = (username, getpass.getpass("Password: "))
database = couch[dbname]

# retrieve all docs (assumes they all need the update)
rows = database.view("_all_docs", include_docs=True)
# it you want docs of a type that are emitted by a view:
# rows = database.view("_design/ddocname/_view/viewname", include_docs=True)

docs = [] # for a bulk update at the end

for row in rows:
    # Might want to filter on e.g. id to ensure no design docs are included
    if row.id.startswith("_design"):
        print "skip", row.id
        continue
    doc = copy.copy(row.doc)
    doc[new_field] = new_value
    docs.append(row.doc)
    database[doc.id] = doc    

print "Done!"
