# RAG with AWS Bedrock and Streamlit

Use this solution to quickly and inexpensively begin prototyping and vetting business use cases for GenAI using a custom corpus of knowledge with Retrieval Augmented Generation (RAG) in a low-code Streamlit application.

This solution contains a backend application which uses LangChain to provide PDF data as embeddings to your choice of text-gen foundational model via Amazon Web Services (AWS) new, managed LLM-provider service, Amazon Bedrock and your choice of vector database with FAISS or a Kendra Index.

The only cost-generating AWS service this solution uses is Amazon Bedrock.


## What You'll Build


## Prerequisites

You'll need to install all prerequisites on your local operating machine.

    
For the app, you'll need to have:
1. [Python 3.8 or higher](https://www.python.org/downloads/macos/)
2. Set up the SDK for Python (Boto3) and AWS CLI
    - Boto3 & Botocore: `pip3 install ./backend/boto3-1.26.162-py3-none-any.whl ./backend/botocore-1.29.162-py3-none-any.whl`
    - AWS CLI: [Instructions Here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
3. Install the requirements using the requirements file with `pip3 install -r ./requirements.txt`


## IAM Permission

Your backend will need permissions to call the Bedrock API. More specifically, it should have least privileged access to Invoke foundational models in Bedrock. To do this, you'll need to create an IAM user with the appropriate permissions, then generate access keys (cli credentials). Complete documentation of Bedrock IAM Reference configurations [found here.](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html)

1. From the IAM console, perform the following steps:
2. Select the IAM Group associated with your user.
3. Click on "Add Permissions" and choose "Create Inline Policies" from the dropdown list.
4. Create a new inline policy and include the following permissions:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "*"
    }
  ]
}
```
Please note : When creating this IAM role, follow the best practice of granting [least privileged access.](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege)

6. Create programmatic access keys/CLI credentials.
7. Run `aws configure --profile <name_of_profile>'
7. include the name of your AWS CLI Profile you configured in backend code.
   


## How to Run

1. In one terminal session, execute 'streamlit run ./frontend/app.py'


## How to Use

Once you confirm that the app(s) are running, you can begin prototyping. 


### Add Your Own Corpus for RAG Embeddings 

you can add your own pdf files.
 
#for deployment need to attach the Bedrock Ploicy Role to the EC2 instance


### Prompt Engineering with LangChain

Foundational Models are trained in specific ways to interact with prompts. Check out the [Claude Documentation Page](https://docs.anthropic.com/claude/docs) to learn best practices and find examples of pre-engineered prompts.



