from django.test import TestCase

from ctim.ctia.models.ransomware import Group
from ctim.ctia.serializers import GroupDetailSerializer


class GroupDetailSerializerTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.group1 = Group.objects.create(name="TestGroup1", description="Test description 1")

    def test_group_detail_serializer_retrieval(self):
        serializer = GroupDetailSerializer(instance=self.group1)
        data = serializer.data
        # Assert that the group name is preserved as stored in the database
        self.assertEqual(data["name"], "TestGroup1")


class GroupDetailSerializerErrorHandlingTestCase(TestCase):
    def test_group_detail_serializer_non_existent_group(self):
        # Test case: Serializer should handle non-existent group names gracefully
        serializer = GroupDetailSerializer(data={"name": "NonExistentGroup"})
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.validated_data.get("name"))

    def test_group_detail_serializer_empty_group_name(self):
        # Test case: Serializer should handle empty input group names gracefully
        serializer = GroupDetailSerializer(data={"name": ""})
        self.assertFalse(serializer.is_valid())
        self.assertIsNone(serializer.validated_data.get("name"))
