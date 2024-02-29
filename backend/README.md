# Backend 
Welcome to the Expo Backend. This will be very similar to [portal](https://github.com/bitcamp/portal), but with some differences. 

## Differences
- Node18 instead of Node12
- No split between dev, stg, prd; will only be dev and prd
- Fewer things to do (not as complex of a project)

## Purpose
- Parses devpost submission and creates scheduling for projects based on environment variables
- Uploads schedule to database (guessing DynamoDB for now, but will update) (POST)
- Creates API endpoint to return the schedule for the frontend to consume (GET)
  - (Optional) Create API to see a specific team's submission (GET)

# Technology
We will be using the [Serverless Framework](https://www.serverless.com/), which is essentially an abstraction of AWS, making the creation of services (like Lambda)
easier and more straightforward. It lacks some granularity but is good enough for our purposes.

We will be using **serverless framework v3**. This is the only version compatible with Node18. 

The overall architecture looks like:
- Deploy to Serverless which creates AWS resources
- Lambda handles the API calls
- Lambda uses DynamoDB to read or write relevant data and returns it
- Some frontend hosting site (Netlify, Amplify, only directors worry about this) will consume the API using the relevant endpoints

## Description + File Organization
- `serverless.yml`: controls the stack that will be deployed to AWS. It's a declaration file that creates the resources and allocates the specifics
in order for the apps to run. Once deployed, you can see the resources in the Serverless (SLS) [dashboard](https://app.serverless.com/). 
  - In more detail (if you are interested), it will create a CloudFormation stack managed by Serverless and is automatically created. SLS is connected to our AWS account via an IAM role that provides it the permissions to modify and create resources.
- `config`: Controls environment variables for `serverless.yml` to consume. This allows us to dynamically set resource names when using the deploy command (below)


# Relevant commands
## Installation
Based on whether we end up using Python or JS, we will need to install dependencies. This includes the AWS SDKs in order to call AWS resources. 

For JS/TS, we can simply use `package.json` and `package-lock.json` as normal. For Python3, SLS allows us to use an `aws_requirements.txt` file when deploying
to Lambda. Make sure you have Python3 (preferably 3.6+) with supported pip version. 

With JS/TS, we will be using `aws-sdk` version 3. This is a much more robust and granular implementation compared to sdk-v2. Check resources for differences.

**If using Python, you must write your code in a virtual environment.** There are a lot of options, including `venv`, `pyenv`, `conda`, and more.
For first time users, I recommend [`venv`](https://docs.python.org/3/tutorial/venv.html). **Please ask the directors if you are unsure how to setup 
a virtual environment!!**

```bash
# Python (for running locally)
pip install -r aws_requirements.txt

# Python (for installing packages)
pip install $(package_name)
# ADD the package name to aws_requirements.txt
pip install pipreqs
pipreqs --savepath aws_requirements.txt # Add --force if it doesn't let you

# Python (before deployment). `basepath` should be wherever the files are. They can be in `backend/src` or just the `backend` folder. 
pip install -t $(basepath)/vendor -r aws_requirements.txt

# JavaScript (so much simpler)
npm install # OR npm i

# JavaScript (installing packages). Do it in the `backend` folder. 
npm install $(package)
```

[SLS Python Resource](https://www.serverless.com/blog/handling-aws-lambda-python-dependencies)

## Using `serverless`/`sls`

Here are the commands that actually builds the resources and deploys them. This should only be done **once you are ready to deploy and test changes.** 
It's not for commit purposes like `git`. 

```bash
# Installation (use serverless@latest or serverless@3 to specify)
npm install -g serverless

# Deploy to AWS. Stage can be `dev` or `prd`
sls deploy -s $(stage)
```
> Use `-g` global tag when installing serverless because you want it to be a command you can use anywhere, not just in your folder.

# Testing

Make sure you populate the parameters when testing using the Console

## Simple Lambda Testing
You can always test your lambda functions in the console. For now, assume our stack is called `expo-backend`. 

Find the `expo-backend` resource in CloudFormation in the AWS console. Click on it and go to the "Resources" tab. Filter the resources for the function
you are looking for. Click on that. In the Lambda Dashboard of this function, feel free to test. Editing the Lambda function and deploying **DOES NOT DO ANYTHING**
as it was created by a CloudFormation stack. You have to redeploy using the `sls` command, unfortunately. 

## More Rigorous API Gateway testing
API gateway is AWS resource that controls the API calls that invoke the Lambda functions. You should find the appropriate API gateway stack (`expo-backend` or something)
and click on it. Click the appropriate URL API endpoint on the left and click on the right one (POST, GET, etc.). Click on the endpoint and click the 
"Test" tab all the way on the right. This will test the endpoint as well as your Lambda functions.

# Resources
- Serverless config + docs: https://www.serverless.com/framework/docs/providers/aws/guide/serverless.yml
- Serverless Python: https://www.serverless.com/blog/handling-aws-lambda-python-dependencies
- Pipreq for python dependencies: https://pypi.org/project/pipreqs/
- Virtual environments: https://realpython.com/python-virtual-environments-a-primer/
  - https://docs.python.org/3/tutorial/venv.html
- API Gateway + Lambda: https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-with-lambda-integration.html
- AWS SDKv2 vs SDKv3: https://dev.to/dvddpl/aws-sdk-v2-or-v3-which-one-should-you-use-3kaj

