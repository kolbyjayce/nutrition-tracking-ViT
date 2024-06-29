## Nutritional analysis AI

The purpose of this project was to experiment with deploying an AI model from hugging face (google ViT) to a real world application. It is built using flask to be hosted on a web server. I was able to run this model easily on my laptop with 4 GB of vRam but I have not tried running on CPU only.

To run this site, ensure that a .env file exists with a USDA api key. If none, then one can be grabbed from this site
https://fdc.nal.usda.gov/api-key-signup.html

### Running

Install all prerequisites listed in requirements.txt `pip install -r ./requirements.txt`

The entry file is run.py. Simple run that python file and the server will start. It will host it on your local computer port 3000

Can be visited from localhost:3000 or your ip address (ex 192.168.1.64:3000) for visibility from other devices on your network.

### Flow

The AI model is a temporary solution to eventually be replaced with a custom fine-tuned model once enough data is gathered. For now, it works but many inputs need to be verified.

1. A picture is input
2. A prediction is returned
3. The prediction is verified
4. If false, the corrected input is stored in a sqlite database
5. Then the correct label (from AI or user input) is searched in a nutrition API
6. The result is then displayed

### Future Considerations
- Fine-tuned model on gathered real world data
- Potential architecture switch once enough classes are gathered (to CNN)
- Integration of FoodData Central ID into training
    - Currently outputs label, outputting integer label instead could be more efficient
- Incorporating serving size into image analysis
    -No data sets were complete enough to accomplish this task. By gathering data (food classification, image, serving size) at once, a model can be trained to accomplish this
- Storage of accounts, nutritional information, etc. As a real application would run
- Mobile application to communicate with api to allow for easy upload