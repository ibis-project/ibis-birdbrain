# imports
from enum import Enum
from marvin import ai_classifier


# classifiers
@ai_classifier
class EvalPythonCode(Enum):
    """Classifies Python code as valid or invalid."""

    INVALID = False
    VALID = True


@ai_classifier
class EvalSQLCode(Enum):
    """Classifies SQL code as valid or invalid."""

    INVALID = False
    VALID = True


@ai_classifier
class EvalTextForQuery(Enum):
    """Classifies text as requiring a SQL query to answer or not."""

    NOT_QUERY = False
    QUERY = True
