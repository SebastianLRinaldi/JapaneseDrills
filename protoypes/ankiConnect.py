# import requests
# import json

# def get_notes_with_tag(tag):
#     payload = {
#         "action": "findNotes",
#         "version": 6,
#         "params": {
#             "query": f'tag:{tag}'
#         }
#     }

#     response = requests.post("http://localhost:8765", json=payload)
#     response.raise_for_status()

#     note_ids = response.json().get("result", [])
#     return note_ids

# # Example usage:
# tag = "status::understandable"
# note_ids = get_notes_with_tag(tag)
# print(f"Found {len(note_ids)} notes with tag '{tag}':")
# print(note_ids)

import requests
import re
import html

def get_notes_with_tag(tag):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'tag:{tag}'
        }
    }
    response = requests.post("http://localhost:8765", json=payload)
    response.raise_for_status()
    return response.json().get("result", [])





def get_notes_with_tag_and_custom(tag, custom):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'tag:{tag} prop:cdn:{custom}'
        }
    }
    response = requests.post("http://localhost:8765", json=payload)
    response.raise_for_status()
    return response.json().get("result", [])


def get_notes_with_two_tags(tag1, tag2):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'tag:{tag1} tag:{tag2}'
        }
    }
    response = requests.post("http://localhost:8765", json=payload)
    response.raise_for_status()
    return response.json().get("result", [])


def get_notes_with_two_tags_and_custom(tag1, tag2, custom):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'tag:{tag1} tag:{tag2} prop:cdn:{custom}'
        }
    }
    response = requests.post("http://localhost:8765", json=payload)
    response.raise_for_status()
    return response.json().get("result", [])




def get_notes_with_tag_and_mastery(tag, custom):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'tag:{tag} (tag:status:understandable OR prop:cdn:{custom})'
        }
    }
    response = requests.post("http://localhost:8765", json=payload)
    response.raise_for_status()
    return response.json().get("result", [])


def get_fields(note_ids, field_name):
    if not note_ids:
        return {}

    payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": note_ids
        }
    }
    response = requests.post("http://localhost:8765", json=payload)
    response.raise_for_status()
    notes_info = response.json().get("result", [])

    # Extract the field values
    result = {}
    for note in notes_info:
        fields = note.get("fields", {})
        if field_name in fields:
            result[note["noteId"]] = fields[field_name]["value"]
    return result

def clean_html(raw_html, remove_spaces=True):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = html.unescape(cleantext)  # converts &nbsp; to space
    if remove_spaces:
        cleantext = cleantext.replace(' ', '')
    return cleantext

# Usage
"""
Tell you the function, not the form

Cue:
“Express that two things happened in sequence.”
→ Expected: 〜てから, 〜あとで, 〜た上で, etc.


Time Pressure Prompt
Flash a grammar point.

You have 10 seconds to say or write a sentence using it.

Why? Pressure removes overthinking. Forces gut recall.


9. Minimal Clue Prompts
Just show the grammar with a category (e.g., “contrast”).

Cue:
〜のに (contrast)

"""
tag = "verb"
custom = "notesct>13"
field_name = "jap_vocab_from_sentence"

note_ids = get_notes_with_tag_and_mastery(tag, custom)
fields_data = get_fields(note_ids, field_name)
print(len(note_ids))
for note_id, vocab in fields_data.items():
    print(f"{clean_html(vocab)}")
