
#Image Scraping Project

##Introduction:
    This project is aimed at scraping images from various websites and performing certain operations on them. The scraped images can then be shared or utilized for different purposes. Additionally, this project integrates with Slack APIs to provide notifications and sharing capabilities.

##Installation:
To run this project locally, follow these steps:

Clone the repository to your local machine:
   
   ###git clone <repository_url>

Install the required Python packages using pip:

pip install -r requirements.txt

pip install
pip install flask
pip install flask_cors
pip install python-dotenv
pip install beautifulsoup4
pip install requests


#Usage
  Running the Application
  Navigate to the project directory:

        cd ImageScrappingProject

Run the Flask application:

        python app.py

Access the application in your web browser at http://localhost:3625.

#Integration with Slack APIs

This project integrates with Slack APIs to provide the following functionality:

##Notification: 

Receive notifications about the status of the image scraping process.
    A. Sharing: Share scraped images directly to Slack channels or users.
    B. To enable Slack integration, follow these steps:

    1. Create a new Slack app in your Slack workspace.
    2. Obtain the API token for your Slack app.
    3. Configure the Flask application to use the Slack API token for authentication.