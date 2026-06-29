import time

from litellm.exceptions import RateLimitError, BadRequestError


RETRYABLE_ERRORS = (RateLimitError, BadRequestError)


def kickoff_with_retry(
    crew,
    max_retries=5,
    initial_wait=10,
):
    """
    Executes crew.kickoff() with automatic retry on transient LLM errors.
    """
    wait = initial_wait
    last_error = None

    for attempt in range(max_retries):
        try:
            print(f"\nAttempt {attempt + 1}/{max_retries}")
            result = crew.kickoff()
            print("Crew execution completed.")
            return result
        except RETRYABLE_ERRORS as error:
            last_error = error
            print(
                f"\nTransient LLM error: {type(error).__name__}"
                f"\nWaiting {wait} seconds before retry..."
            )
            time.sleep(wait)
            wait *= 2

    raise RuntimeError(
        f"Maximum retries exceeded. Last error: {last_error}"
    ) from last_error
