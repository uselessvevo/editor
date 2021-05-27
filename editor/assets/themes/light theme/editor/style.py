from enum import Enum

from pygments.style import Style
from pygments.token import Keyword
from pygments.token import Literal
from pygments.token import Name
from pygments.token import Comment
from pygments.token import Other
from pygments.token import Punctuation
from pygments.token import String
from pygments.token import Error
from pygments.token import Number
from pygments.token import Operator
from pygments.token import Generic
from pygments.token import Text
from pygments.token import Whitespace


class EditorStyle(Style):
    #: overall background color (``None`` means transparent)
    background_color = '#ffffff'

    #: highlight background color
    highlight_color = '#ffffcc'

    #: line number font color
    line_number_color = 'inherit'

    #: line number background color
    line_number_background_color = 'transparent'

    #: special line number font color
    line_number_special_color = '#000000'

    #: special line number background color
    line_number_special_background_color = '#ffffc0'

    default_style = ""

    # styles = {
    #     Text: "",
    #     # f8f8f2",
    #     Whitespace: "",
    #     Error: "#960050 bg:#1e0010",
    #     Other: "",
    #     Comment: "#000000",
    #     Comment.Multiline: "",
    #     Comment.Preproc: "",
    #     Comment.Single: "",
    #     Comment.Special: "",
    #     Keyword: "#66d9ef",
    #     Keyword.Constant: "",
    #     Keyword.Declaration: "",
    #     Keyword.Namespace: "#f92672",
    #     Keyword.Pseudo: "",
    #     Keyword.Reserved: "",
    #     Keyword.Type: "",
    #     Operator: "#f92672",
    #     Operator.Word: "",
    #     Punctuation: "#f8f8f2",
    #     Name: "#f8f8f2",
    #     Name.Attribute: "#a6e22e",
    #     Name.Builtin: "",
    #     Name.Builtin.Pseudo: "",
    #     Name.Class: "#a6e22e",
    #     Name.Constant: "#66d9ef",
    #     Name.Decorator: "#a6e22e",
    #     Name.Entity: "",
    #     Name.Exception: "#a6e22e",
    #     Name.Function: "#a6e22e",
    #     Name.Property: "",
    #     Name.Label: "",
    #     Name.Namespace: "",
    #     Name.Other: "#a6e22e",
    #     Name.Tag: "#f92672",
    #     Name.Variable: "",
    #     Name.Variable.Class: "",
    #     Name.Variable.Global: "",
    #     Name.Variable.Instance: "",
    #     Number: "#ae81ff",
    #     Number.Float: "",
    #     Number.Hex: "",
    #     Number.Integer: "",
    #     Number.Integer.Long: "",
    #     Number.Oct: "",
    #     Literal: "#ae81ff",
    #     Literal.Date: "#e6db74",
    #     String: "#e6db74",
    #     String.Backtick: "",
    #     String.Char: "",
    #     String.Doc: "",
    #     String.Double: "",
    #     String.Escape: "#ae81ff",
    #     String.Heredoc: "",
    #     String.Interpol: "",
    #     String.Other: "",
    #     String.Regex: "",
    #     String.Single: "",
    #     String.Symbol: "",
    #     Generic: "",
    #     Generic.Deleted: "#f92672",
    #     Generic.Emph: "italic",
    #     Generic.Error: "",
    #     Generic.Heading: "",
    #     Generic.Inserted: "#a6e22e",
    #     Generic.Output: "#66d9ef",
    #     Generic.Prompt: "bold #f92672",
    #     Generic.Strong: "bold",
    #     Generic.Subheading: "#75715e",
    #     Generic.Traceback: ""
    # }

