# Serverless Email Attachment Processor

The `serverless-email-attachment` project provides a fully serverless solution designed for extracting, formatting, storing, and delivering `.csv` file attachments from emails. Utilizing AWS services, including Lambda and S3, alongside Simple Email Service (SES) triggers, this project automates the handling of email attachments efficiently and scalably.

## Features

- **Email Attachment Extraction**: Automatically extracts `.csv` attachments from incoming emails.
- **Data Transformation**: Formats the extracted `.csv` files according to predefined rules.
- **Serverless Deployment**: Utilizes AWS Lambda for processing, ensuring scalability and cost-efficiency.
- **S3 Integration**: Stores the processed attachments in an S3 bucket, facilitating easy access and management.
- **Customizable**: Easily adaptable to handle various attachment types and processing logic.

## Folder Structure

```
serverless-email-attachment/
│
├── src/
│ └── get_email_attachment.py # Main Lambda function for processing emails
│
├── serverless.yml # Serverless Framework configuration file
└── requirements.txt # Python dependencies
```

## Deployment

### Prerequisites

- AWS account
- AWS CLI installed and configured
- Serverless Framework

### Steps

1. **Install Dependencies**

   Ensure you have the Serverless Framework installed. If not, you can install it globally with npm:
 
    ```sh 
    npm install -g serverless
    ```

2. **Deploy the Service**

   Navigate to the project directory and deploy the service using the Serverless Framework:

    ```sh
   serverless deploy
   ```

   This command deploys your function to AWS Lambda, configures the S3 bucket triggers, and sets up the necessary permissions.

3. **Configure SES**

   Set up an AWS SES receipt rule to forward incoming emails to the S3 bucket configured in the `serverless.yml`. Ensure the emails have `.csv` attachments and make sure you adjust the subject environment variable in the `serverless.yml` to match the emails you want to filter.

## Configuration

- **Environment Variables**: Customize behavior by setting environment variables in `serverless.yml`.
  - `ENV`: Deployment environment (`dev`, `staging`, or `prod`).
  - `BUCKET`: The name of the S3 bucket for storing processed attachments.
  - `TARGET_FOLDER`: The folder within the S3 bucket where attachments are stored.
  - `SUBJECT`: The email subject line to filter for processing attachments.

- **Serverless Plugins**: Utilizes `serverless-python-requirements` for Python dependency management and `serverless-pseudo-parameters` for easier AWS account parameterization.

## Usage

Once deployed, the service automatically processes incoming emails that are forwarded to the S3 bucket by SES. Emails matching the specified subject line and containing `.csv` attachments are processed. The attachments are formatted and stored in the specified S3 bucket location.

## Contributions

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes or improvements.

## License

Specify your project's license here, ensuring it's appropriate for your project's usage and distribution.