import inspect


def get_caller_name(skip: int = 2):
    """
    Get a name of a caller in the format module.class.method

    `skip` specifies how many levels of stack to skip while getting caller
    name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

    An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''

    parent_frame = stack[start][0]

    name = []
    module = inspect.getmodule(parent_frame)

    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)

    # detect classname
    if 'self' in parent_frame.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parent_frame.f_locals['self'].__class__.__name__)

    code_name = parent_frame.f_code.co_name
    if code_name != '<module>':  # top level usually
        name.append(code_name)  # function or a method

    del parent_frame
    return ''.join(name)
