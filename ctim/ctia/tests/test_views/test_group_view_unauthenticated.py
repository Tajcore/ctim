from django.test import RequestFactory

from ctim.ctia.models.ransomware import Group
from ctim.ctia.serializers import GroupDetailSerializer
from ctim.ctia.views import GroupViewSet


class TestGroupViewSet:
    # The class should be able to retrieve a Group object by ID.
    def test_retrieve_group_by_id(self):
        group = Group.objects.create(name="Test Group", description="Test Description")
        viewset = GroupViewSet()
        request = RequestFactory().get(f"/groups/{group.id}/")
        response = viewset.retrieve(request, pk=group.id)
        assert response.status_code == 200
        assert response.data["id"] == group.id
        assert response.data["name"] == group.name
        assert response.data["description"] == group.description

    # The class should handle the case where no Group objects exist.
    def test_no_group_objects_exist(self):
        viewset = GroupViewSet()
        request = RequestFactory().get("/groups/")
        response = viewset.list(request)
        assert response.status_code == 200
        assert len(response.data) == 0

    # The class should be able to retrieve a Group object by ID.
    def test_retrieve_group_by_id_serializer_class(self):
        # Initialize GroupViewSet
        view = GroupViewSet()

        # Set up necessary dependencies
        view.action = "retrieve"
        view.request = type("Request", (), {"query_params": {}})()

        # Invoke the get_serializer_class method
        serializer_class = view.get_serializer_class()

        # Assert that the serializer class is GroupDetailSerializer
        assert serializer_class == GroupDetailSerializer
