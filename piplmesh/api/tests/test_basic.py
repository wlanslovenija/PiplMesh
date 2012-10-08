import datetime, time, urlparse

from django.core import urlresolvers
from django.test import client, utils
from django.utils import simplejson as json, timezone

from tastypie_mongoengine import test_runner

from pushserver import signals

from piplmesh.account import models as account_models
from piplmesh.frontend import tasks

@utils.override_settings(DEBUG=True, CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, PUSH_SERVER_IGNORE_ERRORS=True)
class BasicTest(test_runner.MongoEngineTestCase):
    api_name = 'v1'
    user_username = 'test_user'
    user_password = 'foobar'
    
    user_username2 = 'test_user2'
    user_password2 = 'foobar2'

    def setUp(self):
        self.user = account_models.User.create_user(username=self.user_username, password=self.user_password)
        self.user2 = account_models.User.create_user(username=self.user_username2, password=self.user_password2)

        self.client = client.Client()
        self.assertTrue(self.client.login(username=self.user_username, password=self.user_password))
        self.client2 = client.Client()
        self.assertTrue(self.client2.login(username=self.user_username2, password=self.user_password2))

        self.updates_data = []
        signals.post_send_update.connect(self._on_update, dispatch_uid='send-update')

    def tearDown(self):
        signals.post_send_update.disconnect(dispatch_uid='send-update')
        self.updates_data = []

    def _on_update(self, channel_id, data, already_serialized, request, response, **kwargs):
        self.updates_data.append({
            'channel_id': channel_id,
            'data': data,
            'already_serialized': already_serialized,
            'request': request,
            'response': response,
        })

    def resourceListURI(self, resource_name):
        return urlresolvers.reverse('api_dispatch_list', kwargs={'api_name': self.api_name, 'resource_name': resource_name})

    def resourcePK(self, resource_uri):
        match = urlresolvers.resolve(resource_uri)
        return match.kwargs['pk']

    def resourceDetailURI(self, resource_name, resource_pk):
        return urlresolvers.reverse('api_dispatch_detail', kwargs={'api_name': self.api_name, 'resource_name': resource_name, 'pk': resource_pk})

    def fullURItoAbsoluteURI(self, uri):
        scheme, netloc, path, query, fragment = urlparse.urlsplit(uri)
        return urlparse.urlunsplit((None, None, path, query, fragment))

    def test_basic(self):
        # Creating a post

        response = self.client.post(self.resourceListURI('post'), '{"message": "Test post."}', content_type='application/json')
        self.assertEqual(response.status_code, 201)

        post_uri = response['location']

        response = self.client.get(post_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['message'], 'Test post.')
        self.assertEqual(response['author']['username'], self.user_username)
        self.assertNotEqual(response['created_time'], None)
        self.assertNotEqual(response['updated_time'], None)
        self.assertEqual(response['comments'], [])
        self.assertEqual(response['attachments'], [])
        self.assertEqual(response['is_published'], False)

        post_created_time = response['created_time']
        post_updated_time = response['updated_time']

        # Delay so next update will be for sure different
        time.sleep(1)

        # Test authorization
        response = self.client2.get(post_uri, content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # Adding an attachment

        attachments_resource_uri = self.fullURItoAbsoluteURI(post_uri) + 'attachments/'

        response = self.client.post(attachments_resource_uri, '{"link_url": "http://wlan-si.net/", "link_caption": "wlan slovenija"}', content_type='application/json; type=link')
        self.assertEqual(response.status_code, 201)

        attachment_uri = response['location']

        response = self.client.get(attachment_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['link_url'], 'http://wlan-si.net/')
        self.assertEqual(response['link_caption'], 'wlan slovenija')
        self.assertEqual(response['link_description'], '')
        self.assertEqual(response['author']['username'], self.user_username)

        response = self.client.get(post_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['attachments'][0]['link_url'], 'http://wlan-si.net/')
        self.assertEqual(response['attachments'][0]['link_caption'], 'wlan slovenija')
        self.assertEqual(response['attachments'][0]['link_description'], '')
        self.assertEqual(response['created_time'], post_created_time)
        self.assertNotEqual(response['updated_time'], post_updated_time)

        post_updated_time = response['updated_time']

        # Delay so next update will be for sure different
        time.sleep(1)

        # Publishing a post

        response = self.client.patch(post_uri, '{"is_published": true}', content_type='application/json')
        self.assertEqual(response.status_code, 202)

        response = self.client.get(post_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['is_published'], True)
        
        # Test authorization
        response = self.client2.get(post_uri, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Checking updates

        self.assertEqual(len(self.updates_data), 1)
        self.assertEqual(self.updates_data[0]['channel_id'], tasks.HOME_CHANNEL_ID)
        self.assertTrue(self.updates_data[0]['already_serialized'])

        post = json.loads(self.updates_data[0]['data'])

        self.assertEqual(post['type'], 'post_published')
        self.assertEqual(post['post']['message'], 'Test post.')
        self.assertEqual(post['post']['author']['username'], self.user_username)
        self.assertEqual(post['post']['comments'], [])
        self.assertEqual(post['post']['attachments'][0]['link_url'], 'http://wlan-si.net/')
        self.assertEqual(post['post']['attachments'][0]['link_caption'], 'wlan slovenija')
        self.assertEqual(post['post']['attachments'][0]['link_description'], '')
        self.assertEqual(post['post']['created_time'], post_created_time)
        self.assertEqual(post['post']['is_published'], True)

        # Adding a comment

        comments_resource_uri = self.fullURItoAbsoluteURI(post_uri) + 'comments/'

        response = self.client.post(comments_resource_uri, '{"message": "Test comment."}', content_type='application/json')
        self.assertEqual(response.status_code, 201)

        comment_uri = response['location']

        response = self.client.get(comment_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['message'], 'Test comment.')
        self.assertEqual(response['author']['username'], self.user_username)

        response = self.client.get(post_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['comments'][0], self.fullURItoAbsoluteURI(comment_uri))
        self.assertEqual(response['created_time'], post_created_time)
        self.assertNotEqual(response['updated_time'], post_updated_time)

    def test_notification(self):
        # Creating a post

        response = self.client.post(self.resourceListURI('post'), '{"message": "Test post for notifications.", "is_published": true}', content_type='application/json')
        self.assertEqual(response.status_code, 201)

        post_uri = response['location']

        response = self.client.get(post_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['comments'], [])
        self.assertEqual(response['is_published'], True)

        # Adding a comment

        comments_resource_uri = self.fullURItoAbsoluteURI(post_uri) + 'comments/'

        response = self.client2.post(comments_resource_uri, '{"message": "Test comment 1."}', content_type='application/json')
        self.assertEqual(response.status_code, 201)

        comment_uri = response['location']
        
        response = self.client2.get(comment_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['message'], 'Test comment 1.')

        # Verifying notification

        response = self.client.get(self.resourceListURI('notification'))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(len(response['objects']), 1)

        notification_uri = response['objects'][0]['resource_uri']

        self.assertEqual(response['objects'][0]['comment']['message'], 'Test comment 1.')
        self.assertEqual(response['objects'][0]['comment']['author']['username'], self.user_username2)
        self.assertEqual(response['objects'][0]['comment']['created_time'], response['objects'][0]['created_time'])
        self.assertEqual(response['objects'][0]['post'], self.fullURItoAbsoluteURI(post_uri))
        self.assertEqual(response['objects'][0]['read'], False)

        # Checking updates

        self.assertEqual(len(self.updates_data), 2)
        self.assertEqual(self.updates_data[0]['channel_id'], tasks.HOME_CHANNEL_ID)
        self.assertEqual(self.updates_data[1]['channel_id'], self.user.get_user_channel())
        self.assertTrue(self.updates_data[1]['already_serialized'])

        notification = json.loads(self.updates_data[1]['data'])

        self.assertEqual(notification['type'], 'notification')
        self.assertEqual(notification['notification']['comment']['message'], 'Test comment 1.')
        self.assertEqual(notification['notification']['comment']['author']['username'], self.user_username2)
        self.assertEqual(notification['notification']['post'], self.fullURItoAbsoluteURI(post_uri))
        self.assertEqual(notification['notification']['read'], False)

        # Marking notification as read

        response = self.client.patch(notification_uri, '{"read": true}', content_type='application/json')
        self.assertEqual(response.status_code, 202)

        response = self.client.get(notification_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['read'], True)

        # Testing readonly field

        created_time = response['created_time']

        response = self.client.patch(notification_uri, '{"created_time": "%s"}' % (timezone.now() + datetime.timedelta(seconds=30)).isoformat(), content_type='application/json')
        self.assertEqual(response.status_code, 202)

        response = self.client.get(notification_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        # Field has not changed
        self.assertEqual(response['created_time'], created_time)

    def test_newline_post(self):
        # Creating a post with a message containing newlines

        post = {
            'message': "Test post.\nAnother line.\nAnd another.",
        }

        response = self.client.post(self.resourceListURI('post'), json.dumps(post), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        post_uri = response['location']

        response = self.client.get(post_uri)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)

        self.assertEqual(response['message'], post['message'])
        self.assertEqual(response['author']['username'], self.user_username)
        self.assertNotEqual(response['created_time'], None)
        self.assertNotEqual(response['updated_time'], None)
        self.assertEqual(response['comments'], [])
        self.assertEqual(response['attachments'], [])
        self.assertEqual(response['is_published'], False)
