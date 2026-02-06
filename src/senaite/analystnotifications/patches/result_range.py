from bika.lims.content.duplicateanalysis import DuplicateAnalysis
import logging
logger = logging.getLogger("senaite.analystnotifications.patches.result_range")

_original_getResultsRange = None


def patch_duplicate_results_range():
    global _original_getResultsRange

    if _original_getResultsRange is not None:
        return

    _original_getResultsRange = DuplicateAnalysis.getResultsRange
    logger.info("Patching DuplicateAnalysis.getResultsRange: %s", _original_getResultsRange)


    def getResultsRange(self):
        specs = _original_getResultsRange(self)

        # specs is usually an object with min/max attrs
        if specs:
            specs.min = None
            specs.max = None

            if hasattr(specs, "minformatted"):
                specs.minformatted = ""
            if hasattr(specs, "maxformatted"):
                specs.maxformatted = ""

        return specs

    DuplicateAnalysis.getResultsRange = getResultsRange
