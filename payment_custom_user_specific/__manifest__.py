# -*- coding: utf-8 -*-
{
    "name": "Restrict Users Payment",
    "summary": "Hide cost price, hide standard price, hide product price, hide product cost price",
    "description": "The cost price can only be accessed through Access Group.",
    "version": "14.0.1",
    "category": "Access Right",
    "depends": ['account','web_domain_field','user_customization'],
    "data": [
'views/account_payment.xml'
    ],
    "application": False,
    "installable": True,
}
