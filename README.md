# A CLOUD BASED WEB SCRAPER

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
  
- ### Let's code:

  We’re now all set up to write our web scraper in python. Where to start? Well basically we’ll have to make an HTTP request to the website we want to extract data from and after getting a response, we’ll navigate through the HTML tags to get the data we want. So for our example we’ll be getting **Business news articles** from a news website. Because why not? The news is paginated and each page contains 10 news articles. For our example we’ll only be scraping data off the first two pages to get the most recent Business news.
  
  It’s necessary to understand the structure of the webpage in order to extract data more intelligently. So the first thing to do is **access the desired webpage** in your **browser** of choice, then right click on an element on the page and select **inspect**. This opens up the **development tools tab**, allowing you to see the HTML tags structure. It helps if you understand basic HTML syntax to better understand the anatomy of a website.
  
  The image below shows the layout used by each news article on the site :
  
  ![news_article_layout](https://github.com/Kabuswe/Cloud-Web-Scraping/blob/master/news_article.PNG)
  
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
