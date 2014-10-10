import couchdb
import getpass
import copy

#his address has been ssh tunnelled 
address = "http://localhost:8080"
dbname = "pmt"
username = "snotdaq"
new_field = "type"
#new_value = -1

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
    print row
    # Might want to filter on e.g. id to ensure no design docs are included
    if row.id.startswith("_design"):
        print "skip", row.id
        continue
    doc = copy.copy(row.doc)
    #print doc

    #change the field name but keep its value
    #Get the current value of  
    current_value = doc[new_field]
    #print current_value
    doc['pmt_type'] = current_value
    doc['type'] = 'pmt'
    #print doc 
    #raw_input("Press enter to continue for current value")
    #docs.append(row.doc)
    #print doc
    database[doc.id] = doc
    #print "recorded version \n\n\n"
    #print database[doc.id]
    #raw_input("Press enter to continue")
    

#database.update(docs)

print "Done!"
