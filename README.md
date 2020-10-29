# Sample Flask application

Small Flask application to demonstrate an application with traces from non-lambda and lambda. It is meant to be used with the [face recognition serverless application](https://github.com/arapulido/face-recognition-serverless-app).

It has a small web form that will upload an image to a S3 bucket, and will call the [FaceDetection function](https://github.com/arapulido/face-recognition-serverless-app/blob/master/functions/face_detection.py).

## Usage

* Deploy the Lambda pipeline following the instructions in its [README.md file](https://github.com/arapulido/face-recognition-serverless-app/blob/master/README.md).
* Install the Datadog agent for your system following its [installation instructions](https://docs.datadoghq.com/agent/basic_agent_usage/?tab=agentv6). Make sure that [tracing is enabled](https://docs.datadoghq.com/tracing/send_traces/). 
* Clone this repository and install locally

```
git clone https://github.com/arapulido/upload-picture-s3-face-recognition
cd upload-picture-s3-face-recognition
mkvirtualenv upload-picture-s3-face-recognition
pip install -r requirements.txt
```

* Configure the application through environment variables:
 
 |Variable|Description|
 |---|---|
 |`SECRET_KEY`|The Flask secret key||
 |`S3_BUCKET`|The name of the bucket to upload the image to|
 |`S3_KEY`|An AWS key with permissions to upload items to the S3 bucket|
 |`S3_SECRET_ACCESS_KEY`|The key secret for `S3_KEY`|
 |`FACE_DETECTION_ENDPOINT`|The URL that will call the Face Detection function|

* Run the application:

```
python application.py
```



