import logging
from zope.interface import implementer
from zope.component import adapter
from zope.interface import Interface

from senaite.app.listing.interfaces import IListingViewAdapter
from bika.lims import api

logger = logging.getLogger("senaite.analystnotifications")


@implementer(IListingViewAdapter)
@adapter(Interface, Interface)
class AddAnalysesBatchIDAdapter:

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):

        if getattr(self.context, "portal_type", None) != "Worksheet":
            return

        request = getattr(self.listing, "request", None)
        url = getattr(request, "ACTUAL_URL", "") if request else ""
        if "add_analyses" not in url:
            return

        self.listing.columns["BatchID"] = {
            "title": "Batch ID",
            "toggle": True,
            "sortable": True,
            "index": "BatchID",
        }

        #self.listing.sort_fields["BatchID"] = "BatchID"

        for state in self.listing.review_states:
            if "BatchID" not in state["columns"]:
                state["columns"].append("BatchID")

    def folder_item(self, obj, item, index):
      """Populate BatchID safely for Add Analyses listing"""

      # Default value guarantees no KeyError downstream
      item["BatchID"] = "-"

      # Resolve real object
      ar = api.get_object(obj)

     # EARLY RETURN: must be an AnalysisRequest
      if not ar:
          return item

      if not hasattr(ar, "getBatch"):
          # This avoids AttributeError on unexpected objects
          return item

      #EARLY RETURN: no batch assigned
      batch = ar.getBatch()
      if not batch:
          return item

      # All good Happy path
      item["BatchID"] = batch.getId()
      return item