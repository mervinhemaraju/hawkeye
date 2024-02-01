import requests, json, logging, os, boto3
from datetime import datetime
from utils.constants import *
from utils.slack_builder import *
from models.secrets_manager import SecretsManager

##################################
##### GLOBAL INITIALIZATIONS #####
##################################
# Initialize Logging
logging.getLogger().setLevel(logging.INFO)


###############################
########## FUNCTIONS ##########
###############################
def post_to_slack(message, slack_hook, blocks=None):
    return requests.post(
        slack_hook,
        json.dumps({
            'text': message,
            'attachments': blocks
        })
    )


def main(event, context):

    # Try except clause to
    # handle all possible errors in the whole script
    # to prevent crash
    try:

        # Log on Cloudwatch
        logging.info(f"Event obtained: {event}")
        
        # Initialize secrets
        secrets = SecretsManager(
            secret_name=VALUE_AWS_SECRET_MANAGER_NAME.format(os.environ["AWS_ACCOUNT"])
        ).require_secrets()

        # * Get all the details need here
        account_originated = event['account'] if 'account' in event else VALUE_PLACEHOLDER_UNKNOWN
        acccount_region = event['region'] if 'region' in event else VALUE_PLACEHOLDER_UNKNOWN
        time_of_action = event['time'] if 'time' in event else VALUE_PLACEHOLDER_UNKNOWN
        username = VALUE_PLACEHOLDER_UNKNOWN
        user = VALUE_PLACEHOLDER_UNKNOWN
        event_source = VALUE_PLACEHOLDER_UNKNOWN
        event_name = VALUE_PLACEHOLDER_UNKNOWN
        parameters_of_request = VALUE_PLACEHOLDER_UNKNOWN
        outcome_of_request = VALUE_PLACEHOLDER_UNKNOWN

        if 'detail' in event:

            username = event['detail']['userIdentity']['sessionContext']['sessionIssuer']['userName'] if 'userIdentity' in event['detail'] and 'sessionContext' in event[
                'detail']['userIdentity'] and 'sessionIssuer' in event['detail']['userIdentity']['sessionContext'] else VALUE_PLACEHOLDER_UNKNOWN
            user = event['detail']['userIdentity']['arn'] if 'userIdentity' in event[
                'detail'] and 'arn' in event['detail']['userIdentity'] else VALUE_PLACEHOLDER_UNKNOWN
            event_source = event['detail']['eventSource'] if 'eventSource' in event['detail'] else VALUE_PLACEHOLDER_UNKNOWN
            event_name = event['detail']['eventName'] if 'eventName' in event['detail'] else VALUE_PLACEHOLDER_UNKNOWN
            outcome_of_request = event['detail']['responseElements'] if 'responseElements' in event['detail'] else VALUE_PLACEHOLDER_UNKNOWN
            parameters_of_request = event['detail']['requestParameters'] if 'requestParameters' in event['detail'] else VALUE_PLACEHOLDER_UNKNOWN
            
        # Sanitization process
        account_originated = AWS_ACCOUNT_MATCHER[account_originated] if account_originated in AWS_ACCOUNT_MATCHER else account_originated
        user = (user.rsplit('/', 1))[1] if '/' in user else user
        event_source = (event_source.split('.'))[0].upper() if '.' in event_source else event_source
        time_of_action = datetime.strptime(time_of_action, '%Y-%m-%dT%H:%M:%SZ').strftime("%d-%m-%Y, %I:%M:%S %p")

        # Verify if filtering of keywords is needed
        # if event_source in AWS_SERVICE_ACTIONS_KEYWORDS_FILTERING:

        #     # Filter all event name that matches the keyword
        #     keyword_match = [keyword for keyword in AWS_SERVICE_ACTIONS_KEYWORDS_FILTERING[event_source] if keyword in event_name]

        #     # Verify if atleast one match occurred.
        #     if len(keyword_match) == 0:
        #         # Log to Cloudwatch
        #         logging.info("Filtering denied this event.")
        #         return

        # Determine block color
        creation = [keyword for keyword in ["create", "creation," "put", "add"] if keyword in event_name.lower()]
        deletion = [keyword for keyword in ["delete", "remove", "terminate", "deletion"] if keyword in event_name.lower()]
        
        # Generate the report of the variables below
        logging.info(f"Generating Report...")
        logging.info(f"Account: {account_originated}")
        logging.info(f"Region: {acccount_region}")
        logging.info(f"Time: {time_of_action}")
        logging.info(f"Username: {username}")
        logging.info(f"User: {user}")
        logging.info(f"AWS Service: {event_source}")
        logging.info(f"Action Performed: {event_name}")
        logging.info(f"Outcome of Request: {str(outcome_of_request)}")

        # Create a slack block
        block = block_report(
            account_originated=account_originated,
            acccount_region=acccount_region,
            time_of_action=time_of_action,
            username=username,
            user=user,
            event_source=event_source,
            event_name=event_name,
            parameters_request=parameters_of_request,
            outcome_of_request=outcome_of_request,
            color=VALUE_COLOR_CREATION if len(creation) > 0 else VALUE_COLOR_DELETION if len(deletion) > 0 else VALUE_COLOR_MODIFICATION
        )

        # Post to Slack
        logging.info(f"Posting to Slack...")

        # Post to Slack
        post_to_slack(
            message=None,
            slack_hook=secrets['slack_webhook'],
            blocks=block
        )

    except Exception as e:

        # Log on Cloudwatch
        logging.error(f"{EXCEPTION_GENERAL} {e}")

        # Create a slack block
        block = block_error(
            aws_account=os.environ['AWS_ACCOUNT'], error_message=str(e))

        # Post to Slack
        post_to_slack(
            message="<!here>",
            slack_hook=secrets['slack_webhook'],
            blocks=block
        )
