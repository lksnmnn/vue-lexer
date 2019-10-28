import re

from pygments.lexer import bygroups, default, include
from pygments.lexers.javascript import JavascriptLexer
from pygments.token import Name, Operator, Punctuation, String, Text

# Use same tokens as `JavascriptLexer`, but with tags and attributes support
TOKENS = JavascriptLexer.tokens

TOKENS.update(
    {
        "vue": [
            (r"(<)([\w-]+)", bygroups(Punctuation, Name.Tag), "tag"),
            (
                r"(<)(/)([\w]+)(>)",
                bygroups(Punctuation, Punctuation, Name.Tag, Punctuation),
            ),
        ],
        "tag": [
            (r"\s+", Text),
            (
                r"([@:]?[\w-]+\s*)(=)(\s*)",
                bygroups(Name.Attribute, Operator, Text),
                "attr",
            ),
            (r"[{}]+", Punctuation),
            (r"[\w\.-]+", Name.Attribute),
            (r"(/?)(\s*)(>)", bygroups(Punctuation, Text, Punctuation), "#pop"),
        ],
        "attr": [
            ("{", Punctuation, "expression"),
            ('".*?"', String, "#pop"),
            ("'.*?'", String, "#pop"),
            default("#pop"),
        ],
        "expression": [
            ("{", Punctuation, "#push"),
            ("}", Punctuation, "#pop"),
            include("root"),
        ],
    }
)
TOKENS["root"].insert(0, include("vue"))


class VueLexer(JavascriptLexer):
    name = "vue"
    aliases = ["vue", "vuejs"]
    filenames = ["*.vue"]
    mimetypes = ["text/x-vue", "application/x-vue"]

    flags = re.MULTILINE | re.DOTALL | re.UNICODE

    tokens = TOKENS
