__all__ = [
    "Contact",
    "RAWContact",
    "ContactData",
    "MIMEType"
]

from .json_originated import (
    JSONOriginated
)


# Useful links:
# https://www.dev2qa.com/android-contacts-database-structure/
# https://www.dev2qa.com/android-contacts-fields-data-table-columns-and-data-mimetype-explain/
# https://developer.android.com/guide/topics/providers/contacts-provider


class Contact(JSONOriginated):

    __var_base__ = lambda _ : "contact"


class RAWContact(JSONOriginated):

    __var_base__ = lambda _ : "raw_contact"


class ContactData(JSONOriginated):

    __var_base__ = lambda _ : "data"


class MIMEType(JSONOriginated):

    __var_base__ = lambda _ : "mime"
