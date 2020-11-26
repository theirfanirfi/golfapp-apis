import re
def escape_string(a_string):
    escaped = a_string.translate(str.maketrans({"-": r"\-",
                                                "]": r"\]",
                                                "'": r"\'",
                                                "\\": r"\\",
                                                "^": r"\^",
                                                "$": r"\$",
                                                "*": r"\*",
                                                ".": r"\.",
                                                "&": r"\&",
                                                "#": r"\#",
                                                ";": r"\;",

                                                }))
    return escaped

def strip_emoji(text):
    RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    return RE_EMOJI.sub(r'', text)