#We need to implement the cript in a way that when there is no more internet we can recover the data, we will make an exception for the error of when there is no internet and store the data and the last item scraped

# We need to import these libraries
# We will do the scraping using Selenium library which allows to see how the programm scrap the data and to interact with the website
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import re
import selenium
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try : #With this exception we will be able to save the scraped data if there is a problem with our connection or the website 
    #We create the driver using chrome
    driver = webdriver.Chrome()
    driver.get('https://www.huffandpuffers.com/')
    driver.maximize_window()
    parent_handle = driver.current_window_handle #does not have any interest here because there are never more than 1 window


    #Going on the disposables page
    disposables_page = driver.find_element(By.XPATH, '//*[@id="shopify-section-header"]/store-header/div/div/nav/desktop-navigation/ul/li[1]/a')
    disposables_page.click()

    #finding the number of pages for the disposables vapes
    all_pages = driver.find_elements(By.CLASS_NAME,"pagination__nav")
    all_pages_list=[]

    #creating the final lists of data, we will then turn them into csv files
    all_names = [] #list of products names
    all_prices = [] #list of products prices
    all_ratings = [] #list of products average ratings
    all_nbr_reviews = [] #list of reviews numbers of the products
    all_flavors = [] # list of flavor list of each products
    all_reviews = [] #...
    all_reviews_title = [] #...
    all_flavor_rating = [] #...
    all_sweetness_rating =[]
    all_lasting_rating = []
    all_nbr_1_stars = []
    all_nbr_2_stars = []
    all_nbr_3_stars = []
    all_nbr_4_stars = []
    all_nbr_5_stars = []





    for x in all_pages:
        all_pages_list.append(x.text)
    strings = all_pages_list[0].split()

    numbers = [int(x) for x in strings]
    nbr_pages=max(numbers)

    #creating a boucle to scrap all the pages
    for i in range (1,nbr_pages+1 ):
        current_page = i #we store where we are in this variable
        url = 'https://www.huffandpuffers.com/collections/disposable-salt-nicotine-devices?page='+str(i)
        driver.get(url)

        #scraping on all the products
        all_products = driver.find_elements(By.CLASS_NAME, "product-item__primary-image")
        for k in range(len(all_products)):
            current_product = k #we store on which product we are scraping
            driver.refresh() # it seems like refreshing the page erase the error of an element not interactible when we open the page again.
            all_products = driver.find_elements(By.CLASS_NAME, "product-item__primary-image") # we redefine what are all_products everytime so it does not raise an error of element not found.
            all_products[k].click() # we click on the product image to open it

            #opening all the reviews
            try : # When an element has no reviews we have to make a first exception
                
                page = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[3]/div/div[5]/button')

                try : 
                    # It seems like as the driver click to fast, we need to make him wait for the element to be clickable and to make a second exception because it also causes an error when all reviews pages are loaded

                    while driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[3]/div/div[5]/button').is_displayed()==True:
                        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[3]/div/div[5]/button'))).click()
                    #scraping the reviews and the reviews title
                    review = driver.find_elements(By.CLASS_NAME,"okeReviews-review-main-content")
                    review_title = driver.find_elements(By.CLASS_NAME, "okeReviews-review-main-heading")
                    reviews=[]
                    review_titles=[]

                    for x in review:
                        reviews.append(x.text)

                    for x in review_title:
                        review_titles.append(x.text)
                    
                    all_reviews_title.append(review_titles)
                    all_reviews.append(reviews)

                    #scraping the name and adding to the list
                    name = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/h1').text
                    all_names.append(name)

                    #scraping the price and adding to the list
                    price = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/div/div[1]/span').text.strip('Sale price\n$')
                    all_prices.append(price)

                    #scraping the number of reviews and adding to the list
                    nbr_reviews = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/div/div[2]/div/div/div[2]/span[1]').text.strip(' Reviews')
                    all_nbr_reviews.append(nbr_reviews)

                    #scraping the rating and adding to the list
                    rating = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/div/div[2]/div/div/div[1]/span/span[1]').text
                    all_ratings.append(rating)

                    #scraping the list of flavors
                    flavors_brut = driver.find_elements(By.CLASS_NAME,"block-swatch__item")
                    flavors=[]
                    for x in flavors_brut:
                        flavors.append(x.text)
                    all_flavors.append(flavors)

                    #scraping the rating for the flavor
                    flavor_rating = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]/div/div[1]/div[1]').get_attribute('style').strip('width: ')
                    all_flavor_rating.append(float(flavor_rating.strip('%;')))

                    #scraping the rating for the lasting
                    lasting_rating = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[2]/div/div[1]/div[1]').get_attribute('style').strip('width: ')
                    all_lasting_rating.append(float(lasting_rating.strip('%;')))

                    #scraping the rating for the sweetness
                    sweetness_rating = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/div/div[1]/div[1]').get_attribute('style').strip('width: ')
                    all_sweetness_rating.append(float(sweetness_rating.strip('%;')))

                    #scraping the number of stars of the reviews for each product
                    nbr_1_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[5]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_2_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[4]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_3_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[3]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_4_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[2]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_5_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[1]/div[2]/div/div[2]').text.strip('\nReviews')   
                    all_nbr_1_stars.append(nbr_1_stars)
                    all_nbr_2_stars.append(nbr_2_stars)
                    all_nbr_3_stars.append(nbr_3_stars)
                    all_nbr_4_stars.append(nbr_4_stars)
                    all_nbr_5_stars.append(nbr_5_stars)      
                    
                    driver.get(url) 
                        
                
                    
                except selenium.common.exceptions.TimeoutException  : #all reviews opened
                    
                    #scraping the reviews and the reviews title
                    review = driver.find_elements(By.CLASS_NAME,"okeReviews-review-main-content")
                    review_title = driver.find_elements(By.CLASS_NAME, "okeReviews-review-main-heading")
                    reviews=[]
                    review_titles=[]

                    for x in review:
                        reviews.append(x.text)

                    for x in review_title:
                        review_titles.append(x.text)
                    
                    all_reviews_title.append(review_titles)
                    all_reviews.append(reviews)

                    #scraping the name and adding to the list
                    name = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/h1').text
                    all_names.append(name)

                    #scraping the price and adding to the list
                    price = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/div/div[1]/span').text.strip('Sale price\n$')
                    all_prices.append(price)

                    #scraping the number of reviews and adding to the list
                    nbr_reviews = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/div/div[2]/div/div/div[2]/span[1]').text.strip(' Reviews')
                    all_nbr_reviews.append(nbr_reviews)

                    #scraping the rating and adding to the list
                    rating = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/div/div[2]/div/div/div[1]/span/span[1]').text
                    all_ratings.append(rating)

                    #scraping the list of flavors
                    flavors_brut = driver.find_elements(By.CLASS_NAME,"block-swatch__item")
                    flavors=[]
                    for x in flavors_brut:
                        flavors.append(x.text)
                    all_flavors.append(flavors)

                    #scraping the rating for the flavor
                    flavor_rating = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]/div/div[1]/div[1]').get_attribute('style').strip('width: ')
                    all_flavor_rating.append(float(flavor_rating.strip('%;')))

                    #scraping the rating for the lasting
                    lasting_rating = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[2]/div/div[1]/div[1]').get_attribute('style').strip('width: ')
                    all_lasting_rating.append(float(lasting_rating.strip('%;')))

                    #scraping the rating for the sweetness
                    sweetness_rating = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/div/div[1]/div[1]').get_attribute('style').strip('width: ')
                    all_sweetness_rating.append(float(sweetness_rating.strip('%;')))

                    #scraping the number of stars of the reviews for each product
                    nbr_1_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[5]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_2_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[4]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_3_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[3]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_4_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[2]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_5_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[1]/div[2]/div/div[2]').text.strip('\nReviews')   
                    all_nbr_1_stars.append(nbr_1_stars)
                    all_nbr_2_stars.append(nbr_2_stars)
                    all_nbr_3_stars.append(nbr_3_stars)
                    all_nbr_4_stars.append(nbr_4_stars)
                    all_nbr_5_stars.append(nbr_5_stars)      
                    
                    driver.get(url)

                except selenium.common.exceptions.ElementNotInteractableException  : #an error can happen beside the timeout error so we must make another excpetion
                
                #scraping the reviews and the reviews title
                    review = driver.find_elements(By.CLASS_NAME,"okeReviews-review-main-content")
                    review_title = driver.find_elements(By.CLASS_NAME, "okeReviews-review-main-heading")
                    reviews=[]
                    review_titles=[]

                    for x in review:
                        reviews.append(x.text)

                    for x in review_title:
                        review_titles.append(x.text)
                    
                    all_reviews_title.append(review_titles)
                    all_reviews.append(reviews)

                    #scraping the name and adding to the list
                    name = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/h1').text
                    all_names.append(name)

                    #scraping the price and adding to the list
                    price = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/div/div[1]/span').text.strip('Sale price\n$')
                    all_prices.append(price)

                    #scraping the number of reviews and adding to the list
                    nbr_reviews = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/div/div[2]/div/div/div[2]/span[1]').text.strip(' Reviews')
                    all_nbr_reviews.append(nbr_reviews)

                    #scraping the rating and adding to the list
                    rating = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/div/div[2]/div/div/div[1]/span/span[1]').text
                    all_ratings.append(rating)

                    #scraping the list of flavors
                    flavors_brut = driver.find_elements(By.CLASS_NAME,"block-swatch__item")
                    flavors=[]
                    for x in flavors_brut:
                        flavors.append(x.text)
                    all_flavors.append(flavors)

                    #scraping the rating for the flavor
                    flavor_rating = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]/div/div[1]/div[1]').get_attribute('style').strip('width: ')
                    all_flavor_rating.append(float(flavor_rating.strip('%;')))

                    #scraping the rating for the lasting
                    lasting_rating = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[2]/div/div[1]/div[1]').get_attribute('style').strip('width: ')
                    all_lasting_rating.append(float(lasting_rating.strip('%;')))

                    #scraping the rating for the sweetness
                    sweetness_rating = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/div/div[1]/div[1]').get_attribute('style').strip('width: ')
                    all_sweetness_rating.append(float(sweetness_rating.strip('%;')))

                    #scraping the number of stars of the reviews for each product
                    nbr_1_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[5]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_2_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[4]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_3_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[3]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_4_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[2]/div[2]/div/div[2]').text.strip('\nReviews')
                    nbr_5_stars = driver.find_element(By.XPATH,'//*[@id="shopify-block-7c9f8916-7108-428f-86be-8d0fc655727b"]/div/div/div/div[2]/div/div[1]/div/div[2]/ul/li[1]/div[2]/div/div[2]').text.strip('\nReviews')   
                    all_nbr_1_stars.append(nbr_1_stars)
                    all_nbr_2_stars.append(nbr_2_stars)
                    all_nbr_3_stars.append(nbr_3_stars)
                    all_nbr_4_stars.append(nbr_4_stars)
                    all_nbr_5_stars.append(nbr_5_stars)      
                    
                    driver.get(url)


                    

            except selenium.common.exceptions.NoSuchElementException :
            #No review to scrap at all
                

                reviews=[]
                review_titles=[]
                all_reviews.append('None')
                all_reviews_title.append('None')


                #scraping the name and adding to the list
                name = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/h1').text
                all_names.append(name)

                #scraping the price and adding to the list
                price = driver.find_element(By.XPATH, '//*[@id="shopify-section-template--15530171171000__main"]/section/div/div/div/product-meta/div/div[1]/span').text.strip('Sale price\n$')
                all_prices.append(price)
                
                all_nbr_reviews.append('None')
                
                all_ratings.append('None')

                #scraping the list of flavors
                flavors_brut = driver.find_elements(By.CLASS_NAME,"block-swatch__item")
                flavors=[]
                for x in flavors_brut:
                    flavors.append(x.text)
                all_flavors.append(flavors)

                
                all_flavor_rating.append('None')
                
                all_lasting_rating.append('None')
                
                all_sweetness_rating.append('None')
            
                all_nbr_1_stars.append('None')
                all_nbr_2_stars.append('None')
                all_nbr_3_stars.append('None')
                all_nbr_4_stars.append('None')
                all_nbr_5_stars.append('None')      
                
                driver.get(url) #we return to the main page of disposables



    # we create the dataframe
    final_dic = {'product_name':all_names, 'price':all_prices, 'nbr_reviews':all_nbr_reviews, 
                'flavor':all_flavors,'reviews_title':all_reviews_title, 'reviews':all_reviews, 
                'flavors_rating':all_flavor_rating, 'sweetness_ratings':all_sweetness_rating, 'lasting_rating':all_lasting_rating,
                'nbr_1_stars':all_nbr_1_stars, 'nbr_2_stars':all_nbr_2_stars, 'nbr_3_stars':all_nbr_3_stars, 'nbr_4_stars':all_nbr_4_stars,
                'nbr_5_stars':all_nbr_5_stars}

    df = pd.DataFrame(final_dic)
    print(df)
    print(df.size)

    df.to_csv('data.csv')

