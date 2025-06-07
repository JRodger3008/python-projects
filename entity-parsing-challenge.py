"""
Extracts Entities from Text using the Regular Expression ('re') Module.

'Entity' in computing is a distinct, identifiable piece of information, and
something that can be extracted and classified.

I asked Claude (AI) to set me a project that would best help me learn the 're' module 
in Python, I was given the text and 10 entity types to parse from it:
    - Email addresses: Contact entity
    - Phone numbers (various formats): Contact entity
    - Dates (US and UK-style): Temporal entity
    - URLs (http, https, and ftp protocols): Location and Organisation entities
    - Invoice/Ticket/Order numbers: Identifier entity
    - Currency amounts (£ and $): Financial entity
    - Credit card numbers (16-digit): Financial entity
    - Social Security Number (SSN): Identifier entity
    - IP addresses: Identifier entity
    - Names (First & Last names): Person entity

Note: I added some additional entity formats to test myself (e.g., UK-International Phone Number).

Primary resources used:
https://docs.python.org/3/library/re.html 
https://media.datacamp.com/legacy/image/upload/v1665049611/Marketing/Blog/Regular_Expressions_Cheat_Sheet.pdf

Author: Jordan Rodger
Created: 05/06/2025 Last Edit: 07/06/2025
"""

import re # Regular Expression

text = """
Contact Sarah Johnson at sarah.johnson@techcorp.com or call (555) 123-4567. 
Meeting scheduled for 2024-03-15 at 2:30 PM EST. Invoice #INV-2024-001 
for $1,250.75 is due. Alternative contact: Mike Davis at +1-800-555-0199 or 
mike.davis@company.org. Visit our website at https://www.techcorp.com 
or ftp://files.techcorp.com/docs. Reference ticket #TK-9876 and 
order #ORD-ABC-123. Payment via credit card 4532-1234-5678-9012 
or wire transfer to account 987-654-3210. Social Security Number 
123-45-6789 on file. IP address 192.168.1.100, and 192.168.1.1 flagged. 
Additional phone numbers: 555.987.6543, (+44)7912991234 and (800)CALL-NOW.
Sub-totals: £3,000.80 and $2,100. Website: http://techcorp.com.
Today's date is 06/06/2025.
"""


def extract_entities(text):
    """
    Extract various entity types from text using regular expressions (patterns).

    Parses the input text to identify, and extract different entity types including
    email addresses, phone numbers, dates, URLs, invoice numbers, currency amounts,
    credit card numbers, account numbers, SSNs, IP addresses, and full names.
    This is essentially a manual form of 'Named Entity Recognition' (NER) used in 
    Natural Language Processing (NLP).
    
    Args:
        text (str): The text excerpt to extract information from.
    Returns:
        entities (dict): A dictionary where keys are entity types (str) and values
        are lists of matched strings.
    """
    entities = {}

    # Match standard email formats.
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.]+"

    # Phone numbers (US, UK-International, and alphanumeric formats).
    ppattern1 = r"\(\d{3}\)\s?\d{3}-\d{4}"  # (555) 123-4567
    ppattern2 = r"\+1-\d{3}-\d{3}-\d{4}"    # +1-800-555-0199
    ppattern3 = r"\d{3}\.\d{3}\.\d{4}"      # 555.987.6543
    ppattern4 = r"\(\d{3}\)[a-zA-Z\-]{4,}"  # (800)CALL-NOW
    ppattern5 = r"\(\+\d{2}\)\d{10}"        # (+44)7912991234
    phone_pattern = f"{ppattern1}|{ppattern2}|{ppattern3}|{ppattern4}|{ppattern5}"

    # Match dates in YYYY-MM-DD and DD/MM/YYYY formats.
    date_pattern = r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}"
    
    # Match URLs with http, https, and ftp protocols.
    url_pattern = r"(?:https?|ftp)://[^\s/$.?#].[^\s]*"

    # Match invoice, ticket, and order numbers (e.g., #INV-2024-001).
    inv_pattern = r"#(?:INV|TK|ORD)-[A-Z0-9\-]+"

    # Match currency values with optional commas and decimal place.
    currency_pattern = r"[$£]\d{1,3}(?:,\d{3})*(?:\.\d{2})?"

    # Match 16-digit card numbers formatted as XXXX-XXXX-XXXX-XXXX
    ccn_pattern = r"\d{4}-\d{4}-\d{4}-\d{4}"

    # Match account numbers (XXX-XXX-XXXX); excludes +1-800-555-0199 using negative look-behind.
    an_pattern = r"(?<!\+1-)\d{3}-\d{3}-\d{4}\b"
    
    # Match Social Security Numbers (SSNs) in XXX-XX-XXXX format.
    ssn_pattern = r"\d{3}-\d{2}-\d{4}"

    # Match IP addresses flexibly, like 192.168.1.100 and 192.168.1.1
    ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

    # Match full names (First Last) following 'Contact' or 'contact:' (I was getting
    # false positives like 'Contact Sarah' and 'Social Security').
    # Using two capture groups (with alternation '|'), only one will match per case;
    # the other remains empty.
    names_pattern = r"Contact\s+([A-Z][a-z]+\s+[A-Z][a-z]+)|contact:\s+([A-Z][a-z]+\s+[A-Z][a-z]+)"

    # Using re.findall this pattern returns tuples like: [('Sarah Johnson', ''), ('', 'Mike Davis')]
    # Use list comprehension to extract the non-empty element from each tuple (short-circuit logic).
    raw_name_matches = re.findall(names_pattern, text)
    cleaned_names = [name1 or name2 for name1, name2 in raw_name_matches]
    entities['names'] = cleaned_names

    # Extract and store matches for all other entity types.
    entities['emails'] = re.findall(email_pattern, text)
    entities['phones'] = re.findall(phone_pattern, text)
    entities['dates'] = re.findall(date_pattern, text)
    entities['urls'] = re.findall(url_pattern, text)
    entities['invoices'] = re.findall(inv_pattern, text)
    entities['currency_amounts'] = re.findall(currency_pattern, text)
    entities['credit_card_numbers'] = re.findall(ccn_pattern, text)
    entities['account_numbers'] = re.findall(an_pattern, text)
    entities['social_security_numbers'] = re.findall(ssn_pattern, text)
    entities['ip_addresses'] = re.findall(ip_pattern, text)
    
    return entities


# Display the extracted entities in a structured format.
result = extract_entities(text)
for entity_type, matches in result.items():
    print(f"{entity_type}: {matches}")