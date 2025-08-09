import json
import boto3
import uuid
from datetime import datetime

polly = boto3.client('polly')
s3 = boto3.client('s3')

BUCKET_NAME = "polly-output-bucket-for-files"

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        
        if "body" not in event:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Missing request body"})
            }
        
        body = event["body"]
        if event.get("isBase64Encoded", False):
            import base64
            body = base64.b64decode(body).decode('utf-8')
        
        data = json.loads(body)
        text_to_speak = data.get("text")
        if not text_to_speak:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Missing 'text' field in request body"})
            }

        response = polly.synthesize_speech(
            Text=text_to_speak,
            OutputFormat='mp3',
            VoiceId='Joanna'
        )
        
        audio_stream = response.get('AudioStream')
        if audio_stream is None:
            return {
                "statusCode": 500,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Failed to synthesize speech"})
            }
        
        filename = f"speech_{uuid.uuid4().hex}.mp3"
        
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=audio_stream.read(),
            ContentType='audio/mpeg'
        )
        
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Speech synthesized and uploaded successfully",
                "filename": filename,
                "url": presigned_url
            })
        }
        
    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
