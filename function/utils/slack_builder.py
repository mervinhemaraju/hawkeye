from utils.constants import *

def block_error(aws_account, error_message):  
    
    return [{
        "color": VALUE_COLOR_NEGATIVE,
        "blocks":  [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": EXCEPTION_GENERAL,
                    "emoji": False
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*AWS Account:*\n{aws_account}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Error Message:*\n{error_message}"
                    }
                ]
            }
        ]
    }]
    
def block_report(
    account_originated, 
    acccount_region,
    time_of_action,
    username,
    user,
    event_source,
    event_name,
    parameters_request,
    outcome_of_request,
    color=VALUE_COLOR_MODIFICATION
):
    pr = ""
    
    if parameters_request != None:
        
        for key,value in parameters_request.items():
            pr = pr + f"{key.capitalize()}: {value}\n"
            
    oor = ""
    
    if outcome_of_request != None:
        
        for key,value in outcome_of_request.items():
            oor = oor + f"{key.capitalize()}: {value}\n"
    
    return [{
        "color": color,
        "blocks":  [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"An event has been captured on {account_originated} under region {acccount_region}",
                    "emoji": False
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*User:*\n{user}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*User Role Involved:*\n{username}"
                    },
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Event Name:*\n{event_name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Event Source:*\n{event_source}"
                    },
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Time of Action:*\n{time_of_action}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Parameters of Request:*\n```{pr}```"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Outcome of Request:*\n```{oor}```"
                    }
                ]
            },
        ]
    }]