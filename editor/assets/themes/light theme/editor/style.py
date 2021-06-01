from pygments.style import Style
# from pygments.token import Keyword
# from pygments.token import Literal
# from pygments.token import Name
# from pygments.token import Comment
# from pygments.token import Other
# from pygments.token import Punctuation
# from pygments.token import String
# from pygments.token import Error
# from pygments.token import Number
# from pygments.token import Operator
# from pygments.token import Generic
# from pygments.token import Text
# from pygments.token import Whitespace


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
