import re

PII_PATTERNS = {
    "full_name": r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.\w+\b",
    "phone_number": r"\b(?:\+91[-\s]?|0)?[6-9]\d{9}\b",
    "dob": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    "aadhar_num": r"\b\d{4} \d{4} \d{4}\b",
    "credit_debit_no": r"\b(?:\d{4}[- ]?){3}\d{4}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/\d{2,4}\b"
}

def mask_entities(text):
    masked_text = text
    entities = []

    for label, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, masked_text):
            entity = match.group()
            start, end = match.span()
            entities.append({
                "position": [start, end],
                "classification": label,
                "entity": entity
            })
            masked_text = masked_text.replace(entity, f"[{label}]")

    return masked_text, entities
