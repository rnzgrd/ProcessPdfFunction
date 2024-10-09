import logging
import os
import requests
import json
import azure.functions as func
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

app = func.FunctionApp()

@app.function_name(name="ProcessPdfFunction")
@app.route(route="processpdf", auth_level=func.AuthLevel.ANONYMOUS)
def process_pdf_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing PDF link...')

    # Get PDF link from the request
    pdf_url = req.params.get('pdf_url')
    if not pdf_url:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = None
        if req_body:
            pdf_url = req_body.get('pdf_url')

    if not pdf_url:
        return func.HttpResponse(
            "Please pass a PDF URL in the 'pdf_url' query parameter or in the request body",
            status_code=400
        )

    try:
        # Fetch the PDF content
        response = requests.get(pdf_url)
        response.raise_for_status()
        pdf_content = response.content

        # Use your provided endpoint and key
        endpoint = "https://docint-qima-pdf-test.cognitiveservices.azure.com/"
        key = "1f16f9b39bd6416ebf58663798896cd6"

        # Create a DocumentAnalysisClient
        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        # Use the 'read' API to analyze the document
        poller = document_analysis_client.begin_analyze_document(
            model_id="prebuilt-read", document=pdf_content
        )
        result = poller.result()

        # Convert the result to a dictionary
        json_result = result.to_dict()

        # Return the JSON result
        return func.HttpResponse(
            body=json.dumps(json_result, ensure_ascii=False, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )