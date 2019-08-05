#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_compute_address_facts
description:
- Gather facts for GCP Address
short_description: Gather facts for GCP Address
version_added: 2.7
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  filters:
    description:
    - A list of filter value pairs. Available filters are listed here U(https://cloud.google.com/sdk/gcloud/reference/topic/filters).
    - Each additional filter in the list will act be added as an AND condition (filter1
      and filter2) .
    type: list
  region:
    description:
    - URL of the region where the regional address resides.
    - This field is not applicable to global addresses.
    required: true
    type: str
extends_documentation_fragment: gcp
'''

EXAMPLES = '''
- name: " a address facts"
  gcp_compute_address_facts:
    region: us-west1
    filters:
    - name = test_object
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
'''

RETURN = '''
items:
  description: List of items
  returned: always
  type: complex
  contains:
    address:
      description:
      - The static external IP address represented by this resource. Only IPv4 is
        supported. An address may only be specified for INTERNAL address types. The
        IP address must be inside the specified subnetwork, if any.
      returned: success
      type: str
    addressType:
      description:
      - The type of address to reserve, either INTERNAL or EXTERNAL.
      - If unspecified, defaults to EXTERNAL.
      returned: success
      type: str
    creationTimestamp:
      description:
      - Creation timestamp in RFC3339 text format.
      returned: success
      type: str
    description:
      description:
      - An optional description of this resource.
      returned: success
      type: str
    id:
      description:
      - The unique identifier for the resource.
      returned: success
      type: int
    name:
      description:
      - Name of the resource. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match the
        regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character
        must be a lowercase letter, and all following characters must be a dash, lowercase
        letter, or digit, except the last character, which cannot be a dash.
      returned: success
      type: str
    networkTier:
      description:
      - 'The networking tier used for configuring this address. This field can take
        the following values: PREMIUM or STANDARD. If this field is not specified,
        it is assumed to be PREMIUM.'
      returned: success
      type: str
    subnetwork:
      description:
      - The URL of the subnetwork in which to reserve the address. If an IP address
        is specified, it must be within the subnetwork's IP range.
      - This field can only be used with INTERNAL type with GCE_ENDPOINT/DNS_RESOLVER
        purposes.
      returned: success
      type: dict
    users:
      description:
      - The URLs of the resources that are using this address.
      returned: success
      type: list
    region:
      description:
      - URL of the region where the regional address resides.
      - This field is not applicable to global addresses.
      returned: success
      type: str
'''

################################################################################
# Imports
################################################################################
from ansible.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest
import json

################################################################################
# Main
################################################################################


def main():
    module = GcpModule(argument_spec=dict(filters=dict(type='list', elements='str'), region=dict(required=True, type='str')))

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/compute']

    items = fetch_list(module, collection(module), query_options(module.params['filters']))
    if items.get('items'):
        items = items.get('items')
    else:
        items = []
    return_value = {'items': items}
    module.exit_json(**return_value)


def collection(module):
    return "https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/addresses".format(**module.params)


def fetch_list(module, link, query):
    auth = GcpSession(module, 'compute')
    response = auth.get(link, params={'filter': query})
    return return_if_object(module, response)


def query_options(filters):
    if not filters:
        return ''

    if len(filters) == 1:
        return filters[0]
    else:
        queries = []
        for f in filters:
            # For multiple queries, all queries should have ()
            if f[0] != '(' and f[-1] != ')':
                queries.append("(%s)" % ''.join(f))
            else:
                queries.append(f)

        return ' '.join(queries)


def return_if_object(module, response):
    # If not found, return nothing.
    if response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg="Invalid JSON response with error: %s" % inst)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


if __name__ == "__main__":
    main()
