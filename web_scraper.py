from selenium import webdriver

def get_links(driver: webdriver.Chrome) -> list:
    '''
    Returns a list with all the links in the current page
    Parameters
    ----------
    driver: webdriver.Chrome
        The driver that contains information about the current page
    
    Returns
    -------
    link_list: list
        A list with all the links in the page
    '''

    prop_container = driver.find_element(by=By.XPATH, value='//div[@class="css-1itfubx e5pbze00"]')
    prop_list = prop_container.find_elements(by=By.XPATH, value='./div')
    link_list = []

    for house_property in prop_list:
        a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
        link = a_tag.get_attribute('href')
        link_list.append(link)

    return link_list

big_list = []
driver = load_and_accept_cookies()

for i in range(5): # The first 5 pages only
    big_list.extend(get_links(driver)) # Call the function we just created and extend the big list with the returned list
    ## TODO: Click the next button. Don't forget to use sleeps, so the website doesn't suspect
    pass # This pass should be removed once the code is complete


for link in big_list:
    ## TODO: Visit all the links, and extract the data. Don't forget to use sleeps, so the website doesn't suspect
    pass # This pass should be removed once the code is complete

driver.quit() # Close the browser when you finish