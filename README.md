# About 🔍

BirdiDQ is an intuitive and user-friendly data quality application that allows you to run data quality checks on top of python great expectation open source library using natural language queries. Type in your requests, and BirdiDQ will generate the appropriate GE method, run the quality control and return the results along with data docs you need. 

# Note 
BirdiDQ is under development and is an open source project. Contributions are welcomed!
## Features

- **🔍 Data Exploration Made Easy:** Quickly and interactively explore your data using a range of features like filters, comparisons, and more. Uncover hidden insights and make informed decisions with confidence.
- **🎯 Natural Language Processing:**: Speak BirdiDQ's language! No technical expertise required. Simply type in your queries, and BirdiDQ intelligently converts them into powerful Great Expectations methods (using a fine-tuned Large Language Model), saving you time and effort..
- **⚡ Instant Results**: Run comprehensive data quality checks on your selected data sources, and get instant feedback on data inconsistencies. BirdiDQ ensures that your data is reliable and trustworthy.
- **📧Automate Email Alert**: Reach out to the Data Owner directly through the app, sending them an email with the detailed data quality report generated by Great Expectations.
- **GEN AI models**: Uses finetuned LLM on customed expectations data.

## Tech Stack
This app is an LLM-powered app built using:
- **[Streamlit](https://streamlit.io/)**
- **[Great Expectations](https://github.com/Soulter/hugging-chat-api)**
- **Finetuned LLMs**:
    - **[Falcon-7B parameters causal decoder-only model](https://huggingface.co/tiiuae/falcon-7b)**: The model is finetuned on custom data with **Qlora** approach.
    - **[OpenAI GPT-3](https://platform.openai.com/docs/guides/fine-tuning)**: Also finetuned on the same data
- **Note**: The finetuned GPT-3 model seems to perform better for now.
## Queries example

Here are some example queries you can try with BirdiDQ:

- Ensure that at least 80% of the values in the country column are not null.
- Check that none of the values in the address column match the pattern for an address starting with a digit.
