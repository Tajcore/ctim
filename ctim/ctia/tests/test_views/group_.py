from django.urls import reverse
from rest_framework.test import APITestCase

from ctim.ctia.models.ransomware import Group
from ctim.ctia.serializers import GroupDetailSerializer, GroupListSerializer


class GroupViewSetTestCase(APITestCase):
    def setUp(self):
        # Create test data
        self.group1 = Group.objects.create(name="TestGroup1", description="Test description 1")
        self.group2 = Group.objects.create(name="TestGroup2", description="Test description 2")

    def test_group_list_view(self):
        url = reverse("group-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        serializer = GroupListSerializer(instance=[self.group1, self.group2], many=True)
        print(response.data)
        print(serializer.data)
        self.assertEqual(response.data, serializer.data)

    def test_group_detail_view(self):
        url = reverse("group-detail", args=[self.group1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        serializer = GroupDetailSerializer(instance=self.group1)
        self.assertEqual(response.data, serializer.data)
