import requests
import random
import lorem
from data import skeleton_data_project, skeleton_data_article
from datetime import datetime, timedelta

# Define the date range for generating random dates
start_date = datetime(2020, 1, 1)  # Modify the start date as needed
end_date = datetime(2023, 12, 31)  # Modify the end date as needed

# Generate a random date within the specified range
# random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
random_date = datetime.now()

# Define the URL to post the data to
BASE_URL = "http://localhost:8000/api/v1"
PROJECT_URL = f"{BASE_URL}/ingest/iprox_project"
ARTICLE_URL = f"{BASE_URL}/ingest/iprox_article"

def ingest_projects():
    # Generate random project_id
    for project_id in range(100):
        # Populate skeleton data with Lorem Ipsum
        skeleton_data_project['title'] = lorem.sentence()
        skeleton_data_project['subtitle'] = lorem.sentence()

        skeleton_data_project['sections']['what'][0]['title'] = lorem.sentence()
        skeleton_data_project['sections']['what'][0]['body'] = lorem.paragraph()
        skeleton_data_project['sections']['where'][0]['title'] = lorem.sentence()
        skeleton_data_project['sections']['where'][0]['body'] = lorem.paragraph()
        skeleton_data_project['sections']['when'][0]['title'] = lorem.sentence()
        skeleton_data_project['sections']['when'][0]['body'] = lorem.paragraph()
        skeleton_data_project['sections']['work'][0]['title'] = lorem.sentence()
        skeleton_data_project['sections']['work'][0]['body'] = lorem.paragraph()

        skeleton_data_project['sections']['contact'][0]['title'] = lorem.sentence()
        skeleton_data_project['sections']['contact'][0]['body'] = lorem.paragraph()

        skeleton_data_project['contacts'][0]['id'] = random.randint(1, 1000)
        skeleton_data_project['contacts'][0]['name'] = random.randint(1, 1000)
        skeleton_data_project['contacts'][0]['position'] = random.randint(1, 1000)
        skeleton_data_project['contacts'][0]['phone'] = '+31612345678'
        skeleton_data_project['contacts'][0]['email'] = 'foo@bar'

        skeleton_data_project['timeline']['title'] = lorem.sentence()
        skeleton_data_project['timeline']['intro'] = lorem.paragraph()
        skeleton_data_project['timeline']['items'][0]['date'] = random_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        skeleton_data_project['timeline']['items'][0]['title'] = lorem.sentence()
        skeleton_data_project['timeline']['items'][0]['body'] = lorem.paragraph()
        skeleton_data_project['timeline']['items'][0]['items'][0] = lorem.paragraph()
        skeleton_data_project['timeline']['items'][0]['collapsed'] = True

        skeleton_data_project['image']['id'] = random.randint(1, 1000)
        skeleton_data_project['image']['alternativeText'] = lorem.sentence()
        skeleton_data_project['image']['aspectRatio'] = 1024/768
        skeleton_data_project['image']['sources'][0]['url'] = lorem.sentence()
        skeleton_data_project['image']['sources'][0]['width'] = 1024
        skeleton_data_project['image']['sources'][0]['height'] = 768

        skeleton_data_project['images'][0]['id'] = random.randint(1, 1000)
        skeleton_data_project['images'][0]['alternativeText'] = lorem.sentence()
        skeleton_data_project['images'][0]['aspectRatio'] = 1024/768
        skeleton_data_project['images'][0]['sources'][0]['url'] = lorem.sentence()
        skeleton_data_project['images'][0]['sources'][0]['width'] = 1024
        skeleton_data_project['images'][0]['sources'][0]['height'] = 768

        skeleton_data_project['coordinates']['lat'] = 7.632432421348
        skeleton_data_project['coordinates']['lon'] = 78.324324897732

        skeleton_data_project['url'] = f'mock_{project_id}'
        skeleton_data_project['id'] = project_id
        skeleton_data_project['created'] = random_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        skeleton_data_project['modified'] = random_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        skeleton_data_project['publicationDate'] = random_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        skeleton_data_project['expirationDate'] = random_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        # Send a POST request with the populated data
        response = requests.post(PROJECT_URL, json=skeleton_data_project)

        # Check the response
        if response.status_code == 200:
            print(f"Successfully posted data for project_id: {project_id}")
        else:
            print(f"Failed to post data. Status code: {response.status_code}")
            print(response.text)

def ingest_articles():
    for article_id in range(1, 99):
        skeleton_data_article['title'] = lorem.sentence()
        skeleton_data_article['intro'] = lorem.paragraph()
        skeleton_data_article['body'] = lorem.paragraph()
        skeleton_data_article['image']['id'] = article_id + 100
        skeleton_data_article['image']['alternativeText'] = lorem.sentence()
        skeleton_data_article['image']['aspectRatio'] = 1024/768
        skeleton_data_article['image']['sources'][0]['url'] = f'mock_{article_id}'
        skeleton_data_article['image']['sources'][0]['width'] = 1024
        skeleton_data_article['image']['sources'][0]['height'] = 768
        skeleton_data_article['type'] = "foobar"
        skeleton_data_article['projectIds'] = [article_id, article_id + 1]
        skeleton_data_article['url'] = lorem.sentence()
        skeleton_data_article['id'] = article_id
        skeleton_data_article['created'] = random_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        skeleton_data_article['modified'] = random_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        skeleton_data_article['publicationDate'] = random_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        skeleton_data_article['expirationDate'] = random_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        # Send a POST request with the populated data
        response = requests.post(ARTICLE_URL, json=skeleton_data_article)
        
        # Check the response
        if response.status_code == 200:
            print(f"Successfully posted data for article_id: {article_id}")
        else:
            print(f"Failed to post data. Status code: {response.status_code}")
            print(response)
            print(response.text)

ingest_projects()
ingest_articles()
