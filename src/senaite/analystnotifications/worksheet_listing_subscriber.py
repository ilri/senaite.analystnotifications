import logging
from .adapters import AddAnalysesBatchIDAdapter

logger = logging.getLogger("senaite.analystnotifications")
logger.setLevel(logging.WARNING)

def add_batchid_adapter(obj, event):
    """Attach BatchID adapter logic to Add Analyses worksheet."""
    logger.warning(">>> add_batchid_adapter subscriber triggered <<<")
    # obj.object is sometimes the view
    view = getattr(obj, "object", obj)

    # Only patch Add Analyses worksheet
    if getattr(view, "id", "") != "add_analyses":
        return

    # Instantiate the adapter (logger fires here)
    AddAnalysesBatchIDAdapter(view)