import ElasticEmail
from ElasticEmail.api import contacts_api, emails_api
from ElasticEmail.model.contact_status import ContactStatus
from ElasticEmail.model.contact_payload import ContactPayload
from pprint import pprint

from ElasticEmail.model.email_message_data import EmailMessageData
from ElasticEmail.model.email_recipient import EmailRecipient

configuration = ElasticEmail.Configuration()
configuration.api_key['apikey'] = '8C2A1826827CCF635A2C9BBF8A01E51DAD1C8969A13C1625650A698915237D00AD2052326D6F2BD5530308F53A385AC7'
contact_payload = [
        ContactPayload(
            email="johnsmith@domain.com",
            status=ContactStatus("Active"),
            first_name="John",
            last_name="Smith",
        ),
    ]


list_names = [
        "New list",
    ]

with ElasticEmail.ApiClient(configuration) as api_client:
    api_instance = emails_api.EmailsApi(api_client)
    email_message_data = EmailMessageData(
        recipients=[
            EmailRecipient(
                email="MeowWow "
            ),
        ],
        content={
            "Body": [
                {
                    "ContentType": "HTML",
                    "Content": "My test email content ;)"
                }
            ],
            "Subject": "Python EE lib test",
            "From": "MyEmail "
        }
    )

    try:
        api_response = api_instance.emails_post(email_message_data)
        pprint(api_response)
    except ElasticEmail.ApiException as e:
        print("Exception when calling EmailsApi->emails_post: %s\n" % e)


