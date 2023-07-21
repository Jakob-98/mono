# Python Wrapper for OpenAI GPT Functions PoC

This repository contains a proof of concept (PoC) experiment aimed at illustrating a method to simplify the usage of OpenAI GPT Functions in Python. Our approach involves wrapping existing Python functions to generate metadata for OpenAI GPT functions automatically. 

The repository contains two contrasting examples - a naive approach and our proposed wrapper-based solution.

## Project Structure

Inside the `experiments` folder, you will find two different approaches.

1. The naive approach is where you manually define the JSON specification for the function.

2. The proposed wrapper approach where you use the provided decorator `@function_metadata_decorator` to define your function and generate metadata automatically.

The `func_json_extractor.py` and `openai_service.py`` provide the relevant code to try it yourself.

## How to Use

In the naive approach:

```python
def get_current_weather(location, unit="fahrenheit"):
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]

...
```

In the wrapper approach:

```python
@function_metadata_decorator
def get_current_weather(location, unit="fahrenheit"):
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

functions = [
    get_current_weather.metadata
]
```

The wrapper approach allows you to directly retrieve the function metadata via `myfunc.metadata`.

Example with existing library (Pandas):

```python
import pandas as pd

# load example df raw github
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv") 

function_specs = [
    FunctionSpec(
        func_ref=df.head,
        parameters=extract_function_metadata(df.head)
    ),
    FunctionSpec(
        func_ref=df.tail,
        parameters=extract_function_metadata(df.tail)
    ),
    FunctionSpec(
        func_ref=df.describe,
        parameters=extract_function_metadata(df.describe)
    )
]

openai.api_key = os.environ["OPENAI_API_KEY"]

openai_service = OpenAIService(openai, function_specs=function_specs)

messages = [
    {"role": "user", "content": "What's the head of the dataframe?"}
]

response = openai_service.call_function(messages)
print(response)
```

**Note:** certain functions will not work, e.g. numpy.log, which is built in c. We cannot use inspect.signature for these functions. Instead, we could opt to use `somefunc.types` to infer the types, but this is out of scope for the PoC.
