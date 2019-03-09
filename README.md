# A CLOUD BASED WEB SCRAPER

## Index
  
  - [Introduction](#introduction) 
  - [Platforms and services](#platforms-and-services)
  - [Build flow](#build-flow)
  - [Build a web scraper in python](#1--build-a-web-scraper-in-python)
  
    - [Setting up the environment](#setting-up-the-environment)
    - [Installing the packages](#installing-the-packages)
    - [Setting up cloud phantomjs](#setting-up-cloud-phantomjs)
    - [Setting up Rapid API](#setting-up-rapid-api)
    - [Writing the code](#writing-the-code)
    - [Setting up cloudant](#setting-up-cloudant)
    
  - [Containerise the python web scraper using Docker](#2--containerise-the-python-web-scraper-using-docker)
  - [Upload Docker container of the web scraper to Docker Hub](#3--upload-docker-container-of-the-web-scraper-to-docker-hub)
  - [Deploy the container to IBM cloud](#4--deploy-the-container-to-ibm-cloud)
  - [Create time controlled triggers on the IBM cloud functions service](#5--create-time-controlled-triggers-on-the-ibm-cloud-functions-service)
  
  
## Introduction

This article will help you build a web scraper and upload it to work autonomously on the cloud. Before we deploy a web scraper to the cloud it’s important to understand what web scraping is. Web scraping as per Wikipedia, is the process extracting data from websites. Why would one need to extract data from a website? Should I be interested? What’s the point? Well the answer to these questions depends on the use case. One would scrape a website for analytical purposes or just for personal use, seeing that this information is available publicly. You can read more about web scraping from the Wikipedia article here https://en.wikipedia.org/wiki/Web_scraping, it’ll give you sufficient information to satisfy your curiosity. 

They're several web scraping techniques that exist and that can be done in several programming languages, you’re free to choose your preferred tool to get the work done. In this article we’ll be working with the python programming language. No need to worry, the syntax is fairly simple and easy to understand and of course I’ll be explaining every step so you don’t get confused. If you already understand basic python programming syntax, this will be a breeze. Hang in there and let’s get it done.
So what will our web scraper do? Our web scraper is going to be assigned the task of extracting news articles from a news site. Because the main reason one would want an autonomous web scraper is to extract data that is constantly being updated. 

**Disclaimer: before scraping any website be sure to read their user terms and conditions. Some sites may take legal action if you don't follow usage guidelines.**  

## Platforms and services 

This section will list and briefly explain the platforms and services we'll use for our cloud based web scraper example.

- **IBM cloud platform:**  this will be our cloud platform of choice, for the reason being that you can access several services without having to provide credit card information. For our example we'll get to work with :
  - **Cloud functions service:** this service will allow us to execute our web scraper on the cloud. 
  - **Cloudant:** a non-relational, distributed database service. We'll use this to store the data we scrape.
- **Docker container platform:** this platform we'll allow us to containerize our web scraper in a well defined environment with all necessary dependencies. This action allows our web scraper to work on any given platform that supports docker containers. In our example our docker container will be used by the *ibm cloud functions service*.
- **Github:** we'll use Github for version control and also to link to our docker container. Linking our docker container to a github repository containing our web scraper will automatically initiate a new build for our docker container image. The new image will carry all changes made to the repository's content.
- **Cloud phantomjs platform:** this platform will help render the web pages from the HTTP requests we'll make on the cloud. Once a page is rendered the response is returned as HTML.
- **Rapid API platform:** this platform will help manage our API calls to the cloud phantomjs platform and also provide an interface that shows execution statistics. 

## Build flow

It always helps to know the end goal of a project to better understand what features to implement. Below is a list of steps we’ll take to reach our end goal: 

- Build a web scraper In python,
- Containerise the python web scraper using Docker,
- Upload Docker container of the web scraper to Docker Hub,
- Deploy the container to IBM cloud,
- Create time controlled triggers on the IBM cloud functions service

## 1.  Build a web scraper in python

Python proposes several libraries for your web scraping needs, ranging from the **requests library** for making HTTP requests to **selenium** for browser automation and testing. These libraries are very useful if you’re using your machine but for our use case, we want it to work on the cloud independent of our machines and the network latency we are subjected to. You can read about selenium web browser automation here https://www.seleniumhq.org/. 

In our example we’ll be using **cloud phantomjs**, which will be responsible for rendering our website on the cloud and **unirest library** to make an http request to cloud phantomjs. Unirest is an open source library that allows us to make HTTP requests for simple html websites and also JavaScript driven websites. You can further read on Unirest here http://unirest.io/python.html. Once the request is made, a response is returned in the form of html. To be able to navigate through the html tags, we have to properly parse the response. But how? The answer is **Beautiful Soup**, another python library that allows us to parse the html response. Once parsed we can then easily navigate through the html tags programmatically with Beautiful Soup. 

- ### Setting up the environment: 

  We’ll be building our web scraper in the **python 2.7 environment**. To get python 2.7 follow this link https://www.python.org/downloads/release/python-2715/ and choose the installer specific to your OS and system type. Download and install using the installer. 
  
  Once installed your machine is ready to execute python script. My machine? I thought you said we are going to be working on the cloud. No need to panic we’re getting there. Before we can deploy our web scraper to the cloud we first need to run tests on our machine to make sure it’s working error free. 
  
  On a windows OS you need to add python to the **PATH environment variable**. This allows you to execute a python script in command prompt and also any code editor that supports executing python scripts. I recommend **Visual studio code**.

  To add python to the PATH environment variable follow these steps:
  
  - Locate the folder you chose to install python in, open sub-directories if any exist until you see **python.exe**.
  - Copy the path to the directory containing the python.exe file.
  - Open **Control panel** -> **System** -> **Advanced system parameters** -> **Environment variables**
  - Under **user variables**, select **path** and click the **modify button**
  - Click **new** and paste the path you copied earlier
  - Restart your machine
  
  Now that you have added python to the path environment variable you can now execute python scripts in command prompt or in a supported code editor of your choice. 
  To execute a python script in command prompt, you can use the following syntax : 
  ```cmd
  C:\>python <script_name>.py
  ```
  If you had a different version of python already added to the PATH environment variable then you need to specify what version you want to use. In our case we want to execute our script using version 2.7. To do that you can use the following syntax : 
  ```cmd
  C:\>py -2.7 <script_name>.py
  ```

- ### Installing the packages:
  
  The python packages we’ll be using don’t come preinstalled with python, so you’ll need to download and install each one. Python uses **pip** to install packages. Pip is a package management system used to install and manage software packages written in Python. To install packages using pip, open command prompt and type:
   ```cmd
  C:\>pip install <package_name>
  ```
  If you have a different version of python already installed and have it's path in the path environment variable then you have to type:
    ```cmd
  C:\>py -2.7 –m pip install <package_name>
  ```
  
  Here’s a list of the packages we’ll be using:
  
  - **Unirest** : to make an HTTP request to cloud phantomjs
  
  ```cmd
  pip install unirest
  ```
   ```cmd
  py -2.7 –m pip install unirest
  ```
  - **Urllib3**: used implicitly by unirest to handle HTTP requests
  
  ```cmd
  pip install urllib3
  ```
   ```cmd
  py -2.7 –m pip install urllib3
  ```
  - **Bs4**: this is the Beautiful soup 4 package, which we’ll use to navigate through the html tags and parse the response from cloud phantomjs to HTML.
  
   ```cmd
  pip install bs4
  ```
   ```cmd
  py -2.7 –m pip install bs4
  ```
  - **Lxml**: this package is used by Beautiful soup to parse response objects. Html5lib is another package that can be used for parsing but is relatively slower.
  
  ```cmd
  pip install lxml
  ```
   ```cmd
  py -2.7 –m pip install lxml
  ```

- ### Setting up cloud phantomjs:

  In order to use cloud phantomjs you’ll need to sign up for a free account on this link https://phantomjscloud.com/. The free account will allow you to render 500 webpages/day for free and for the example we’ll be working with, 500 pages is more than sufficient. The cloud phantomjs platform offers flexible plans if you’d like to work with more pages.
  
  Once signed up you get access to an API key that you’ll need to attach to an HTTP request URL, in order to make use of your 500 webpage tier. 
  
- ### Setting up Rapid API:

  To be able to view API call statistics you'll need to sign up for a free Rapid API account and follow the following link to get your Rapid API key that we'll later use in the code for our web scraper. Here's the link https://rapidapi.com/novaleaf/api/phantomjs-cloud-web-browser-and-webpage-processing-as-a-service. 
  
- ### Writing the code:

  We’re now all set up to write our web scraper in python. Where to start? Well basically we’ll have to make an HTTP request to the website we want to extract data from and after getting a response, we’ll navigate through the HTML tags to get the data we want. So for our example we’ll be getting **Business news articles** from a news website. Because why not? The news is paginated and each page contains 10 news articles. For our example we’ll only be scraping data off the first two pages to get the most recent Business news.
  
  It’s necessary to understand the structure of the webpage in order to extract data more intelligently. So the first thing to do is **access the desired webpage** in your **browser** of choice, then right click on an element on the page and select **inspect**. This opens up the **development tools tab**, allowing you to see the HTML tags structure. It helps if you understand basic HTML syntax to better understand the anatomy of a website.
  
  The image below shows the layout used by each news article on the site :
  
  ![news_article_layout](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/news_article.PNG)
  
  We'll be adding the data retrieved for each news article to a python dictionary object. The content of each python dictionary object will look like this :
  
    ```json
  {
  
      "article_image_url" : "",
      "article_title" : "",
      "article_date" : "",
      "article_summary" : ""
      
   }
  ```
  
  Now that we have an idea of how the data will be structured let's go ahead and write the code that will allow us to retrieve the data.
  
  **Importing the packages**:
  
  In order to use the python packages we installed earlier, we need to import them. The code snippet below shows how this done : 
  
    ```python
    from bs4 import BeautifulSoup
    import unirest
    ...
  ```
  
  The two other packages we installed namely lxml and urllib3 are not shown above because we'll not be using them explicitly in the code.
  
  **Making the HTTP request**:
  
  It's now time to use all the keys we've collected so far. We're going to compose the HTTP request URL responsible for returning our HTML response. To do that we use the following code snippet :
  
  ```python
    ...
    page_number = 1
    response = unirest.get("https://phantomjscloud.p.rapidapi.com/single/browser/v1/your_cloud_phantomjs_api_key_here/?requestType=text&targetUrl="+"https://mwebantu.news/category/business/page/"+str(page_number)+"/",
                headers={
                    "X-RapidAPI-Key": "your_rapid_api_key_here"
                }
            )
    ...
  ```
  
  Let's break down the above code. So we're using the **unirest** package to make an HTTP request and the response is stored in a variable named response. The HTTP request URL is made up of **five parts**. 
  
  The first being the `https://phantomjscloud.p.rapidapi.com/single/browser/v1/...` which directs our request to **cloud phantomjs** through **Rapid API**. 
  
  The second part `...your_cloud_phantomjs_api_key_here/...` is for the cloud phantomjs API, which allows the request to be processed by the cloud phantomjs platform. 
  
  The third part is the `...requestType=text...`, this specifies the type we're requesting to be returned. If we were making a request to a webpage that returns JSON data, we'd set the the requestType to JSON. 
  
  The fourth part is `...targetUrl="+"https://...`, this section allows us to indicate the URL for the webpage we want to scrape. 
  
  The fifth and last being `...headers={"X-RapidAPI-Key": "your_rapid_api_key_here"}...`, this section allows us to add extra information to the HTTP request URL. In this case we're specifying the Rapid API key as extra information for the request.    
  
  **Parsing the response**:
  
  In order for us to make use of the response we get from the HTTP request we made earlier we must it parse it to HTML. Once parsed we'll be able to programmatically navigate through the HTML tags. 
  
  ```python
    ...
    soup_obj = BeautifulSoup(response.body,'lxml')
    ...
  ```
  
  Now we're able to naviagte through the HTML tags to get the data we want from the webpage. Beautiful soup allows us to navigate to a specific HTML tag or to get a list of HTML tags that have the same attribute being searched e.g a CSS class. To get an HTML tag and affect it to a variable, we can type `div_tag = soup_obj.find('div')` which returns the first occurence of the **div tag** in the HTML structure. But this is'nt too useful if the first div tag contains data that we have no interest in. 
  
  The best solution is providing extra details like the tag's CSS class or ID, this will then pin down a specific tag that responds to the attribute we're searching for. To do this you can type the following `div_tag = soup_obj.find('div',{'class':'td-ss-main-content')`, this gives us the div tag holding the main content of the web page. 
  
  If our selected tag contains other tags, we can use the variable containing the tag to further navigate to another specific tag. Let's take an example of a div tag containing several other div tags having the same attribute. To do that we type `div_tags_list = soup_obj.find_all('div',{'class':'td_module_16 td_module_wrap td-animation-stack')`, notice that in this example we use **find_all** to get a list of all the tags that correspond to the searched property. Furthermore, we can access individual attributes or get the text that's in between the tag. To get an attribute we can type `div_tag_class = div_tag.get('class')` and to get the text in between the tag we can type `div_tag_text = div_tag.getText()`.
  
  After getting the data from a webpage, we normally have to save it somewhere. In the next section we're going to see how we can set up database service on the cloud. This service will allow us to store the data we scrape on the cloud. 
  
- ### Setting up cloudant: 

  Cloudant is a non-relational database service offered by the IBM cloud platform. In order to use this service you'll need to set up a free IBM cloud account. Follow this link to sign up for an account https://www.ibm.com/cloud/.
  
  Once signed up you can browse the IBM cloud platform catalog for all services offered by IBM cloud. In this case search the catalog for **cloudant**, create the service instance by first selecting an **authentication method** and then clicking the **create button**. Once the instance has been created you can access cloudant through the **resource list** section of your IBM cloud dashboard. Once the resource opens up, select **service credentials** on the left tab, click the **new credential** button to create credentials for the service. Once you create your new credentials, you can view them by selecting **view credentials**. The image below highlights the credentials we'll need to store data on the cloudant database service.  
  
  ![credentials](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/Credentials.PNG)

  Now we have the credentials necessary to use the cloudant database service. The next section explains how to use cloudant in python.
  
  **Setting up cloudant in python:**
  
  In order to use cloudant in python, the cloudant package must be installed. To install use the following commands :
  
   ```cmd
  pip install cloudant
  ```
  or
   ```cmd
  py -2.7 –m pip install cloudant
  ```
  **Connecting to cloudant in python:**
  
  To connect to cloudant in python you first have to import the intalled cloudant package and then provide your credentials. The code snippet below shows how to import cloudant:
   ```python
  from cloudant.client import Cloudant
  from cloudant.adapters import Replay429Adapter
  ...
  ```
  After importing the package we can now establish a connection to the cloudant database service using our credentials with the code snippet below:
    ```python
  ...
  client = Cloudant('your-username-here', 'your-password-here', url='your-url-here',adapter=Replay429Adapter(retries=10, initialBackoff=0.01))
  client.connect()
  ...
  ```
  Once we've established a connection we can now perform actions like, creating a database or adding data to an existing database. The cloudant database uses **JSON objects** as it's records. The database records in this case are calleed **documents**. For our example, the python dictionary objects holding the data scrapped from the webpage will be saved as individual documents corresponding to a record in the database. 
  
  To create a database we can call the **create database** method on the client variable. The code snippet below demonstrates how to create database: 
   ```python
  ...
  client.connect()
  news_articles_db = client.create_database("news_articles")
  ...
  ```
  To add a record to the database we can call the **create document** method on the database object. The code snippet shows how to do exactly that:
    ```python
  ...
  news_articles_db.create_document(python_dictionary)
  client.disconnect()
  ```
  
  Now that we can use cloudant to save our scrapped data, we're all set up with the tools we need to run our web scrapper. You'll find the full code in the `app.py` file of the app folder of this repository with comments explaining the code.
  
## 2.  Containerise the python web scraper using Docker

Containers help us bind our project in an environment necessary for our project to run including all the external packages it needs. This allows our project to work anywhere and not only on the machine we worked on to create it. There several options for containerisation offered by several platforms. In this example we'll be using the docker platform to containerise our project. 

In order to use docker you'll need to download and install **docker desktop** for your specific system type and operating system. For older machines it's recommended to use **docker toolbox**. In this example we'll be continuing with docker toolbox, here's a link to the download page https://docs.docker.com/toolbox/toolbox_install_windows/. Make sure to enable virtualisation in your **BIOS** before using docker toolbox or docker desktop.

After successfully installing docker toolbox, you can use docker by running the **docker quick start terminal**. In order to containerise the web scraper we first need to change our current directory to the directory containing the web scraper. The directory containing the web scraper must contain a **docker file**. A docker file is a text file that contains all the commands necessary to assemble a docker image. In this example our docker file will contain the python 2.7 runtime as the parent image of the web scraper. The file also contains a command to use **python pip** to install all the packages needed to run the web scraper. The code snippets below break down the contents of the docker file necessary for the web scraper to work.

First things first we need a python environment to run our python based web scraper. So for this we need to set a python runtime as the parent image of the web scraper. The referenced image is an official python image pulled directly from **docker hub**.
```dockerfile
FROM python:2.7-slim
```
Next we set the working directory to app, which will contain all the files that the web scraper needs to run and to build the docker image.
```dockerfile
WORKDIR /app
```
Once the working directory is established we need to copy all the files in our current project directory to the working directory.
```dockerfile
COPY . /app
```
After the files have been copied, all the necessary dependencies will have to installed using python pip.
```dockerfile
RUN pip install --trusted-host pypi.python.org -r requirements.txt
```
The contents of `requirements.txt`:
```text
unirest
lxml
urllib3
bs4
Cloudant
```
Once all the dependencies are installed the web scraper is ready to run by making a command line instruction.
```dockerfile
CMD ["python", "app.py"]
```
Once we have our **docker file** all set up we can finally build the docker image for our web scraper by executing the following command in the docker terminal.
```docker
docker build --tag=web_scraper .
```

## 3.  Upload Docker container of the web scraper to Docker Hub

Supposing that we successfully built the docker container in the previous section. **Docker hub** allows us to host our project's image much like **github repositories**. In this section we'll be uploading the already built container to docker hub. 

In order to upload to docker hub you first need to create a free account using the following link if you don't already have an account. https://hub.docker.com/signup

Once signed up take note of your credentials we'll need them in the next step. Open the docker terminal and connect to your newly created account using the docker login command.
```docker
docker login
```
After logging in we'll now tag the docker container to the docker hub account currently logged in. This action creates a repository to host the image on docker hub.
```docker
docker tag web_scraper user_name/web-scraper:v1
```
```docker
$ docker image ls
REPOSITORY                 TAG                 IMAGE ID            CREATED             SIZE
user_name/web-scraper      v1                  c4b87238b670        2 hours ago         152MB
web_scraper                latest              c4b87238b670        2 hours ago         152MB
```
Once the repository has been created on your machine, we can now make a **push action** to docker hub.
```docker
docker push user_name/web-scraper:v1
```
After the push action has been made and has completed the push process you can verify the created repository by accessing your account. 

## 4.  Deploy the container to IBM cloud

Now that the web scraper has been containerised and hosted on docker hub, we can now deploy it as a **cloud function** on ibm cloud. Once deployed as a cloud function IBM cloud makes a **pull action** on the hosted container in order to execute the web scraper on the cloud. 

In order to deploy the container to IBM cloud you'll need to download and install the **IBM cloud functions CLI**. Here's the link https://cloud.ibm.com/docs/cli/reference/bluemix_cli?topic=cloud-cli-install-ibmcloud-cli#install-ibmcloud-cli .

After successfully installing the IBM cloud functions CLI, open the docker terminal to install the cloud functions plugin. To install the plugin run the command below in the docker terminal:
```docker
ibmcloud plugin install cloud-functions
```
Once the plugin is installed we can now login to our IBM cloud account in order to create a cloud function using the hosted web scraper container. The IBM login command must include the **cloud foundry org** and **cloud foundry space**. If you have'nt created any cloud foundry org, the default is the email you used to sign up to IBM cloud. To confirm these details you can type **functions** in the search bar of the IBM cloud website. Once presented the functions page you can click the **start creating** button. If presented the error of `No Cloud Foundry Space`, simply close it and change the region in the region section, to the region you account is based on. Once the right region has been selected you can clearly see your cloud foundry org and cloud foundry space details. To login using these details you can execute the command below:
```docker
ibmcloud login -a cloud.ibm.com -o "cloud_foundry_org" -s "cloud_foundry_space"
```
After successfully logging in to the IBM account we now need to login to the docker hub account hosting the web scraper container.
```docker
docker login
```
Once logged in to the two accounts we can now deploy the web scraper container as a cloud function on IBM cloud. To do this we create a new action that will pull the container from docker hub.
```docker
ibmcloud fn action create cloud_webscraper --docker <username>/web-scraper:v1
```
After executing the above command, the action is created and can be viewed in the actions tab of the IBM cloud functions page. Open the created action by clicking the name. Once presented the **action's page**, select **Runtime** in order to modify the default runtime timeout of 60 seconds to 300 seconds. This done to allow the web scraper enough time to run without being interrupted. It takes roughly 60 seconds for the container to pulled by IBM cloud, so a 60 second timeout would'nt allow the web scraper to run. 

The screenshots below show how to check for the created **action** on IBM cloud and how to modidify the runtime timeout:

**Accessing the actions from the IBM cloud Functions page:**

![Action1](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/actions_1.PNG)

**Selecting our desired Action from the actions list:**

![Action2](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/actions_2.PNG)

**Accessing the runtime tab:**

![Action3](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/actions_3.PNG)

**Modifying the runtime timeout:**

![Action4](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/actions_4.PNG)

## 5.  Create time controlled triggers on the IBM cloud functions service

Triggers are very useful in completing the autonomous experience. This means that the cloud function can be executed without you having to explicitly run it. There several types of triggers we could use on an action but for this is example we'll be using the time controlled triggers. This means that for the days selected and times selected the action will be triggered on the cloud and will work fully autonomously.

Our example involved getting news articles from a news website. So our trigger will basically execute the action that executes the web scraper to get scrap news articles from the site every morning when the site is updated. Executing the web scraper then adds the latest articles to the cloud based database and this sums up the entire project of an autonomous cloud based web scraper. 

The screenshots below demonstrate how to add a time controlled trigger to the created action of the web scraper:

**Accessing the triggers from the IBM cloud Functions page:**

![Trigger1](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/triggers_1.PNG)

**Start the trigger creation process:**

![Trigger2](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/triggers_2.PNG)

**Selecting the periodic trigger type:**

![Trigger3](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/triggers_3.PNG)

**Configuring the trigger:**

![Trigger4](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/triggers_4.PNG)

**Connecting an action to the trigger:**

![Trigger5](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/triggers_5.PNG)

**Adding an existing action to the connection:**

![Trigger6](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/triggers_6.PNG)

**Viewing the connected action:**

![Trigger7](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/images/triggers_7.PNG)