except selenium.common.exceptions.WebDriverException :

    print('a problem with the website or the connection occured. Scraped data was save in a csv and the progress of the scraping was stored in variables')
    print('the scraping was on page '+ str(current_page) + 'and on the product number'+ str(current_product))
    #We will check the length of the lists and fill them with 'None' so we can make a final csv without an error on the lengths of the arrays
    all = [all_names, all_prices, all_ratings, all_nbr_reviews, all_flavors, all_reviews, all_reviews_title, all_flavor_rating, all_sweetness_rating, 
    all_lasting_rating, all_nbr_1_stars, all_nbr_2_stars, all_nbr_3_stars, all_nbr_4_stars, all_nbr_5_stars]
    max_len = max([len(x) for x in all])
    for x in all :
        while len(x)<max_len:
            x.append('None')

    #we create the dataframe and the csv :
    partial_dic = {'product_name':all_names, 'price':all_prices, 'nbr_reviews':all_nbr_reviews, 
                'flavor':all_flavors,'reviews_title':all_reviews_title, 'reviews':all_reviews, 
                'flavors_rating':all_flavor_rating, 'sweetness_ratings':all_sweetness_rating, 'lasting_rating':all_lasting_rating,
                'nbr_1_stars':all_nbr_1_stars, 'nbr_2_stars':all_nbr_2_stars, 'nbr_3_stars':all_nbr_3_stars, 'nbr_4_stars':all_nbr_4_stars,
                'nbr_5_stars':all_nbr_5_stars}
    df2 = pd.DataFrame(partial_dic)
    print(df2)

    df2.to_csv('partial_data.csv')