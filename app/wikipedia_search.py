import wikipedia
from unstructured_client import UnstructuredClient
from unstructured_client.models import operations, shared
import json
import requests

def search_wikipedia(query):
    try:
        page = wikipedia.page(query)
        content = page.content
        """
        client = UnstructuredClient(
            api_key_auth="iY4xDUJec73Lfj0tmZGoW7pyEe5N5K",
            server_url="https://api.unstructuredapp.io",
        )

        files = shared.Files(
            content=content.encode(),
            file_name=f"{page.title}.txt",
        )

        req = operations.PartitionRequest(
            shared.PartitionParameters(files=files, strategy=shared.Strategy.AUTO)
        )

        try:
            resp = client.general.partition(req)
            unstructured_content = json.dumps(resp.elements, indent=2)
        except Exception as e:
            unstructured_content = f"Error in Unstructured API: {str(e)}"

        # Combine Wikipedia content with unstructured content
        combined_content = f"Wikipedia Content:\n{content}\n\nUnstructured Content:\n{unstructured_content}"
        """
        return content 
    except wikipedia.exceptions.DisambiguationError as e:
        return search_wikipedia(e.options[0])
    except wikipedia.exceptions.PageError:
        return "Page not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"
