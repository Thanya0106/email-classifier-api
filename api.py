from fastapi import FastAPI
from pydantic import BaseModel
from pii_masker import mask_entities
from classifier import classify_email

app = FastAPI()

class EmailInput(BaseModel):
    input_email_body: str

@app.post("/classify")
def classify(request: EmailInput):
    original = request.input_email_body
    masked, entities = mask_entities(original)
    category = classify_email(masked)

    return {
        "input_email_body": original,
        "list_of_masked_entities": entities,
        "masked_email": masked,
        "category_of_the_email": category
    }
