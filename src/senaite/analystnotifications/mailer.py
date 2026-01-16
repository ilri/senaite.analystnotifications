# -*- coding: utf-8 -*-
import logging
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

logger = logging.getLogger("senaite.analystnotifications")


def send_email_to_analyst(worksheet):
    site = getSite()
    mailhost = getToolByName(site, "MailHost", None)

    logger.warning("email sender is %s and mailhost is %s", site.getProperty('email_from_address', None), mailhost)

    if mailhost is None:
        logger.error("MailHost not found")
        return

    field = worksheet.getField('Analyst')
    analyst = field.get(worksheet) if field else None

    if not analyst:
        logger.warning("No analyst assigned to worksheet %s", worksheet.id)
        return
    sample_ids = set()
    for analyses in worksheet.getAnalyses():
        sample = analyses.aq_parent
        sample_ids.add(sample.getId())
    

    # Analyst is usually a userid
    email = worksheet.portal_membership.getMemberById(analyst).getProperty('email')

    if not email:
        logger.warning("Analyst %s has no email", analyst)
        return

    subject = "Worksheet assigned: %s" % worksheet.Title()
    body = "You have been assigned worksheet %s" % worksheet.Title()
    sender = get_sender_email() 

    mailhost.send(
        body,
        mto=email,
        mfrom=sender[0],
        subject=subject,
        charset="utf-8"
    )

    logger.info("Email sent to %s for worksheet %s", email, worksheet.id)


def get_sender_email():
    registry = getUtility(IRegistry)

    email = registry.get("plone.email_from_address", None)
    name = registry.get("plone.email_from_name", None)
    logger.warning("Sender email: %s, name: %s", email, name)

    return email, name

