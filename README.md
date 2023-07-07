# detect_api
An api for detecting things contain in picture

## API URL
### Be used for testing
>request [GET]: `<HOST>/`<br>
>response: `{"column": "value"}, 201`

### Be used for uploading image to be detect
>request [POST]: `<HOST>/detect`<br>
>Content-Type: application/json
>`{"filename": "golden retriever.jpeg"}`<br>
>response: `{
    "chair": 99,
    "dog": 99,
    "handbag": 67,
    "person": 90
}`
>>terminal command: `curl -X POST http://127.0.0.1:5000/detect -H "Content-Type: application/json" -d '{"filename": "golden retriever.jpeg"}'`
