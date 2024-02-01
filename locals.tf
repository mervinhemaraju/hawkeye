locals {
  tags = {
    owner = "SysOps"
    team  = "SysOps"
  }

  constants = {

    datasources = {
      LAYER_LIBRARY_REQUESTS = "requests"
    }

    lambda = {
      RETRIES_ATTEMPT = 0
      TIMEOUT         = "120"
      HANDLER         = "main.main"
      VERSION         = "python3.9"
      TRUSTED_ENTITIES = [
        {
          type = "Service",
          identifiers = [
            "lambda.amazonaws.com"
          ]
        }
      ]
    }

  }
}
