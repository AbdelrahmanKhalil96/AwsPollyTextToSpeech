# Text-to-Speech API with AWS Lambda, Polly, API Gateway, and S3

This project implements a serverless text-to-speech service that converts input text into speech audio using AWS Polly, stores the audio in an S3 bucket, and serves it securely to clients via presigned URLs.

---

## Architecture Overview

- **Frontend (index.html):** Simple web page allowing users to input text and trigger speech generation.
- **API Gateway:** Exposes a REST API endpoint to receive text input and trigger Lambda.
- **AWS Lambda:** Processes API requests, calls Amazon Polly to synthesize speech, uploads audio to S3, and returns a presigned URL.
- **Amazon S3:** Stores the generated MP3 audio files securely.
- **Presigned URLs:** Provide temporary, secure access to audio files for playback.

<img width="1536" height="1024" alt="ChatGPT Image Aug 9, 2025, 12_25_05 PM" src="https://github.com/user-attachments/assets/4c462c89-476f-4ead-8c45-04b87f8b6211" />

---

## Components

### 1. AWS Lambda Function

- Written in Python.
- Accepts POST requests with JSON body `{ "text": "Any Text" }`.
- Calls Amazon Polly to synthesize MP3 audio.
- Uploads audio file to private S3 bucket.
- Generates presigned URL valid for 1 hour.
- Returns JSON response with presigned URL for audio playback.

### 2. API Gateway

- REST API with a POST `/upload` method.
- Lambda Proxy Integration enabled.
- CORS enabled for cross-origin access from frontend.

### 3. S3 Bucket

- Bucket name: `polly-output-bucket-for-files`
- Bucket access: Private.
- Lambda role has permissions to `PutObject`.
- Audio files stored with unique filenames.

### 4. Frontend

- Simple HTML + JavaScript.
- Sends POST requests with input text to API Gateway.
- Receives presigned URL and plays audio in browser.

---

## Setup Instructions

1. **Create S3 Bucket**

   - Name it `polly-output-bucket-for-files` (or update code accordingly).
   - Keep it private (no public access).

2. **Create IAM Role for Lambda**

   - Attach policy allowing:
     - `polly:SynthesizeSpeech`
     - `s3:PutObject` on your bucket ARN.

3. **Create Lambda Function**

   - Use provided Python code (`lambda_function.py`).
   - Set timeout to at least 10 seconds.
   - Assign the IAM role created above.

4. **Create API Gateway REST API**

   - Create resource `/upload`.
   - Add POST method integrated with Lambda (Proxy Integration enabled).
   - Enable CORS on the resource.
   - Deploy API to a stage (e.g., `dev`).

5. **Configure Frontend**

   - Update `index.html` with your API Gateway invoke URL.
   - Serve the HTML file (locally or from any web host).

6. **Test**

   - Open frontend in browser.
   - Enter text and click "Generate Speech".
   - Audio will play after processing.

---
Actual Testing Link:

http://static-site-for-api-polly.s3-website-us-east-1.amazonaws.com/

## Notes

- The presigned URL expires after 1 hour for security.

---


