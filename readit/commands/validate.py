import requests

# Performs validation of URL
# If URL is valid, returns True
# If URL is invalid, returns False, with error message
# If URL is invalid add tags ERROR, ERROR_TYPE to URL in database
# If URL is not provided, returns False, with error message


def validate_url(url):
    response = requests.get(url)
    status_code = response.status_code

    error_messages = {
        404: "URL not found",
        403: "Access forbidden",
        500: "Internal server error",
    }

    error_message = error_messages.get(status_code, "An error occurred")

    return status_code, error_message
