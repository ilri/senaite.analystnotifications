# -*- coding: utf-8 -*-
import logging
from Acquisition import aq_parent
from senaite.analystnotifications.mailer import send_email_to_analyst

logger = logging.getLogger("senaite.analystnotifications")

logger.warning(">>> subscribers.py LOADED <<<")

def is_worksheet(obj):
    """Detect if obj is a worksheet dynamically."""
    # Check portal_type first
    if getattr(obj, 'portal_type', None) == 'Worksheet':
        return True
    # Fallback: check if it has an 'analyst' field
    if hasattr(obj, 'getField') and obj.getField('analyst'):
        return True
    return False


def worksheet_analyst_assigned(obj, event):
    """Subscriber to send email when an analyst is assigned to a worksheet."""

    # Start with the object the event fired on
    logger.warning("The object type is: %s",getattr(obj, 'portal_type', None))

    ws = obj

    # If not a worksheet, try parent (acquisition)
    if not is_worksheet(ws):
        parent = aq_parent(ws)
        if parent and is_worksheet(parent):
            ws = parent
        else:
            logger.debug(">>> Event fired on non-worksheet object: %s (%s) <<<", getattr(obj, 'id', repr(obj)), type(obj))
            return

    # Access the analyst field
    field = ws.getField('Analyst')
    analyst = field.get(ws) if field else None

    if not analyst:
        logger.warning(">>> Worksheet %s has no assigned analyst <<<", getattr(ws, 'id', repr(ws)))
        return

    logger.warning(">>> Worksheet %s assigned to analyst %s <<<", getattr(ws, 'id', repr(ws)), analyst)

    # Send email
    try:
        send_email_to_analyst(ws)
        logger.warning(">>> Email sent for worksheet %s <<<", getattr(ws, 'id', repr(ws)))
    except Exception as e:
        logger.error(">>> Failed to send email for worksheet %s: %s <<<", getattr(ws, 'id', repr(ws)), str(e))
