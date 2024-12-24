from loguru import logger
from typing_extensions import Annotated
from zenml import get_step_context, step

from llm_engineering.application import utils
from llm_engineering.domain.documents import UserDocument

# Define the function’s signature
@step
def get_or_create_user(user_full_name: str) -> Annotated[UserDocument,
"user"]:
    logger.info(f"Getting or creating user: {user_full_name}")
    first_name, last_name = utils.split_user_full_name(user_full_name)

    # Try to retrieve the user from the database or create a new one if it doesn’t exist.
    user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)

    #retrieve the current step context and add metadata about the user to the output
    step_context = get_step_context()
    step_context.add_output_metadata(output_name="user", metadata=_get_metadata(user_full_name, user))
    return user

# Helper function which builds a dictionary containing the query parameters
# and the retrieved user information, which will be added as 
# metadata to the user artifact
def _get_metadata(user_full_name: str, user: UserDocument) -> dict:
    return {
"query": {
"user_full_name": user_full_name,
},
"retrieved": {
"user_id": str(user.id),
"first_name": user.first_name,
"last_name": user.last_name,
},
}