#Define a function that scraps data from a news site
def getData():
    #Importing the packages
    from bs4 import BeautifulSoup
    import unirest
    #Import read and modify cloudant database functions defined in db_action.py
    from db_action import dbLoadNewArticle,getLastSavedDbState
   
    firstTime = True
    hasBeenUpdated = False
    page_number=1  
    #Modify unirest HTTP request timeout for slow connection purposes
    unirest.timeout(90)
    try:
        #Make HTTP request to phantomjs cloud through the rapidapi platform by providing phantomjs cloud api key, rapidapi key and the target URL
        response = unirest.get("https://phantomjscloud.p.rapidapi.com/single/browser/v1/your-phantomjscloud-api-key/?requestType=text&targetUrl="+"https://mwebantu.news/category/business/",
                headers={
                    "X-RapidAPI-Key": "your-rapidapi-key"
                }
            )
        #Parse the response to HTML using lxml parser.
        #Create Beautifulsoup object to navigate the HTML tags of the parsed response
        soup_obj1 = BeautifulSoup(response.body,"lxml")
        #Create loop to scrap data on the first page and second page respectively
        while(page_number<=2):
            #Get the div tag holding all the news articles
            news_articles_container = soup_obj1.find('div',{'class':'td-ss-main-content'})
            #Get a list of all the news articles in the main content div tag
            news_articles_list = news_articles_container.find_all('div',{'class':'td_module_10 td_module_wrap td-animation-stack'})
            #Loop through the articles list 
            for news_article in news_articles_list:
                #Verify if the database has been modified to get it's most recent state after modification
                if firstTime or hasBeenUpdated:    
                    news_articles = getLastSavedDbState()
                    firstTime = False
                    hasBeenUpdated = False
                
                #Instantiate an empty python dictionary
                article=dict()

                #Get article data by navigating to the tags holding the data
                #Affect retrieved data to the python dictionary object 
                article["article_title"] = news_article.find('div',{'class':'item-details'}).find('a').getText().upper()
                article["article_date"] = news_article.find('time').get('datetime')
                article["article_image_url"] = news_article.find('div',{'class':'td-module-thumb'}).find('img').get('src')
                article["article_full_story_url"] = news_article.find('div',{'class':'item-details'}).find('a').get('href')
                article["article_summarised"] = news_article.find('div',{'class':'td-excerpt'}).getText()
                
                #Verify if the current article already exists in the database.
                #If it does'nt exist add it to the database
                if article["article_title"] not in news_articles:
                    dbLoadNewArticle(article)
                    hasBeenUpdated = True
            #Increment value of page_number by one to get data of the second page on the next loop            
            page_number+=1

            #Make HTTP request to get the second page containing news articles
            response = unirest.get("https://phantomjscloud.p.rapidapi.com/single/browser/v1/your-phantomjscloud-api-key/?requestType=text&targetUrl="+"https://mwebantu.news/category/business/page/"+str(page_number)+"/",
                headers={
                    "X-RapidAPI-Key": "your-rapidapi-key"
                }
            ) 
            #Parse the response  
            soup_obj1 = BeautifulSoup(response.body,"lxml")
        return True
    except:
        return False
getData()