# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from azure.cli.command_modules.profile._subscription_selector import SubscriptionSelector


# These dummy subscriptions are used in both unit test and interactive test
DUMMY_SUBSCRIPTIONS = [
    # 0: sub 2
    {
        "id": "00000000-0000-0000-0000-222222222222",
        "name": "sub 2",
        "tenantDefaultDomain": "tenant1.onmicrosoft.com",
        "tenantDisplayName": "Tenant 1",
        "tenantId": "00000000-0000-0000-1111-111111111111",
        "environmentName": "AzureCloud",
        "isDefault": True
    },
    # 1: sub 1
    {
        "id": "00000000-0000-0000-0000-111111111111",
        "name": "SUB 1",
        "tenantDefaultDomain": "tenant1.onmicrosoft.com",
        "tenantDisplayName": "Tenant 1",
        "tenantId": "00000000-0000-0000-1111-111111111111",
        "environmentName": "AzureCloud",
        "isDefault": False
    },
    # 2: sub 3
    {
        "id": "00000000-0000-0000-0000-333333333333",
        "name": "Sub 3 with long long long long long name",
        "tenantDefaultDomain": "tenant1.onmicrosoft.com",
        "tenantDisplayName": "Tenant 1",
        "tenantId": "00000000-0000-0000-1111-111111111111",
        "environmentName": "AzureCloud",
        "isDefault": False
    },
    # 3: tenant account
    {
        "id": "00000000-0000-0000-1111-222222222222",
        "name": "N/A(tenant level account)",
        "tenantDefaultDomain": "tenant2.onmicrosoft.com",
        "tenantDisplayName": "Tenant 2",
        "tenantId": "00000000-0000-0000-1111-222222222222",
        "environmentName": "AzureCloud",
        "isDefault": False
    }
]

dummy_subscriptions_no_tenant_domain = [
    {
        "id": "00000000-0000-0000-0000-222222222222",
        "name": "sub 2",
        "tenantId": "00000000-0000-0000-1111-111111111111",
        "environmentName": "AzureCloud",
    }
]


class TestSubscriptionSelection(unittest.TestCase):

    def setUp(self):
        super().setUp()

    def test_format_subscription_table(self):
        sub = DUMMY_SUBSCRIPTIONS
        selector = SubscriptionSelector(sub)

        assert (selector._index_to_subscription_map == {
            '1': sub[3],
            '2': sub[1],
            '3': sub[0],
            '4': sub[2]})

        expected_table_str = """\
No     Subscription name                     Subscription ID                       Tenant
-----  ------------------------------------  ------------------------------------  --------
[1]    N/A(tenant level account)             00000000-0000-0000-1111-222222222222  Tenant 2
[2]    SUB 1                                 00000000-0000-0000-0000-111111111111  Tenant 1
[3] *  \x1b[96msub 2\x1b[0m                                 \x1b[96m00000000-0000-0000-0000-222222222222\x1b[0m  \x1b[96mTenant 1\x1b[0m
[4]    Sub 3 with long long long long lo...  00000000-0000-0000-0000-333333333333  Tenant 1"""
        assert selector._table_str == expected_table_str


def invoke_subscription_selector():
    """This method provides a way of directly testing subscription selection, without running an actual `az login`.
    Invoke this method with:
    python -m azure.cli.command_modules.profile.tests.latest.test_subscription_selector
    """
    result = SubscriptionSelector(DUMMY_SUBSCRIPTIONS)()
    print("Result:", result)


if __name__ == '__main__':
    invoke_subscription_selector()
