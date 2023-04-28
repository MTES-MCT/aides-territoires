from deepdiff import DeepDiff
from deepdiff.model import PrettyOrderedSet
from difflib import SequenceMatcher
from django.db.models import JSONField
from django.utils.html import format_html
from dataproviders.utils import content_prettify


def json_compare(old_json: JSONField, new_json: JSONField):
    """
    Compares two JSONFields and outputs the result as html
    """
    ddiff = DeepDiff(old_json, new_json, ignore_order=True, verbose_level=2)

    result_html = '<div class="json-compare">'

    if "dictionary_item_removed" in ddiff:
        result_html += "<h3>Suppression&nbsp;:</h3>"
        entries = ddiff["dictionary_item_removed"]
        result_html += format_entries(entries, "removed-entries", tag="del")

    if "iterable_item_removed" in ddiff:
        result_html += "<h3>Suppression de liste&nbsp;:</h3>"
        entries = ddiff["iterable_item_removed"]
        result_html += format_entries(entries, "removed-entries", tag="del")

    if "dictionary_item_added" in ddiff:
        result_html += "<h3>Ajout&nbsp;:</h3>"
        entries = ddiff["dictionary_item_added"]
        result_html += format_entries(entries, "added-entries", tag="ins")

    if "iterable_item_added" in ddiff:
        result_html += "<h3>Ajout de liste&nbsp;:</h3>"
        entries = ddiff["iterable_item_added"]
        result_html += format_entries(entries, "added-entries", tag="ins")

    if "values_changed" in ddiff:
        result_html += "<h3>Modification&nbsp;:</h3>"
        entries = ddiff["values_changed"]
        result_html += format_entries(entries, "added-entries", format_value=True)

    result_html = result_html.replace("{", "(")
    result_html = result_html.replace("}", ")")
    return format_html(result_html + "</div>")


def format_entries(
    entries_dict: dict, class_root: str, tag: str = "", format_value: bool = False
) -> str:

    """
    Formats a dict of entries for printing
    "tag" and "format_value" parameters are mutually exclusive:
        if format_value is present, tag is not used.
    """
    result_html = ""

    for key, value in entries_dict.items():
        result_html += f'<div class="{class_root}-path">{ format_paths(key) }: </div>'
        if format_value:
            result_html += f'<div class="changed-entries-values">{ format_value_diff(value) }</div>'
        else:
            result_html += (
                f'<div class="{class_root}-values"><{tag}>{value}</{tag}></div>'
            )

    return result_html


def format_paths(raw_path: PrettyOrderedSet) -> str:
    str_path = str(raw_path)
    str_list = str_path.split(",")

    output = ""
    for item in str_list:
        output += format_path(item)

    return output


def format_path(str_path: str) -> str:
    """
    Takes a path and formats it as an unordered list
    """
    str_path = str_path.lstrip("root[").rstrip("]")

    path_items = str_path.split("][")

    output = '<span class="formated-path">'

    for item in path_items:
        item = item.lstrip("'").rstrip("'")
        output += str(item) + "\n"
    output += "</span>"

    return output


def format_value_diff(value_dict: dict) -> str:
    """
    Takes the diff with two values outputted by Deepdiff and compares them
    """

    # Casting to string (to manage numbers/booleans)
    # then splitting so that the sequencer works on full words instead of single chars.
    old_value = str(value_dict["old_value"]).split(" ")
    new_value = str(value_dict["new_value"]).split(" ")

    sm = SequenceMatcher(None, old_value, new_value)

    output = []
    for opcode, a1, a2, b1, b2 in sm.get_opcodes():
        old_words = " ".join(old_value[a1:a2])
        old_words = content_prettify(old_words)
        new_words = " ".join(new_value[b1:b2])
        new_words = content_prettify(new_words)
        if opcode == "equal":
            output.append(old_words)
        elif opcode == "insert":
            output.append(f"<ins>{new_words}</ins>")
        elif opcode == "delete":
            output.append(f"<del>{old_words}</del>")
        elif opcode == "replace":
            output.append(f"<del>{old_words}</del><ins>{new_words}</ins>")
    return "".join(output)
