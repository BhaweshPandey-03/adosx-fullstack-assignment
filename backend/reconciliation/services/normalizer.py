import re


RECORD_ID_PATTERN = re.compile(r"^REC-(\d+)$")


def normalize_record_ref(value):
    """
    Convert known System B record reference formats into
    a canonical REC-NNNN form.

    Returns:
        Canonical reference when recognized.
        None when the value cannot be normalized safely.
    """
    if value is None:
        return None

    value = value.strip().upper()

    if not value:
        return None

    # Remove whitespace around separators.
    value = re.sub(r"\s*-\s*", "-", value)

    # Convert "REC 1034" / "REC1034" into "REC-1034".
    if value.startswith("REC"):
        digits = value[3:].strip()

        if digits.isdigit():
            return f"REC-{digits}"

    # Convert a bare numeric reference like "1112".
    if value.isdigit():
        return f"REC-{value}"

    # Already canonical.
    if RECORD_ID_PATTERN.fullmatch(value):
        return value

    return None