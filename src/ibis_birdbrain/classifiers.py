# imports
import marvin

from enum import Enum


# classifiers
@marvin.ai_classifier
class NeedsDataQuery(Enum):
    """
    Needs query.
    """

    YES = True
    NO = False


@marvin.ai_classifier
class NeedsInternetSearch(Enum):
    """
    Needs internet search.
    """

    YES = True
    NO = False


@marvin.ai_classifier
class NeedsDocsSearch(Enum):
    """
    Needs docs search.
    """

    YES = True
    NO = False


@marvin.ai_classifier
class IsRelevantDataConnection(Enum):
    """
    Is a data connection relevant to the text.
    """

    YES = True
    NO = False


@marvin.ai_classifier
class IsRelevantDocument(Enum):
    """
    Is a document relevant to the text.
    """

    YES = True
    NO = False
