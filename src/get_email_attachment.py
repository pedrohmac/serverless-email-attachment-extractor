import email
import os
import logging
import boto3
from datetime import datetime

# Setup Logging
ENV = os.environ.get('ENV')
LEVEL = 'DEBUG' if ENV in ('DEV', 'STAGING') else 'INFO'
LOG_LEVEL = logging.DEBUG if LEVEL in ['DEBUG'] else logging.INFO
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)

BUCKET = os.environ.get('BUCKET')
TARGET_FOLDER = os.environ.get('TARGET_FOLDER', 'extracted-attachments')

SUBJECT = os.environ.get('SUBJECT')

def handler(event, _context):

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    s3 = boto3.client('s3')

    # Get s3 object contents based on bucket name and object key; in bytes and convert to string
    data = s3.get_object(Bucket=event['Records'][0]['s3']['bucket']['name'], Key=event['Records'][0]['s3']['object']['key'])
    contents = data['Body'].read().decode("utf-8")

    # Given the s3 object content is the SES email, get the message content and attachment using email package
    msg = email.message_from_string(contents)
    attachment = msg.get_payload()[1]
    if SUBJECT not in msg['subject'].lower():
        LOGGER.info(f'Email subject does not match expected: {msg["subject"]}')
        return  {
        'statusCode': 303,
        'body': f'Email subject does not match expected: {msg["subject"]}'
    }
    store_id = attachment.get_filename().split(".")[0]

    # Write the attachment to a temp location
    with open('/tmp/attach.csv', 'wb') as attachment_file:
        attachment_file.write(attachment.get_payload(decode=True))

    # Upload the file at the temp location to destination s3 bucket
    try:
        s3.upload_file('/tmp/attach.csv', BUCKET, f'{TARGET_FOLDER}/{timestamp}-{store_id}.csv')
        LOGGER.debug("File uploaded to S3")
    except FileNotFoundError:
        LOGGER.debug("The file was not found")

    output_filename = format_csv(attachment, timestamp)

    update_request_stock(output_filename)

    # Clean up the file from temp location
    os.remove('/tmp/attach.csv')

    return {
        'statusCode': 200,
        'body': 'SES Email received and processed'
    }


def format_csv(attachment, timestamp):
    output_filename = f'/tmp/{ENV}-{attachment.get_filename().split(".")[0]}-{timestamp}.csv'
    LOGGER.debug('Writing outfile')
    with open('/tmp/attach.csv', 'r', encoding='utf-16-le') as infile, open(output_filename, 'w', encoding="utf-8") as outfile:
        # Skip the second line, remove this if not needed for your use case
        outfile.write("product_id,stock_on_hand \n")

        lines = infile.readlines()[2:]

        for i, line in enumerate(lines):
            # Strip removes any spaces and newline characters from the ends
            stripped_line = line.strip()
            if stripped_line:  # Check if the line is not empty
                if stripped_line.find('affected') != -1:
                    continue
                # Replace tabs with commas and write to output file
                if stripped_line.split('\t')[1] == '.0000':
                    outfile.write(stripped_line.replace(
                        '\t', ',').replace('.0000', '0'))

                else:
                    outfile.write(stripped_line.replace(
                        '\t', ',').replace('.0000', ''))

                if int(i) != int(len(lines) - 3):
                    # Write a newline to go to the next row
                    outfile.write('\n')
    LOGGER.debug('Outfile written')
    return output_filename


def update_request_stock(output_filename):
    return True
