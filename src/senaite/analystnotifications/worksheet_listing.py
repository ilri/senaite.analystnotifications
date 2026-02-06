import logging
from zope.component import adapter
from zope.interface import Interface
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

logger = logging.getLogger("senaite.analystnotifications")


@adapter(Interface, IObjectModifiedEvent)
def add_batchid_column(obj, event):
    """Add Batch ID column to Add Analyses worksheet listings."""
    logger.warning(">>> add_batchid_column subscriber triggered <<<")
    view = getattr(obj, 'object', obj)  # usually obj is the view
    if not view:
        return

    # Only target Add Analyses listing
    logger.warning("The view id is: %s", getattr(view, 'id', None))
    if getattr(view, 'id', '') != 'add_analyses':
        return

    columns = getattr(view, 'columns', {})
    if 'BatchID' not in columns:
        columns['BatchID'] = {'title': 'Batch ID', 'toggle': True}
        view.columns = columns
        logger.warning(">>> Batch ID column added to Add Analyses <<<")

    # Patch row items for existing analyses
    for item in getattr(view, 'items', []):
        try:
            analysis = item.getObject()
            sample = analysis.getSample()
            batch = sample.getBatch() if sample else None
            item['BatchID'] = batch.getId() if batch else ''
        except Exception:
            item['BatchID'] = ''