# Project Title

Django-Crew

## Brief Description

Django-Crew is a Django-based application designed to manage and execute complex tasks by coordinating multiple agents and tools. The application provides an administrative interface for configuring agents, tasks, tools, and crews, as well as monitoring their execution results.

## Features

- **Agent Management**: Define and configure agents with specific roles, goals, and associated tools.
- **Task Management**: Create and assign tasks to agents, specifying detailed descriptions and expected outputs.
- **Tool Integration**: Register and manage tools that agents can use to perform their tasks.
- **Crew Coordination**: Organize agents and tasks into crews for coordinated execution.
- **Execution Monitoring**: Track the execution status and results of tasks and crews, with detailed logging and error handling.
- **Admin Interface**: Use the Django admin interface to manage all entities and monitor execution results.

## Installation Instructions

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/thompsonson/ctim.git
   cd ctim
   ```

2. **Build the Docker Images**:
   ```sh
   make build
   ```

3. **Start the Docker Containers**:
   ```sh
   make up
   ```

4. **Apply Database Migrations**:
   ```sh
   make migrate
   ```

5. **Create a Superuser**:
   ```sh
   make createsu
   ```

6. **Access the Admin Interface**:
   Open a browser and navigate to `http://localhost:8000/admin`, then log in with the superuser credentials.

## Usage Examples

### Creating and Managing Tools

1. **Register a New Tool**:
   - Navigate to the Tool Registry section in the admin interface.
   - Click "Add Tool Registry Model".
   - Fill in the details (name, description, module path, method name) and save.

2. **Create Tool Instances**:
   - Navigate to the Tools section in the admin interface.
   - Click "Add Tool Model".
   - Select the corresponding tool registry entry and save.

### Creating Agents and Assigning Tools

1. **Add a New Agent**:
   - Navigate to the Agents section in the admin interface.
   - Click "Add Agent Model".
   - Fill in the details (role, goal, backstory) and save.

2. **Assign Tools to an Agent**:
   - After creating an agent, edit the agent entry.
   - Add the desired tools to the agent and save.

### Organizing Tasks and Crews

1. **Create a Task**:
   - Navigate to the Tasks section in the admin interface.
   - Click "Add Task Model".
   - Fill in the task details (name, description, expected output) and assign an agent.
   - Save the task.

2. **Form a Crew**:
   - Navigate to the Crews section in the admin interface.
   - Click "Add Crew Model".
   - Fill in the crew details and associate agents and tasks.
   - Save the crew.

### Executing and Monitoring Tasks

1. **Kick Off Crew Tasks**:
   - Navigate to the Crews section in the admin interface.
   - Select the desired crew(s) and choose the "Kick off selected crew tasks" action from the dropdown.
   - Confirm the action to start the execution.

2. **Monitor Execution Results**:
   - Navigate to the Execution Results section in the admin interface.
   - View the details of execution results, including status, timestamps, and outputs.

## Configuration Options

- **Allowed Tool Module Paths**: Define the permissible module paths for tool registrations in your Django settings using `ALLOWED_TOOL_MODULE_PATHS`.
- **Sentry Integration**: Configure Sentry for error monitoring by setting `SENTRY_DSN` in your Django settings.
- **Task Time Logging**: Enable task execution time logging to Sentry by setting `TASK_SEND_TIME_TO_SENTRY` in your Django settings.

## Contribution Guidelines

1. **Fork the Repository**:
   - Click on the fork button at the top right corner of the repository page.

2. **Create a Feature Branch**:
   ```sh
   git checkout -b feature-branch-name
   ```

3. **Commit Your Changes**:
   ```sh
   pre-commit install # only need be run the first time
   git commit -m "feat|fix|chore|etc...: Description of your changes using conventional commit descriptions"
   ```

4. **Push to Your Branch**:
   ```sh
   git push origin feature-branch-name
   ```

5. **Create a Pull Request**:
   - Navigate to the original repository and click on the "New Pull Request" button.

## Testing Instructions

1. **Run Unit Tests**:
   ```sh
   make test
   ```

2. **Specific Test Suites**:
   - To run tests for specific modules, use:
     ```sh
     make test crew.tests.<test_module>
     ```

3. **Test Coverage**:
   - Ensure all tests pass and maintain high test coverage for new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements/Credits

- Django: The web framework used for developing this application.
- Celery: For managing asynchronous task execution.
- LangChain: Python LLM orchestration library.
- Crew: A nice LangChain wrapper, providing easily configurable abstractions.

Feel free to contribute and improve this project. Your feedback and suggestions are highly appreciated!
