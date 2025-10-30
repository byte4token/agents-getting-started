import sys

print(f'Using Python {sys.version}')
if sys.version_info < (3, 10):
    raise RuntimeError('PyRIT requires Python 3.10 or later.')


from dotenv import load_dotenv
load_dotenv()

import os
from pprint import pprint

project_endpoint = os.environ.get('AIPROJECT_CONNECTION_STRING')

if project_endpoint:
    azure_ai_project = project_endpoint
    print('Using Azure AI project endpoint:')
    print(azure_ai_project)
else:
    required_vars = ['AZURE_SUBSCRIPTION_ID', 'AZURE_RESOURCE_GROUP', 'AZURE_PROJECT_NAME']
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        raise RuntimeError(
            'Missing required environment variables: ' + ', '.join(missing) +
            '. Set them or define AZURE_AI_PROJECT before continuing.'
        )
    azure_ai_project = {
        'subscription_id': os.environ['AZURE_SUBSCRIPTION_ID'],
        'resource_group_name': os.environ['AZURE_RESOURCE_GROUP'],
        'project_name': os.environ['AZURE_PROJECT_NAME'],
    }
    print('Using Azure AI project configuration:')
    pprint(azure_ai_project)


from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy

credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
red_team_agent = RedTeam(
    azure_ai_project=azure_ai_project,
    credential=credential,
)

print("Available risk categories:")

def simple_callback(query: str) -> str:
    """Return a templated refusal response for every prompt."""
    return (
        "I'm an AI assistant that follows ethical guidelines. "
        "I cannot provide harmful content."
    )

red_team_result = red_team_agent.scan(
    target=simple_callback,
    scan_name='Local-Simple-Callback-Scan',
    output_path='My-First-RedTeam-Scan.json',
)


print('Red Team agent created. Ready to run scans.')
