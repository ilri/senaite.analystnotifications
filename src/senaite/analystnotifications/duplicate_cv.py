from zope.component import adapter
from bika.lims.interfaces import IDuplicateAnalysis
from bika.lims import api
import logging
logger = logging.getLogger("senaite.analystnotifications.adapters.duplicate_cv")

@adapter(IDuplicateAnalysis)
class DuplicateCVOutOfRange(object):
    """Override duplicate QC using CV instead of +/- bounds"""

    def __init__(self, analysis):
        self.analysis = analysis

    def __call__(self, result=None, specification=None):
        original = self.analysis.getAnalysis()
        if not original:
            return None

        original_result = original.getResult()
        if not api.is_floatable(original_result):
            return None

        if not api.is_floatable(result):
            return {
                "out_of_range": True,
                "acceptable": False
            }

        O = api.to_float(original_result)
        D = api.to_float(result)

        # CV limit (%), reuse duplicate variation field
        cv_limit = api.to_float(original.getDuplicateVariation(), 0)
        logger.warning("CV limit for duplicate: %s%%", cv_limit)
        if not cv_limit:
            return None

        mean = (O + D) / 2.0
        if mean == 0:
            return {
                "out_of_range": True,
                "acceptable": False
            }

        cv = abs(D - O) / ((2 ** 0.5) * mean) * 100.0
        logger.warning("Duplicate CV check: O=%s D=%s CV=%.2f%% limit=%.2f%%",
                     O, D, cv, cv_limit)

        if cv <= cv_limit:
            return {
                "out_of_range": False,
                "acceptable": True
            }

        return {
            "out_of_range": True,
            "acceptable": False
        }
