# flake8: noqa

# create_test_data_with_tools.py

import os
from datetime import datetime

import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from crew.models import AgentModel, CrewModel, ExecutionResultModel, TaskModel, ToolModel, ToolRegistryModel

# Clear existing data
AgentModel.objects.all().delete()
TaskModel.objects.all().delete()
CrewModel.objects.all().delete()
ExecutionResultModel.objects.all().delete()
ToolRegistryModel.objects.all().delete()
ToolModel.objects.all().delete()

# Create Tool Registry Entries
directory_tool = ToolRegistryModel.objects.create(
    name="DirectoryReadTool",
    description="Reads files from a specified directory.",
    module_path="crewai_tools",
    method_name="DirectoryReadTool",
)

file_tool = ToolRegistryModel.objects.create(
    name="FileReadTool",
    description="Reads content from a specified file.",
    module_path="crewai_tools",
    method_name="FileReadTool",
)

search_tool = ToolRegistryModel.objects.create(
    name="SerperDevTool",
    description="Searches the internet using SerperDev.",
    module_path="crewai_tools",
    method_name="SerperDevTool",
)

web_rag_tool = ToolRegistryModel.objects.create(
    name="WebsiteSearchTool",
    description="Searches websites for relevant content.",
    module_path="crewai_tools",
    method_name="WebsiteSearchTool",
)

# Create Tools
directory_tool_instance = ToolModel.objects.create(registry=directory_tool)
file_tool_instance = ToolModel.objects.create(registry=file_tool)
search_tool_instance = ToolModel.objects.create(registry=search_tool)
web_rag_tool_instance = ToolModel.objects.create(registry=web_rag_tool)

# Create Agents and link tools
planner = AgentModel.objects.create(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article about the topic: {topic}. You collect information that helps the audience learn something and make informed decisions. Your work is the basis for the Content Writer to write an article on this topic.",
)
planner.tools.set([search_tool_instance, web_rag_tool_instance])

writer = AgentModel.objects.create(
    role="Content Writer",
    goal="Write insightful and factually accurate opinion piece about the topic: {topic}",
    backstory="You're working on writing a new opinion piece about the topic: {topic}. You base your writing on the work of the Content Planner, who provides an outline and relevant context about the topic. You follow the main objectives and direction of the outline, as provided by the Content Planner. You also provide objective and impartial insights and back them up with information provided by the Content Planner. You acknowledge in your opinion piece when your statements are opinions as opposed to objective statements.",
)
writer.tools.set([directory_tool_instance, file_tool_instance])

editor = AgentModel.objects.create(
    role="Editor",
    goal="Edit a given blog post to align with the writing style of the organization.",
    backstory="You are an editor who receives a blog post from the Content Writer. Your goal is to review the blog post to ensure that it follows journalistic best practices, provides balanced viewpoints when providing opinions or assertions, and also avoids major controversial topics or opinions when possible.",
)

# Create Tasks
plan_task = TaskModel.objects.create(
    name="Content Planning Task",
    description=(
        "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering their interests and pain points.\n"
        "3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.",
    status="Pending",
    agent=planner,
)

write_task = TaskModel.objects.create(
    name="Content Writing Task",
    description=(
        "1. Use the content plan to craft a compelling blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
        "3. Sections/Subtitles are properly named in an engaging manner.\n"
        "4. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and alignment with the brand's voice."
    ),
    expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
    status="Pending",
    agent=writer,
)

edit_task = TaskModel.objects.create(
    name="Content Editing Task",
    description=("Proofread the given blog post for grammatical errors and alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
    status="Pending",
    agent=editor,
)

# Create Crew
crew = CrewModel.objects.create(name="Content Creation Crew", status="Pending")
crew.agents.set([planner, writer, editor])
crew.tasks.set([plan_task, write_task, edit_task])

print("Test data with tools created successfully.")
