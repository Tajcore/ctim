from django.test import TestCase

from ctim.ctia.models.ransomware import Group
from ctim.ctia.serializers import GroupListSerializer


class GroupListSerializerTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.group1 = Group.objects.create(name="TestGroup1", description="Test description 1")
        self.group2 = Group.objects.create(name="TestGroup2", description="Test description 2")

    def test_group_list_serializer_retrieval(self):
        serializer = GroupListSerializer(instance=[self.group1, self.group2], many=True)
        data = serializer.data
        # Assert that both group names are preserved as stored in the database
        self.assertEqual(data[0]["name"], "TestGroup1")
        self.assertEqual(data[1]["name"], "TestGroup2")
