# Tool Calling v/s Process Calling - Data Hack Summit'25

This repository contains the demo showcased during the hack session - "Building Fast & Accurate Conversational Agents: Beyond Function Calling"

## Setting up the repository

1. Once you have cloned the repository, create a new virtual environment with conda (anaconda / miniconda) - 

```shell
conda create -n "data_hack" -m "python==3.11"
conda activate data_hack
```

2. Install `uv` for fast dependency resolution -

```shell
pip install uv
```

3. Install all the required dependencies

```
uv pip install openai==1.68.2
uv pip install rasa-pro==3.13.7
uv pip install jupyter==1.0.0
```

## Tool calling demo

The purpose of this demo is to showcase how tool calling is a problematic approach when you want to build customer facing 
conversational agents. It's deep rooted in how tools are supposed to be atomic and stateless while conversational agents
where an LLM is figuring out the right sequence of tools to call needs state and context.

To run the demo - 

1. Ensure you have access to an API key for the OpenAI platform. Set it as an env var

```shell
export OPENAI_API_KEY=<your-api-key>
```

2. Run the jupyter notebook server

```shell
jupyter notebook
```

3. Open the demo notebook - `Tool calling demo.ipynb`

The demo implements a conversational agent that helps users with flight booking tasks, for e.g. booking a new flight or cancelling an existing booking.

In order to see the flakiness of tool calling, try the following conversation - 

```
User: cancel my flight booking

Agent: To assist you with canceling your flight booking, I'll need the following information:

1. Your booking reference code.
2. The last name of the passenger on the booking.

Please provide these details so I can proceed with the cancellation process.

User: CONF12345

Agent: Please provide the last name of the passenger on the booking with reference code CONF12345 so I can proceed with the cancellation process.

User: Smith

Agent: Here are the details of your booking:

- **Flight:** AA101
- **Route:** NYC to PAR
- **Date & Time:** September 15, 2025, at 08:00
- **Fare Class:** Economy
- **Airline:** Delta
- **Passenger:** John Smith
- **Total Paid:** $650.00
- **Payment Method:** Visa ending in 9012

Would you like to proceed with the cancellation of this booking?

User: yeah okay

Agent: The cancellation fee for your booking is $200. The refund amount will be $450.00. 

Would you like to receive the refund to your original payment method, or would you prefer a refund in points with a 5% penalty reduction? Please confirm your choice so I can proceed.
```

The issue in the above conversation is that the agent was explicitly told in the LLM's prompt to double check the membership tier of the customer before calculating the cancellation fees. But
because it missed to do so, it incorrectly calculates the cancellation fee.

Follow along in the demo, to see how this ends up being a game of 'prompt and pray' in order to get some reliability with this approach.


## Process Calling Demo

Process calling is an approach where state and context is added to conversational agents while being able to use
atomic tools. You can read more about it from [rasa's blog post](https://rasa.com/blog/process-calling-agentic-tools-need-state/)

### Setting up the demo

1. Ensure you have setup the repository with all dependencies installed as explained in [this section](#setting-up-the-repository)

2. Fetch your free [Rasa Pro Developer Edition license key](https://rasa.com/rasa-pro-developer-edition-license-key-request/)

### Running the demo

1. Set your rasa pro developer edition license key to an env var - 

```shell
export RASA_PRO_LICENSE=<your-rasa-pro-license>
```

2. Ensure you have access to an API key for the OpenAI platform. Set it as an env var -

```shell
export OPENAI_API_KEY=<your-api-key>
```

3. Navigate to the assistant directory - 

```
cd calm/
```

4. Train the assistant - 

```
rasa train
```

5. Talk to the assistant - 

```
rasa inspect
```

You should be able to have a conversation similar to this - 

https://github.com/user-attachments/assets/b7ec7ef3-957d-410d-aef5-9d628410be4f


