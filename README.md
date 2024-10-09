
Azure Serverless PDF Analyzer API

Overview

This project is a serverless API function built using Azure Functions and Python. The API accepts a PDF URL, processes the document using Azure Document Intelligence (formerly known as Form Recognizer), and returns the extracted content as JSON output. This API demonstrates how to leverage Azure’s serverless architecture and cognitive services to build scalable and efficient applications.

Table of Contents

	•	Prerequisites
	•	Architecture
	•	Setup and Installation
	•	Clone the Repository
	•	Create Azure Resources
	•	Configure Environment Variables
	•	Install Dependencies
	•	Running the Function Locally
	•	Deploying to Azure
	•	Testing the API
	•	Using cURL
	•	Using Postman
	•	Error Handling
	•	Security Considerations
	•	Logging and Monitoring
	•	Contributing
	•	License

Prerequisites

	•	Azure Account: An active Azure subscription. You can create a free account here.
	•	Azure Functions Core Tools: Version 4.x. Installation instructions can be found here.
	•	Python 3.9: Ensure you have Python 3.9 installed, as it’s fully supported by Azure Functions.
	•	Visual Studio Code (Optional): With the Azure Functions extension for development and deployment.
	•	Azure CLI (Optional): For command-line deployment and management.

Architecture

	•	Azure Function App: Hosts the serverless function that processes the PDF.
	•	Azure Document Intelligence: Cognitive service used to analyze the PDF document and extract content.

Setup and Installation

Clone the Repository

git clone https://github.com/yourusername/azure-pdf-analyzer.git
cd azure-pdf-analyzer

Create Azure Resources

	1.	Azure Function App: Create a Function App in Azure to host your function.
	2.	Azure Document Intelligence Resource: Create a Form Recognizer resource in Azure.

You can create these resources via the Azure Portal or using the Azure CLI:

# Example using Azure CLI
az login

# Create a Resource Group
az group create --name myResourceGroup --location eastus

# Create a Storage Account (required for Function App)
az storage account create --name mystorageaccount --location eastus --resource-group myResourceGroup --sku Standard_LRS

# Create a Function App
az functionapp create --resource-group myResourceGroup --consumption-plan-location eastus --runtime python --functions-version 4 --name myFunctionApp --storage-account mystorageaccount

# Create a Form Recognizer Resource
az cognitiveservices account create --name myFormRecognizer --resource-group myResourceGroup --kind FormRecognizer --sku F0 --location eastus --yes

Configure Environment Variables

Local Development

Create a local.settings.json file in the root of your project to store environment variables:

{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "AZURE_FORM_RECOGNIZER_ENDPOINT": "<your_form_recognizer_endpoint>",
    "AZURE_FORM_RECOGNIZER_KEY": "<your_form_recognizer_key>"
  }
}

	•	Replace <your_form_recognizer_endpoint> with your Form Recognizer endpoint URL (e.g., https://your-resource-name.cognitiveservices.azure.com/).
	•	Replace <your_form_recognizer_key> with your Form Recognizer API key.

Important: Do not commit local.settings.json to source control. Ensure it’s listed in your .gitignore file.

Azure Deployment

Set the environment variables in your Function App’s configuration settings:

	1.	Navigate to Your Function App in the Azure Portal.
	2.	Under Settings, select Configuration.
	3.	Add the following application settings:
	•	AZURE_FORM_RECOGNIZER_ENDPOINT: Your Form Recognizer endpoint.
	•	AZURE_FORM_RECOGNIZER_KEY: Your Form Recognizer API key.
	4.	Save the changes and restart the Function App to apply the new settings.

Install Dependencies

Create a virtual environment and install the required packages:

python -m venv .venv
# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

Your requirements.txt should include:

azure-functions
azure-ai-formrecognizer
requests

Running the Function Locally

Start the Azure Functions host:

func start

You should see output indicating that your function is running:

Functions:

    ProcessPdfFunction: http://localhost:7071/api/processpdf

Deploying to Azure

Using Visual Studio Code

	1.	Install the Azure Functions extension for VS Code.
	2.	Sign in to your Azure account in VS Code.
	3.	Deploy the Function App:
	•	Right-click on your function app folder in the Azure Functions explorer.
	•	Select “Deploy to Function App…”.
	•	Follow the prompts to select your subscription and Function App.

Using Azure CLI

# Ensure you're logged in
az login

# Publish the function app
func azure functionapp publish <Your_Function_App_Name>

Testing the API

Using cURL

Example Request

curl -X POST "http://localhost:7071/api/processpdf" \
  -H "Content-Type: application/json" \
  -d '{"pdf_url": "https://example.com/sample.pdf"}'

	•	Replace http://localhost:7071 with your Function App URL when testing deployed functions.
	•	Replace https://example.com/sample.pdf with the URL of the PDF you want to analyze.

Example Response

{
  "content": "Extracted text content from the PDF...",
  "pages": [...],
  "languages": [...],
  "styles": [...],
  "paragraphs": [...],
  "tables": [...],
  "keyValuePairs": [...],
  "entities": [...],
  "documents": [...]
}

Using Postman

	1.	Open Postman and create a new POST request.
	2.	Set the request URL to http://localhost:7071/api/processpdf or your deployed function URL.
	3.	Set Headers:
	•	Key: Content-Type
	•	Value: application/json
	4.	Set Body:
	•	Choose raw and select JSON.
	•	Enter the JSON payload:

{
  "pdf_url": "https://example.com/sample.pdf"
}


	5.	Send the request and view the response.

Error Handling

The function includes error handling for common issues:

	•	Invalid or Missing PDF URL: Returns a 400 Bad Request with an error message.
	•	Unable to Access PDF: Returns a 500 Internal Server Error with an error message.
	•	Issues with Azure Document Intelligence: Returns a 500 Internal Server Error with an error message.

Ensure that:

	•	The PDF URL provided is correct and publicly accessible.
	•	Your Form Recognizer resource is correctly configured and the endpoint and key are valid.

Security Considerations

	•	API Keys: Store API keys securely using environment variables. Never hardcode them into your code or commit them to source control.
	•	.gitignore: Ensure sensitive files like local.settings.json and .env are listed in your .gitignore file.
	•	Authentication: The function is currently set to allow anonymous access (auth_level=func.AuthLevel.ANONYMOUS). For production environments, consider implementing authentication mechanisms.
	•	Input Validation: Validate input to prevent injection attacks and ensure robustness.

Logging and Monitoring

	•	Logging: The function uses the logging module to log important events and errors. Logs can be viewed in the console when running locally or through Azure Monitor when deployed.
	•	Monitoring: Set up Application Insights in Azure to monitor the performance and usage of your function app.

Contributing

Contributions are welcome! Please follow these steps:

	1.	Fork the repository.
	2.	Create a new branch for your feature or bug fix.
	3.	Commit your changes with clear messages.
	4.	Push your branch to your forked repository.
	5.	Submit a pull request to the main repository.

Please ensure your code follows the project’s coding standards and includes appropriate tests.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Note: Replace placeholders like <your_form_recognizer_endpoint> and <your_form_recognizer_key> with your actual endpoint and key in your local settings but never include these sensitive details in the README or any files committed to source control.

If you have any further questions or need assistance with any part of this project, feel free to ask!
