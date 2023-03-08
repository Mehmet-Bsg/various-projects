Explanation to use the script for data scraping : 

The only requirements are to download google chrome on your computer because the script uses ChromeDriver to scrap the data and install selenium library using pip install in your terminal

However Chrome can be changed with the driver of your choice when defining the driver at the beginning of the script. 
The scripted just have to be launched. It will scrap the data for the products named 'disposable' and store it in a csv. 
Numbers are turned into float and int (they are str type when scraped).

I chose to scrap what i thought was the most important : 
-the name of each product
-the price of each product
-the general rating (out of 5)
-the general ratings for the flavor, sweetness and duration (out of 100)
-the number of reviews with 0, 1, 2, 3, 4 and 5 stars for each product
-the text reviews and the titles of these reviews for each product

I think that could be enough to make data analysis from this informations. 

The script is able to store the data if there is an issue with the website or internet during the scraping and will tell you where was the progress before the issue.

It was my first time scraping a website (i have only done scraping on articles) and after reviewing all the options i had i chose selenium library because i though it would be great and i also love the fact that we can see where the scraping is and understand the errors

the scraping of the whole disposable section takes around 30 minutes with a normal internet connection 
