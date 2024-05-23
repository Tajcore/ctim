import random
import time

from django.test import TestCase

from ctim.ctia.models.ransomware import Group
from ctim.ctia.serializers import GroupDetailSerializer


class GroupSerializerPerformanceTestCase(TestCase):
    def setUp(self):
        # Create a large dataset of groups
        self.num_groups = 10000
        self.groups = []
        for i in range(self.num_groups):
            group = Group.objects.create(name=f"TestGroup{i}", description=f"Description for TestGroup{i}")
            self.groups.append(group)

    def test_group_detail_serializer_performance(self):
        # Test case: Measure performance of GroupDetailSerializer with a large dataset
        start_time = time.time()
        num_queries = 100  # Number of groups to query randomly
        for _ in range(num_queries):
            random_group = random.choice(self.groups)
            random_group.name = self.randomize_case(random_group.name)  # Randomly change the case
            serializer = GroupDetailSerializer(data={"name": random_group.name})
            serializer.is_valid()  # Validate the serializer
            serializer.validated_data
        end_time = time.time()
        elapsed_time = end_time - start_time
        # Assert that the elapsed time is under 0.5 seconds
        max_time = 0.5  # Maximum allowed time in seconds
        self.assertLess(elapsed_time, max_time, f"Elapsed time exceeds {max_time} seconds")

    def randomize_case(self, name):
        # Randomly change the case of the group name
        return "".join(random.choice([c.upper(), c.lower()]) for c in name)
