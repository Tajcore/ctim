# Tests for django-crew factories

## Unit Tests for ToolFactory Functionality

**Validation Tests:**

- Test creating a tool instance from a valid `ToolModel` reference.
- Test that attempting to create a tool from an invalid `ToolModel` (e.g., non-existent method or module) raises an appropriate error.

**Import Tests:**

- Test that the correct module is imported based on the `module_path`.
- Test that the correct method is retrieved from the imported module.

**Boundary Tests:**

- Test creating a tool from a `ToolModel` with edge case values, such as very long module paths or method names.

**Error Handling Tests:**

- Test that appropriate exceptions are raised and handled when the module cannot be imported.
- Test that appropriate exceptions are raised and handled when the method cannot be found in the module.

---

## Unit Tests for AgentFactory Functionality

**Validation Tests:**

- Test creating an agent instance from a valid `AgentModel` reference.
- Test that all fields (role, goal, backstory) are correctly set in the created agent instance.
- Test that the agent instance includes all associated tools created by the `ToolFactory`.

**Relationship Tests:**

- Test creating an agent with multiple tools and ensure they are correctly associated.
- Test creating an agent without any tools to ensure it is handled correctly.

**Boundary Tests:**

- Test creating an agent with edge case values, such as very long strings for role, goal, and backstory.

**Error Handling Tests:**

- Test that appropriate exceptions are raised and handled when creating an agent from an invalid `AgentModel` reference.
- Test handling cases where the associated `ToolModel` instances are invalid.

---

## Unit Tests for TaskFactory Functionality

**Validation Tests:**

- Test creating a task instance from a valid `TaskModel` reference.
- Test that all fields (description, expected_output, status) are correctly set in the created task instance.
- Test that the task instance includes all associated tools created by the `ToolFactory`.
- Test that the task instance correctly includes an associated agent created by the `AgentFactory`.

**Relationship Tests:**

- Test creating a task with multiple tools and ensure they are correctly associated.
- Test creating a task without any tools to ensure it is handled correctly.
- Test creating a task with a valid agent and ensure the agent is correctly associated.

**Boundary Tests:**

- Test creating a task with edge case values, such as very long strings for description and expected_output.

**Error Handling Tests:**

- Test that appropriate exceptions are raised and handled when creating a task from an invalid `TaskModel` reference.
- Test handling cases where the associated `ToolModel` or `AgentModel` instances are invalid.

---

## Unit Tests for CrewFactory Functionality

**Validation Tests:**

- Test creating a crew instance from a valid `CrewModel` reference.
- Test that the crew instance includes all associated agents and tasks created by the `AgentFactory` and `TaskFactory`.

**Relationship Tests:**

- Test creating a crew with multiple agents and tasks and ensure they are correctly associated.
- Test creating a crew without any agents or tasks to ensure it is handled correctly.

**Boundary Tests:**

- Test creating a crew with edge case values for associated agents and tasks.

**Error Handling Tests:**

- Test that appropriate exceptions are raised and handled when creating a crew from an invalid `CrewModel` reference.
- Test handling cases where the associated `AgentModel` or `TaskModel` instances are invalid.
