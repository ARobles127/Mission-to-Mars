# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": hemisphere(browser),
      "last_modified": dt.datetime.now()
    } 

    # Stop webdriver and return data
    browser.quit()
    return data      

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


### JPL Space Images Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

### Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    # Convert pd DF into html df, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere(browser):
    # Visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

# 2. Create a list to hold the images and titles.\n",
    hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.\n",
    links = browser.find_by_css('a.product-item img')

    for i in range(len(links)):
        hemisphere={}
    
        #Find elements going to click link.
        browser.find_by_css('a.product-item img')[i].click()
    
        #Find sample image link
        sample_element=browser.links.find_by_text('Sample').first
    
        # Get hemisphere Title 
        hemisphere['img_url']=sample_element['href']
    
        # Get hemisphere Title 
        hemisphere['title']=browser.find_by_css('h2.title').text
    
        # Add Objects to hemisphere_image_urls list
        hemisphere_image_urls.append(hemisphere)
    
        #Go Back
        browser.back()
        
        # 4. Print the list that holds the dictionary of each image url and title.
        return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
