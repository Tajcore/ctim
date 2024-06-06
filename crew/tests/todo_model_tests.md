# Tests for django-crew models

## Unit Tests for Tool Registry Model Functionality

**Validation Tests:**

- Test that a valid `module_path` (from an allowed module or submodule) passes validation.
- Test that an invalid `module_path` (not from an allowed module or submodule) fails validation.
- Test that an empty `module_path` fails validation.

**Boundary Tests:**

- Test that a `module_path` which exactly matches an allowed module prefix passes validation.
- Test that a `module_path` which partially matches an allowed module prefix but isn’t a valid submodule fails validation.

**Settings Tests:**

- Test that validation logic uses the paths defined in `ALLOWED_TOOL_MODULE_PATHS` from the settings.
- Test that validation logic handles the case when `ALLOWED_TOOL_MODULE_PATHS` is not defined in the settings (e.g., defaults to an empty list).

**Integration Tests:**

- Test creating a `ToolRegistryModel` instance via the Django admin interface with a valid `module_path`.
- Test creating a `ToolRegistryModel` instance via the Django admin interface with an invalid `module_path`.

**Edge Case Tests:**

- Test with extremely long `module_path` strings to ensure validation handles them correctly.
- Test with special characters in `module_path` to ensure they are processed correctly.

**Error Handling Tests:**

- Test that appropriate error messages are displayed when validation fails for `module_path`.
- Test that creating a `ToolRegistryModel` instance with missing fields raises the appropriate validation errors.

## Unit Tests for AgentModel Functionality

**Validation Tests:**

- Test that an `AgentModel` instance with valid fields (role, goal, backstory) passes validation.
- Test that an `AgentModel` instance with missing required fields (e.g., no role) fails validation.
- Test that `tools` field correctly accepts multiple `ToolModel` instances.

**Relationship Tests:**

- Test adding multiple tools to an agent and ensure they are correctly associated.
- Test removing a tool from an agent and ensure the association is correctly updated.

**Integration Tests:**

- Test creating an `AgentModel` instance via the Django admin interface with valid data.
- Test updating an `AgentModel` instance via the Django admin interface to add/remove tools.

**Edge Case Tests:**

- Test creating an agent with very long strings for role, goal, and backstory to ensure they are handled correctly.
- Test assigning an empty set of tools to an agent to ensure it is handled correctly.

**Error Handling Tests:**

- Test that appropriate error messages are displayed when validation fails for missing or invalid fields.
- Test handling of duplicate tool entries for the same agent (e.g., the same tool added twice).

---

## Unit Tests for TaskModel Functionality

**Validation Tests:**

- Test that a `TaskModel` instance with valid fields (description, expected_output, status) passes validation.
- Test that a `TaskModel` instance with missing required fields (e.g., no description) fails validation.
- Test that `tools` field correctly accepts multiple `ToolModel` instances.
- Test that the `agent` field correctly accepts an `AgentModel` instance.

**Relationship Tests:**

- Test associating multiple tools with a task and ensure they are correctly linked.
- Test changing the agent of a task and ensure the association is updated correctly.

**Integration Tests:**

- Test creating a `TaskModel` instance via the Django admin interface with valid data.
- Test updating a `TaskModel` instance via the Django admin interface to add/remove tools and change agents.

**Edge Case Tests:**

- Test creating a task with very long strings for description and expected_output to ensure they are handled correctly.
- Test assigning an empty set of tools to a task to ensure it is handled correctly.

**Error Handling Tests:**

- Test that appropriate error messages are displayed when validation fails for missing or invalid fields.
- Test handling of duplicate tool entries for the same task (e.g., the same tool added twice).

---

## Unit Tests for CrewModel Functionality

**Validation Tests:**

- Test that a `CrewModel` instance with valid fields (status) passes validation.
- Test that a `CrewModel` instance with missing required fields (e.g., no status) fails validation.
- Test that `agents` field correctly accepts multiple `AgentModel` instances.
- Test that `tasks` field correctly accepts multiple `TaskModel` instances.

**Relationship Tests:**

- Test adding multiple agents to a crew and ensure they are correctly associated.
- Test adding multiple tasks to a crew and ensure they are correctly associated.

**Integration Tests:**

- Test creating a `CrewModel` instance via the Django admin interface with valid data.
- Test updating a `CrewModel` instance via the Django admin interface to add/remove agents and tasks.

**Edge Case Tests:**

- Test creating a crew with an empty set of agents and tasks to ensure it is handled correctly.
- Test updating a crew to add a large number of agents and tasks to check performance.

**Error Handling Tests:**

- Test that appropriate error messages are displayed when validation fails for missing or invalid fields.
- Test handling of duplicate agent and task entries for the same crew (e.g., the same agent or task added twice).

---

## Unit Tests for ExecutionResultModel Functionality

**Validation Tests:**

- Test that an `ExecutionResultModel` instance with valid fields (status, result_data) passes validation.
- Test that an `ExecutionResultModel` instance with missing required fields (e.g., no status) fails validation.
- Test that the `crew` field correctly accepts a `CrewModel` instance.

**Relationship Tests:**

- Test associating an execution result with a crew and ensure it is correctly linked.

**Integration Tests:**

- Test creating an `ExecutionResultModel` instance via the Django admin interface with valid data.
- Test updating an `ExecutionResultModel` instance via the Django admin interface to change the status and result_data.

**Edge Case Tests:**

- Test creating an execution result with very long strings for status and result_data to ensure they are handled correctly.
- Test creating multiple execution results for the same crew to check if it is handled correctly.

**Error Handling Tests:**

- Test that appropriate error messages are displayed when validation fails for missing or invalid fields.
- Test handling of duplicate execution results for the same crew (if not allowed).
