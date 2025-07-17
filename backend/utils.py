PROGRAM_ALIASES = {
    "MIM": ["master in management", "mim"],
    "MMDT": ["master in management and data technology", "management in data and technology", "mmdt"],
    "MIE": ["master in information engineering", "information engineering", "mie", "ie"]
}

def extract_program_from_messages(messages: list[str]) -> str | None:
    full_text = " ".join(messages).lower()
    for code, aliases in PROGRAM_ALIASES.items():
        for alias in aliases:
            if alias in full_text:
                return code
    return None