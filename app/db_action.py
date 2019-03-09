#define a function that gets the last saved state of the database 
def getLastSavedDbState():
    from cloudant.client import Cloudant
    from cloudant.result import Result
    from cloudant.adapters import Replay429Adapter
    from credentials import getUserName,getPassword,getUrl

    #Establish a connection to the cloudant database by providing the credentials necessary
    client = Cloudant(getUserName(), getPassword(), url=getUrl(),adapter=Replay429Adapter(retries=10, initialBackoff=0.01))
    client.connect()

    #Connect to the "news_articles" database remotely
    db = client.get("news_articles",remote=True)
    #Get all records from the database
    resultset = Result(db.all_docs,include_docs=True)

    news_articles_list = list()
    #Loop through the database records
    for result in resultset:
        #Add all article titles to a list.
        #The news article titles are unique and will be used to check if an article already exists in the database
        news_articles_list.append(result["doc"]["article_title"])
    client.disconnect()

    return news_articles_list

#Define a function that adds a new article to the database
def dbLoadNewArticle(article):
    from cloudant.client import Cloudant
    from cloudant.adapters import Replay429Adapter
    from credentials import getUserName,getPassword,getUrl

    client = Cloudant(getUserName(), getPassword(), url=getUrl(),adapter=Replay429Adapter(retries=10, initialBackoff=0.01))
    client.connect()

    db = client.get("news_articles",remote=True)
    #Create the database record
    new_doc = db.create_document(article)
    #Verify that the record was successfully added
    if new_doc.exists():
        print("Article was successfully added")

    client.disconnect()