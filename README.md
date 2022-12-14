# Data_Collection_Pipeline

This is the web scraper project that employs the scraper on the IMDB website to gather information on top trending anime.
The idea is to collect all the information for easy comparison and store the data scalably on the cloud.

The project uses Python, Selenium, Chromedriver, AWS S3, AWS EC2 and AWS RDS
 to perform the above

## Table of Contents
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)


## Technologies Used
- Python latest
- Chromedriver: latest
- Chrome: latest
- AWS S3
- AWS RDS
- Docker set up on the EC2 instance
- Prometheus
- Grafana Dashboard


## Features
Scraper code:
- takes user input
- scrapes data according to selected number of pages
- creates json file for tabular data, uploads to AWS S3 bucket 
- screenshots images, 50 per page, uploaded to AWS S3
- checks if piece of data already exsists based on id and data name

Additional applications:
- Scraper is containerized through docker and is run on AWS EC2 instance
- Scraper is run in headless mode from the EC2 instance
- Prometheus monitoring is added on top of the container to monitor docker state on EC2
- Grafana dashboard is created on the local machine to monitor the metrics of the containers (Docker) and the hardware metrics of the EC2 instance.

CI/CD Pipeline:
- Github secrets/ github actions created to monitor master branch update and push updates to dockerhub using docker access token saved as github secret
- Cron is set up on EC2 to remove, pull, run container with scraper every 24 hours


## Setup
The required libraries are:
- boto3
- bs4
- numpy
- os
- pandas
- psycopg2
- requests
- selenium
- time
- urllib3
- uuid
- sqlalchemy


Required additional modules:
- import config: xpath constants
- the aws access and secret keys are input as env variables
- RDS engine variables


## Usage
The code is run in 5 steps; running the scraper, gathering the data, creating the data frame(df), uploading df to aws and saving images (either locally or on aws)

1. Running the scraper: 
- This code asks the user how many pages to scrape, then proceeds to launch the webdriver in headless mode, scroll through the first page (in order to load all images), gather the data and finally go to the next page. This process is repeted unil the desired number of pages has been scraped.
```
def run_scraper(self):

    pages = input('How many pages do you wanna scrape: ')

        for i in range(int(pages)):
            self.scrolling()
            self.get_data(pages)    

        self.save_location()
```

2. Gathering the data.
- After the previous function is done running, this function start scraping for the data. (partial code shown below)

```
        for titles in range(len(amount)):

            self.uuid.append(str(uuid.uuid4()))
            if id in list(df['uuid']):
                continue

            item = self.driver.find_elements(By.XPATH, '//div[@class="lister-list"]/div')[titles]
            info = (item.text).split('\n')
            temp_title = info[0].split('(')[0].strip() 
            temp_year = info[0].split('(')[1].replace(')', '') 
            temp_genre = info[1].split('|')[-1].strip() 

            temp_check = info[1].split('|')
            if len(temp_check) == 3:
                temp_rating = temp_check[0]
            else:
                temp_rating = np.NAN
```

3. Creating the df:
- This function creates a dataframe, using pandas, and stores the data gathered in the get_data function locally as a .json file.
```
    def create_df(self):

        print('Creating the dataframe to store all data')
        anime_df = pd.DataFrame({'Title':self.title, 'Year':self.year, 'Link':self.link, 'Genres':self.genre, 'Rating':self.rating, 'ID':self.id, 'UUID':self.uuid, 'Image Links':self.img_link, 'Image Names':self.img_name})
        anime_df.index +=1
        anime_df = pd.concat([df,temp_anime_df],ignore_index=True)
        anime_df.to_json(r'raw_data/data.json')
        self.data_to_aws(anime_df)
```

4. Upload to AWS:
- This code simply dumps the df to the s3 bucket in aws.
```
    def data_to_aws(self):
        print('Uploading dataframe to AWS')
        s3= boto3.client('s3')
        s3.upload_file('raw_data/data.json', 'anime-cloud', 'Raw-Data')
        anime_df.to_sql('animescraper',self.engine, if_exists="replace")
```

5. Save location:
- Lastly this bit of code runs and asks the user where to save the images.
```
    def save_location(self):
        location = input('Save Images locally (pc) or local+cloud (both)? Please type ???pc??? or ???both??? to make your choice: ').lower()
        if location == 'pc':
            print('You chose PC')
            self.local_img_save()
        else:
            print('You chose both')
            self.local_img_save()
            self.img_to_aws()

```


## Project Status
Project is: _in progress_ 


## Room for Improvement
Room for improvement:
- The option for the user to have a choice of either print the data on screen or store the file remotely.
- Live progress bar to show how long code is going to run for.
- Several functions have been combined since the starting point, but the code can be further optimised to run quicker and more efficiently.
- The visualisation/ dashboard of the data as per the user request.


## Acknowledgements
- This project was inspired by AiCore program and my background in education.



## Contact
Created by [@EJKonge](ejkonge@gmail.com) - feel free to contact me!
