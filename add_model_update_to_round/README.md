# Add Model Update To Round

sam build
sam local generate-event s3 put --bucket model-bucket | sam local invoke AddModelUpdateToRoundFunction
