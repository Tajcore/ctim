import unittest
from unittest.mock import patch, MagicMock
from crew.factories import ToolFactory
from crew.models import ToolModel, ToolRegistryModel
from django.core.exceptions import ValidationError
from factory.django import DjangoModelFactory
import factory

class ToolRegistryModelFactory(DjangoModelFactory):
    class Meta:
        model = ToolRegistryModel

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    module_path = "some_module"
    method_name = "some_method"

class ToolModelFactory(DjangoModelFactory):
    class Meta:
        model = ToolModel

    registry = factory.SubFactory(ToolRegistryModelFactory)

class ToolFactoryTests(unittest.TestCase):

    def setUp(self):
        self.tool_registry = ToolRegistryModelFactory.create()
        self.tool = ToolModelFactory.create(registry=self.tool_registry)

    # Validation Tests
    @patch('importlib.import_module')
    def test_create_tool_instance_from_valid_tool_model(self, mock_import_module):
        mock_module = MagicMock()
        mock_method = MagicMock()
        mock_import_module.return_value = mock_module
        setattr(mock_module, self.tool.registry.method_name, mock_method)
        
        tool_instance = ToolFactory.create(self.tool)
        self.assertEqual(tool_instance, mock_method)

    @patch('importlib.import_module')
    def test_create_tool_from_invalid_tool_model_raises_error(self, mock_import_module):
        mock_import_module.side_effect = ModuleNotFoundError
        self.tool.registry.module_path = "invalid_module"
        with self.assertRaises(ModuleNotFoundError):
            ToolFactory.create(self.tool)

    # Import Tests
    @patch('importlib.import_module')
    def test_correct_module_imported_based_on_module_path(self, mock_import_module):
        mock_module = MagicMock()
        mock_import_module.return_value = mock_module
        
        ToolFactory.create(self.tool)
        mock_import_module.assert_called_with(self.tool.registry.module_path)

    @patch('importlib.import_module')
    def test_correct_method_retrieved_from_imported_module(self, mock_import_module):
        mock_module = MagicMock()
        mock_method = MagicMock()
        mock_import_module.return_value = mock_module
        setattr(mock_module, self.tool.registry.method_name, mock_method)
        
        tool_instance = ToolFactory.create(self.tool)
        self.assertEqual(tool_instance, mock_method)

    # Boundary Tests
    @patch('importlib.import_module')
    def test_create_tool_with_long_module_path_and_method_name(self, mock_import_module):
        self.tool.registry.module_path = "a" * 255
        self.tool.registry.method_name = "b" * 255
        mock_module = MagicMock()
        mock_method = MagicMock()
        mock_import_module.return_value = mock_module
        setattr(mock_module, self.tool.registry.method_name, mock_method)
        
        tool_instance = ToolFactory.create(self.tool)
        self.assertEqual(tool_instance, mock_method)

    # Error Handling Tests
    @patch('importlib.import_module')
    def test_module_import_error_handling(self, mock_import_module):
        mock_import_module.side_effect = ModuleNotFoundError
        with self.assertRaises(ModuleNotFoundError):
            ToolFactory.create(self.tool)

    @patch('importlib.import_module')
    def test_method_not_found_error_handling(self, mock_import_module):
        mock_module = MagicMock()
        mock_import_module.return_value = mock_module
        delattr(mock_module, self.tool.registry.method_name)
        
        with self.assertRaises(AttributeError):
            ToolFactory.create(self.tool)

if __name__ == "__main__":
    unittest.main()
