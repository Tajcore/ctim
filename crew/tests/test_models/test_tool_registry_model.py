from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from crew.models import ToolRegistryModel

User = get_user_model()


class ToolRegistryModelTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(email="admin@example.com", password="password")
        self.client.login(username="admin@example.com", password="password")
        settings.ALLOWED_TOOL_MODULE_PATHS = ["allowed.module", "another.module"]

    # Validation Tests
    def test_valid_module_path(self):
        tool = ToolRegistryModel(
            name="Tool1",
            description="A tool description",
            module_path="allowed.module.path",
            method_name="method_name",
        )
        try:
            tool.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

    def test_invalid_module_path(self):
        tool = ToolRegistryModel(
            name="Tool2",
            description="A tool description",
            module_path="invalid.module.path",
            method_name="method_name",
        )
        with self.assertRaises(ValidationError):
            tool.clean()

    def test_empty_module_path(self):
        tool = ToolRegistryModel(
            name="Tool3", description="A tool description", module_path="", method_name="method_name"
        )
        with self.assertRaises(ValidationError):
            tool.clean()

    # Boundary Tests
    def test_exact_module_prefix(self):
        tool = ToolRegistryModel(
            name="Tool4", description="A tool description", module_path="allowed.module", method_name="method_name"
        )
        try:
            tool.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

    def test_partial_module_prefix(self):
        tool = ToolRegistryModel(
            name="Tool5", description="A tool description", module_path="allowed.modul", method_name="method_name"
        )
        with self.assertRaises(ValidationError):
            tool.clean()

    # Settings Tests
    def test_validation_with_defined_paths(self):
        settings.ALLOWED_TOOL_MODULE_PATHS = ["allowed.module", "another.module"]
        tool = ToolRegistryModel(
            name="Tool6",
            description="A tool description",
            module_path="allowed.module.path",
            method_name="method_name",
        )
        try:
            tool.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

    def test_validation_with_undefined_paths(self):
        if hasattr(settings, "ALLOWED_TOOL_MODULE_PATHS"):
            delattr(settings, "ALLOWED_TOOL_MODULE_PATHS")
        tool = ToolRegistryModel(
            name="Tool7",
            description="A tool description",
            module_path="allowed.module.path",
            method_name="method_name",
        )
        with self.assertRaises(ValidationError):
            tool.clean()

    # Integration Tests
    def test_create_tool_registry_model_valid(self):
        response = self.client.post(
            reverse("admin:crew_toolregistrymodel_add"),
            {
                "name": "Tool8",
                "description": "A tool description",
                "module_path": "allowed.module.path",
                "method_name": "method_name",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirects to the change list page

    def test_create_tool_registry_model_invalid(self):
        response = self.client.post(
            reverse("admin:crew_toolregistrymodel_add"),
            {
                "name": "Tool9",
                "description": "A tool description",
                "module_path": "invalid.module.path",
                "method_name": "method_name",
            },
        )
        self.assertEqual(response.status_code, 200)  # Stays on the same page due to validation error
        self.assertContains(response, "Module path invalid.module.path is not allowed.")

    # Edge Case Tests
    def test_extremely_long_module_path(self):
        tool = ToolRegistryModel(
            name="Tool10",
            description="A tool description",
            module_path="allowed.module." + "a" * 240,
            method_name="method_name",
        )
        try:
            tool.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

    def test_special_characters_in_module_path(self):
        tool = ToolRegistryModel(
            name="Tool11",
            description="A tool description",
            module_path="allowed.module.!@#$%^&*()",
            method_name="method_name",
        )
        try:
            tool.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

    # Error Handling Tests
    def test_error_message_for_invalid_module_path(self):
        tool = ToolRegistryModel(
            name="Tool12",
            description="A tool description",
            module_path="invalid.module.path",
            method_name="method_name",
        )
        with self.assertRaises(ValidationError) as cm:
            tool.clean()
        self.assertEqual(cm.exception.messages[0], "Module path invalid.module.path is not allowed.")

    def test_error_for_missing_fields(self):
        tool = ToolRegistryModel(module_path="allowed.module.path", method_name="method_name")
        with self.assertRaises(ValidationError):
            tool.full_clean()
