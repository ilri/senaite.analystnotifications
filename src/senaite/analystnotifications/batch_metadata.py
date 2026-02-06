from bika.lims.interfaces import IAnalysisRequest
from bika.lims import api
from plone.indexer import indexer


@indexer(IAnalysisRequest)
def BatchID(ar):
    """Catalog indexer for Batch ID"""

    try:
        batch = ar.getBatch()
        if not batch:
            return ""
        return batch.getId()
    except Exception:
        return ""