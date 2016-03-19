# -*- coding: utf-8 -*-
'''
    :codeauthor: David Boucha
    :copyright: © 2014 by the SaltStack Team, see AUTHORS for more details.
    :license: Apache 2.0, see LICENSE for more details.


    salt.grains.digitalocean_metadata.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Create a DigitalOcean grain from the DigitalOcean metadata server.
    See https://developers.digitalocean.com/documentation/metadata/#metadata-in-json

    Note that not all datacenters were supported when this feature was first
    released.
'''

# Import Python Libs
import logging
import requests

# Set up logging
LOG = logging.getLogger(__name__)

MD_BASE_URI = "http://169.254.169.254/metadata/v1"
__virtualname__ = "digitalocean"


def __virtual__():
    '''
    We should only load if this is actually a digitalocean instance

    Also catch if the instance predates the metadata service
    '''
    try:
        ret = requests.get(MD_BASE_URI + '.json')
        if ret.text == "":
            return False
        return __virtualname__
    except requests.ConnectionError:
        LOG.info('digitalocean grain: Instance too old to support metadata')
        return False
    except Exception:
        return False


def digitalocean():
    '''
    Return DigitalOcean metadata.
    '''
    metadata = requests.get(MD_BASE_URI + '.json')

    if metadata.status_code == 200:
        return {'digitalocean': metadata.json()}
    return {'digitalocean': []}


if __name__ == '__main__':
    print digitalocean()
