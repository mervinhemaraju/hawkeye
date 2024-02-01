
import boto3, json
import base64
from utils.constants import EXCEPTION_AWS_SECRETS

class SecretsManager:

    def __init__(self, secret_name) -> None:
        
        try:
            # Retrieve secrets
            get_secret_value_response = boto3.client('secretsmanager').get_secret_value(
                SecretId=secret_name
            )

            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                self.secrets = get_secret_value_response['SecretString']
            else:
                self.secrets = base64.b64decode(get_secret_value_response['SecretBinary'])

        except Exception as e:            
            # Raise an exception if any of the above operations fail
            raise Exception(EXCEPTION_AWS_SECRETS.format(str(e)))


    def require_secrets(self):
        # Return the secrets in a JSON format
        return json.loads(self.secrets)
    