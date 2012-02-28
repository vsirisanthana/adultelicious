from django.conf import settings
from django.test.client import RequestFactory
from djangorestframework.response import ErrorResponse
from djangorestframework.tests.testcases import SettingsTestCase
from serene.mixins import ReadModelMixin, UpdateModelMixin, UpdateOrCreateModelMixin
from serene.resources import ModelResource
from serene.tests.models import DummyModel

class TestMixinsBase(SettingsTestCase):
    def setUp(self):
        super(TestMixinsBase, self).setUp()
        installed_apps = tuple(settings.INSTALLED_APPS) + ('serene.tests',)
        self.settings_manager.set(INSTALLED_APPS=installed_apps)
        self.req = RequestFactory()

class TestReadMixin(TestMixinsBase):

    def test_read_model_mixin_must_return_last_modified_header(self):
        dummy = DummyModel.objects.create(name='my dum dum')

        class DummyResource(ModelResource):
            model = DummyModel

        request = self.req.get('/dummies')
        mixin = ReadModelMixin()
        mixin.resource = DummyResource

        response = mixin.get(request, dummy.id)
        self.assertEquals(dummy.name, response.cleaned_content.name)
        self.assertTrue(response.headers.has_key('Last-Modified'))
        self.assertEqual(response.headers['Last-Modified'], dummy.last_modified)

class TestUpdateModelMixin(TestMixinsBase):

    def setUp(self):
        super(TestUpdateModelMixin, self).setUp()
        self.dummy = DummyModel.objects.create(name='dummy1')

        class DummyResource(ModelResource):
            model = DummyModel
        self.mixin = UpdateModelMixin()
        self.mixin.resource = DummyResource

    def test_update_model(self):
        """
        Making sure update still working fine
        """
        dummy = DummyModel.objects.get(id=1)

        update_data = {'name': 'updated_name'}
        request = self.req.put('/dummy/1', data=update_data)
        self.mixin.CONTENT = update_data

        response = self.mixin.put(request, id=dummy.id)

        self.assertEqual(dummy.name, 'dummy1')
        self.assertEqual(response.name, 'updated_name')
        self.assertEqual(response.id, dummy.id)

        #get dummy again now it should have the new name
        dummy = DummyModel.objects.get(id=dummy.id)
        self.assertEqual(dummy.name, response.name)

    def test_update_not_exist_model_return_404(self):
        """
        When make a put request to non-existing object in update mixin model, it should return 404
        """

        with self.assertRaises(DummyModel.DoesNotExist):
            DummyModel.objects.get(id=999)

        update_data = {'name': 'new_dummy'}
        request = self.req.put('/dummy/999', data=update_data)
        self.mixin.CONTENT = update_data

        self.assertRaises(ErrorResponse, self.mixin.put, request, id=999)

class TestUpdateOrCreateModelMixin(TestMixinsBase):

    def setUp(self):
        super(TestUpdateOrCreateModelMixin, self).setUp()
        self.dummy = DummyModel.objects.create(name='dummy1')

        class DummyResource(ModelResource):
            model = DummyModel
        self.mixin = UpdateOrCreateModelMixin()
        self.mixin.resource = DummyResource

    def test_update_model(self):
        """
        Making sure update still working fine
        """
        dummy = DummyModel.objects.get(id=1)

        update_data = {'name': 'updated_name'}
        request = self.req.put('/dummy/1', data=update_data)
        self.mixin.CONTENT = update_data

        response = self.mixin.put(request, id=dummy.id)

        self.assertEqual(dummy.name, 'dummy1')
        self.assertEqual(response.name, 'updated_name')
        self.assertEqual(response.id, dummy.id)

        #get dummy again now it should have the new name
        dummy = DummyModel.objects.get(id=dummy.id)
        self.assertEqual(dummy.name, response.name)

    def test_creation_on_put_not_exist_model(self):
        """
        When make a put request to non-existing object in update or create mixin model, it should create new object
        and return 201
        """

        with self.assertRaises(DummyModel.DoesNotExist):
            DummyModel.objects.get(id=999)

        self.assertEqual(DummyModel.objects.all().count(), 1)
        update_data = {'name': 'new_dummy'}
        request = self.req.put('/dummy/999', data=update_data)
        self.mixin.CONTENT = update_data

        response = self.mixin.put(request, id=999)

        self.assertEqual(response.status, 201)
        new_dummy = DummyModel.objects.get(id=999)
        self.assertEqual(new_dummy.name, 'new_dummy')
        self.assertEqual(DummyModel.objects.all().count(), 2)



