from django.test import TestCase
from django.utils.unittest import skip


from iprestrict import models
from iprestrict import restrictor

class ReloadViewTest(TestCase):
    IP = '192.168.1.1'

    def add_allow_rule(self):
        localip = models.IPGroup.objects.create(name='Local IP')
        models.IPRange.objects.create(ip_group=localip, first_ip=self.IP)
        models.Rule.objects.create(url_pattern='ALL', ip_group = localip, action='A')

    @skip('Have to log in to test reload rules view')
    def test_reload_view(self):
        # This test doesn't conform to unit test best practices.
        # Unfortunately, it does depend on order so it is in one method
        # instead of 3 methods, each asserting one thing

        # 1
        response = self.client.get('', REMOTE_ADDR = self.IP)
        self.assertEqual(response.status_code, 403, 'Should be restricted')

        # 2
        self.add_allow_rule()
        response = self.client.get('', REMOTE_ADDR = self.IP)
        self.assertEqual(response.status_code, 403, 'Should still be restricted - rules have not been reloaded')

        # 3 reload rules
        # TODO I have to log in as superuser for this to work
        response = self.client.get('/iprestrict/reload_rules')
        response = self.client.get('', REMOTE_ADDR = self.IP)
        self.assertEqual(response.status_code, 404, 'Should be allowed now')