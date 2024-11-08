from typing import Dict

import user_agents
from example_consumer.enrichments.enricher import Enrichment


class UserAgent(Enrichment):
    """
    Enrich the incoming record with device, operating system, and browser info gathered from User Agent analysis.
    Implementation: Using the user-agents library, which uses ua-parser under the hood
    """
    def enrich(self, record: Dict) -> Dict:
        """
        Enrich the incoming record with device, operating system, and browser info gathered from User Agent analysis.
        Implementation: Using the user-agents library, which uses ua-parser under the hood
        """
        user_agent_string = record.get('user_agent', '')
        user_agent_object = user_agents.parse(user_agent_string)

        record.update({
            'browser_family': user_agent_object.browser.family,
            'browser_version': user_agent_object.browser.version_string,
            'os_family': user_agent_object.os.family,
            'os_version': user_agent_object.os.version_string,
            'device_family': user_agent_object.device.family,
            'device_brand': user_agent_object.device.brand,
            'device_model': user_agent_object.device.model,
            'device_is_mobile': user_agent_object.is_mobile,
            'device_is_tablet': user_agent_object.is_tablet,
            'device_is_pc': user_agent_object.is_pc,
            'device_is_bot': user_agent_object.is_bot,
            'device_is_touch_capable': user_agent_object.is_touch_capable,
        })

        return record
