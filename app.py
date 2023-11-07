import base64
from multiprocessing import process
from flask import Flask, render_template, request
from flask_cors import CORS
import requests,logging,os
from bs4 import BeautifulSoup
import dotenv
import requests
import json

SLACK_CHANNEL_ID = os.getenv("SLACK_CHHINAL_ID")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")

# Create a logging file
logging.basicConfig(filename="img_scrapper.log", level=logging.INFO)
app = Flask(__name__)

# Enable CORS
CORS(app)

@app.route("/", methods=["GET"])
def homepage():
    return render_template('index.html')

@app.route("/sendcomment", methods=["GET", "POST"])
def sendMsg():
    thread_ts = None
    comment = request.form['comment']
    name = request.form['nameInput']
    print("comment", comment)
    print("name", name)

    # response = requests.get()
    message_body = {
        "text": f"Attention <!channel> :rotating_light: :rotating_light: {name} is Send Some message. Please check the thread for logs :eyes:"
    }

    print("message_body", message_body)
    # Post initial message
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {SLACK_TOKEN}"
        },
        json={
            **message_body,
            "channel": SLACK_CHANNEL_ID
        }
    )
    print("response", response)
    if response.ok:
        thread_id = response.json().get("ts")

        # Post messages in the thread
        if comment:
            request_body = {
                "text": "failing scenarios",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Hey Prashant , : {name} is sent a message"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Message ==> ```{json.dumps(comment)[:2800]}```"
                        }
                    }
                ],
                "channel": SLACK_CHANNEL_ID,
                "thread_ts": thread_id
            }

            requests.post(
                "https://slack.com/api/chat.postMessage",
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                    "Authorization": f"Bearer {SLACK_TOKEN}"
                },
                json=request_body
            )
    else:
        print(f"Error posting initial message to Slack: {response.json()}")
    
    # Add the return statement here
    return render_template("msg.html")
    # return "Message sent successfully"

# Your other routes remain unchanged...


@app.route("/search", methods=["POST"])
def index():
    if request.method == "POST":
        try:
            query = (request.form['content'].replace(" ", ""))
            
            # Create a directory to store the images
            save_dir = os.path.join("/SearchImages", query)
            
            # Check if the directory exists or not
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            # Create a fake agent to avoid getting blocked by Google
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            
            # Search for the images 
            response = requests.get(f"https://www.google.com/search?q={query}&sxsrf=AJOqlzUuff1RXi2mm8I_OqOwT9VjfIDL7w:1676996143273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiq-qK7gaf9AhXUgVYBHYReAfYQ_AUoA3oECAEQBQ&biw=1920&bih=937&dpr=1#imgrc=1th7VhSesfMJ4M")
            
            # Apply Beautiful Soup to the response
            Beautiful_soup = BeautifulSoup(response.text, "html.parser")
            
            # Find the img tag in the response
            img_tags = Beautiful_soup("img")
            
            # Delete the first element of the list
            del img_tags[0]
            
            # Create an empty list to store the images
            img_data = []
            
            # Loop through the img tags
            for index, img_tag in enumerate(img_tags):
                # Fetch the URL of the image
                img_url = img_tag["src"]
                print(img_url)

                # Trigger the URL to fetch the images
                image_data = requests.get(img_url).content
                
                # Create a dictionary 
                img_dict = {"Index": index, "Image": image_data}
                
                # Append the dictionary to the list
                img_data.append(img_dict)
                
                # Save the images in the folder
                with open(os.path.join(save_dir, f"{query}_{index}.jpg"), "wb") as f:
                    f.write(image_data)
                    
                try:
                    images_folder=save_dir
                    for index, filename in enumerate(os.listdir(images_folder)):
                        # Check if the file is an image (you might want to improve this check)
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            with open(os.path.join(images_folder, filename), 'rb') as f:
                                image_data = base64.b64encode(f.read()).decode('utf-8')
                                img_data.append({"Index": index, "Image": image_data})
                                
                except Exception as e:
                    # Handle exceptions, e.g., file not found, permission issues, etc.
                    print(f"Error reading images: {str(e)}") 
                           
            # Render the result.html template with the downloaded images
            return render_template("result.html", img_data=img_data, query=query)
                
        except Exception as e:
            logging.error(e)
            return "Something went wrong"
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9089, debug=True)

