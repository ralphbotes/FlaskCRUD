def clean(text):
    new_text = ""
    characters_to_remove = ",[]()'"

    for char in text:
        if char not in characters_to_remove:
            new_text += char

    return new_text