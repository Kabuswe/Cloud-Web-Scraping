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
- **Cloud phantomjs platform:** this platform will help render the web pages from the HTTP requests we'll make on the cloud. Once a page is rendered the response is returned as HTML.

## Build flow

It always helps to know the end goal of a project to better understand what features to implement. Below is a list of steps we’ll take to reach our end goal: 
