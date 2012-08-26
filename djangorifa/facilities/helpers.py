# http://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname
def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m