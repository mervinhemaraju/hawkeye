##########################################
################## DATA ##################
##########################################
AWS_ACCOUNT_MATCHER = {
    "xxxx": "QA",
    "xxxxx": "Dev",
    "xxxxxx": "IAM",
    "xxxxxxx": "Sbox",
    "xxxxxxxx": "Prod",
    "xxxxxxxxx": "Mgmt",
    "xxxxxxxxxx": "Security",
    "xxxxxxxxxxx": "Playground",
    "xxxxxxxxxxxx": "Prod-Legacy",
    "xxxxxxxxxxxxx": "Web",
}

# AWS_SERVICE_ACTIONS_KEYWORDS_FILTERING = {
#     "EC2": [
#         "SecurityGroup", "Vpc"
#     ]
# }

############################################
################## VALUES ##################
############################################
VALUE_PLACEHOLDER_UNKNOWN = "Unknown"
VALUE_COLOR_MODIFICATION = "#6f42f5"
VALUE_COLOR_CREATION = "#4287f5"
VALUE_COLOR_DELETION = "#87004a"
VALUE_COLOR_NEGATIVE = "#e57373"

VALUE_AWS_SECRET_MANAGER_NAME = "sysops/{}/hawkeye"


#########################################
########### EXCEPTION MESSAGES ##########
#########################################

EXCEPTION_GENERAL = "An error occurred."
EXCEPTION_AWS_SECRETS = "An error occurred while retrieving the AWS Secrets: {}"
