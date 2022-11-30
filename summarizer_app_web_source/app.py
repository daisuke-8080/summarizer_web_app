from flask import Flask, render_template, request, url_for
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from config import key, endpoint

key = key
endpoint = endpoint

# Authenticate the client using your key and endpoint
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for summarizing text
def sample_extractive_summarization(client, input_text):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        ExtractSummaryAction
    ) 

    document = [
    {"id":"1","language": "ja", "text": input_text}
]

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(max_sentence_count=4)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("...Is an error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            summarized_text = "{}".format(
                " ".join([sentence.text for sentence in extract_summary_result.sentences]))
            print(summarized_text)
            return summarized_text


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def Summarizer():
    if request.method == 'POST':
        posted_text = request.form['text_form']
        posted_text = posted_text.replace("  ", "")
        summarized_text = sample_extractive_summarization(client, posted_text)
        return render_template('result.html', posted_text=posted_text, summarized_text=summarized_text)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
