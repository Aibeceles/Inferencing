"""
Utility functions for NeMo Curator Synthetic Data Generation notebooks.

This module contains shared helper functions used across multiple notebooks:
- generate_subtopics: Generate subtopics for a given macro topic
- generate_macro_topics: Generate broad macro topics
"""

from typing import List

from nemo_curator.synthetic import NemotronGenerator
from nemo_curator.synthetic.error import YamlConversionError
from nemo_curator.synthetic.prompts import DEFAULT_MACRO_TOPICS_PROMPT_TEMPLATE


def generate_subtopics(
    generator: NemotronGenerator,
    model: str,
    model_kwargs: dict,
    macro_topic: str,
    n_subtopics: int,
    prompt_template: str,
    n_retries: int = 5,
) -> List[str]:
    """
    Generates a list of subtopics for a given macro topic using a language model (LLM).

    This function interacts with the `generator` object to produce subtopics based on the provided
    macro topic and prompt template. If the YAML conversion fails, it retries the process up to
    `n_retries` times.

    Args:
        generator (NemotronGenerator): The generator instance used for LLM interaction.
        model (str): The name or identifier of the language model to use.
        model_kwargs (dict): A dictionary of additional configuration parameters for the language model.
        macro_topic (str): The macro topic for which subtopics will be generated.
        n_subtopics (int): The number of subtopics to generate.
        prompt_template (str): The prompt template used to guide the LLM in generating subtopics.
        n_retries (int, optional): The maximum number of retry attempts if YAML conversion fails. Defaults to 5.

    Returns:
        List[str]: A list of generated subtopics as strings. If all retries fail, returns an empty list.

    Raises:
        YamlConversionError: If YAML conversion fails after all retry attempts.
    """
    # Initialize an empty list to store generated subtopics
    subtopics = []

    # Retry loop to handle potential YAML conversion errors
    for _ in range(n_retries):
        try:
            # Generate a response from the language model using the specified parameters
            llm_response = generator.generate_subtopics(
                model=model,
                model_kwargs=model_kwargs,
                macro_topic=macro_topic,
                n_subtopics=n_subtopics,
                prompt_template=prompt_template,
            )

            # Convert the first response from the LLM into a YAML-formatted list of subtopics
            subtopics = generator.convert_response_to_yaml_list(
                llm_response=llm_response[0], model=model
            )

            # Exit the retry loop if conversion is successful
            break
        except YamlConversionError as e:
            # Print an error message and retry if YAML conversion fails
            print(f"Hit: {e}, Retrying...")

    # Return the generated list of subtopics (or an empty list if all retries failed)
    return subtopics


def generate_macro_topics(
    generator: NemotronGenerator,
    model: str,
    model_kwargs: dict,
    n_macro_topics: int,
    prompt_template: str = DEFAULT_MACRO_TOPICS_PROMPT_TEMPLATE,
    n_retries: int = 5,
) -> List[str]:
    """
    Generates a list of macro topics using a language model and retries on YAML conversion errors.

    This method leverages a `NemotronGenerator` instance to generate macro topics by invoking a
    language model (LLM). It processes the LLM's response, converts it into a YAML-formatted list,
    and retries the process up to `n_retries` times if a `YamlConversionError` occurs.

    Args:
        generator (NemotronGenerator): An instance of the `NemotronGenerator` class responsible for
            generating and processing LLM responses.
        model (str): The name or identifier of the language model to be used for generating macro topics.
        model_kwargs (dict): A dictionary of additional keyword arguments to configure the language model.
        n_macro_topics (int): The number of macro topics to generate.
        prompt_template (str, optional): A string template used to construct the prompt for the LLM.
            Defaults to `DEFAULT_MACRO_TOPICS_PROMPT_TEMPLATE`.
        n_retries (int, optional): The maximum number of retry attempts in case of a `YamlConversionError`.
            Defaults to 5.

    Returns:
        List[str]: A list of generated macro topics as strings.

    Raises:
        YamlConversionError: If all retry attempts fail due to YAML conversion issues.
    """
    # Initialize an empty list to store the generated macro topics
    macro_topics = []

    # Attempt to generate and convert macro topics up to `n_retries` times
    for _ in range(n_retries):
        try:
            # Generate a response from the language model using the specified parameters
            llm_response = generator.generate_macro_topics(
                n_macro_topics=n_macro_topics,
                model=model,
                model_kwargs=model_kwargs,
                prompt_template=prompt_template,
            )

            # Convert the first response from the LLM into a YAML-formatted list of topics
            macro_topics = generator.convert_response_to_yaml_list(
                llm_response=llm_response[0], model=model, model_kwargs=model_kwargs
            )

            # Break out of the retry loop if conversion is successful
            break
        except YamlConversionError as e:
            # Print an error message and retry if YAML conversion fails
            print(f"Hit: {e}, Retrying...")

    # Return the generated list of macro topics (empty if all retries failed)
    return macro_topics

