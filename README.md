# Agentic Loop
CrewAI via LiteLLM leverages LLMs in SAP Generative AI Hub

## LiteLLM
__SAP Gen AI Hub is now an official LLM provider for LiteLLM__

LiteLLM is an opensource library which supports 100+ LLMs from various providers.
With SAP’s opensource contribution to LiteLLM various LLM and agentic frameworks can be connected to SAP Gen AI Hub via LiteLLM.
The code examples are documented [here](https://sap-contributions.github.io/litellm-agentic-examples).
The agentic code examples are in this [repo](https://github.com/karimmohraz/crewai-litellm).

## Devtoberfest 2025 session
* [Connect to SA Generative AI Hub with LiteLLM](https://www.youtube.com/live/UZz6Eh2XOog)
* LiteLLM_Devtoberfest2025.pdf

## Setup
Install LiteLLM and CrewAI.
```
pip install litellm crewai
```

Note: The SAP contribution to LiteLLM will be available in November (announced at TechEd 2025)

### Prerequisites
* BTP Tenant
* SAP AI Cloud subscription

### Credentials
Provide SAP tenant's client_id, client_secret.

## CrewAI Script
```
python test_crew.py
```
