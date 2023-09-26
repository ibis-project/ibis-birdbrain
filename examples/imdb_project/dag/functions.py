# imports
import ibis


# functions
## public
def convert_nconst_to_int(t, col=None):
    return _convert_str_to_int(t, col, "nm")


def convert_tconst_to_int(t, col=None):
    return _convert_str_to_int(t, col, "tt")


## private
def _convert_str_to_int(t, col=None, replace=""):
    t = t.mutate(t[col].replace(replace, "").cast("int").name(col))
    return t
