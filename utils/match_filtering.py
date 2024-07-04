import re
import unicodedata


def _analyze_text_local(text: str, return_tokens=False) -> str:
    nfkd_form = unicodedata.normalize("NFKD", text)
    nfkd_form = nfkd_form.encode("ASCII", "ignore").decode()
    processed_text = re.sub(r"\W|_|\s+", " ", nfkd_form).lower().strip()
    processed_text = re.sub(r"\s+", " ", processed_text)
    if return_tokens:
        return processed_text.split()
    return processed_text


def check_match(
    query_name,
    query_winery_name,
    query_type,
    retrieved_name,
    retrieved_winery_name,
    retrieved_type,
):
    if query_winery_name == "":
        retrieved_name = retrieved_name + " " + retrieved_winery_name
        retrieved_winery_name = ""

    is_exact_name = sorted(
        _analyze_text_local(query_name, return_tokens=True)
    ) == sorted(_analyze_text_local(retrieved_name, return_tokens=True))

    is_exact_winery_name = sorted(
        _analyze_text_local(query_winery_name, return_tokens=True)
    ) == sorted(_analyze_text_local(retrieved_winery_name, return_tokens=True))

    if query_type is None or query_type.upper().strip() != "RED":
        is_exact_type = True
    else:
        is_exact_type = retrieved_type.upper().strip() == "RED"

    return is_exact_name and is_exact_winery_name and is_exact_type
