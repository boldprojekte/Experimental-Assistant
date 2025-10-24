---
name: Archicad
description: Workflow guide for Archicad automation and design operations. Use for controlling Archicad instances, creating/modifying elements, querying project data, managing layers, views, or any CAD automation tasks. Critical for multi-instance management and semantic tool discovery.
---

# Archicad Workflow

Workflow guide for Archicad automation operations using the Tapir MCP Server with focus on semantic tool discovery and multi-instance management.

## Prerequisites

**IMPORTANT**: Before using Archicad tools, ensure:

1. **Archicad is running** - At least one Archicad instance must be active
2. **Tapir Add-On installed** - Required for community-developed tools access
3. **Project opened** - The Archicad instance should have a project loaded

## Tool Discovery Pattern

The Archicad MCP provides **137 tools** dynamically generated from the Tapir and official Archicad JSON APIs.

### Semantic Search Workflow

**CRITICAL**: Use semantic/natural language to find tools - the server has built-in AI-powered tool discovery.

1. **Discover Active Instances**
   - First, ask to discover active Archicad instances
   - Server returns port numbers for each running instance
   - Note the port number for your target instance

2. **Describe Intent in Natural Language**
   - Instead of knowing exact tool names, describe what you want to do
   - Example: "create a wall" instead of searching for specific API endpoints
   - The semantic search engine finds relevant tools locally

3. **Execute with Port Context**
   - Specify the instance port when calling tools
   - Format: Use the port identifier from discovery step

**Examples:**
- "Show all layers in the current project on port 19723"
- "Create a rectangular wall 5m long on instance 19723"
- "Get all windows in the project from port 19723"

## Multi-Instance Management

**IMPORTANT**: The server supports multiple simultaneous Archicad instances.

### Instance Discovery

Always start by discovering active instances:
- Tool will report all running Archicad instances with their port numbers
- Each instance represents a separate project
- Use port numbers to target specific projects

### Working with Multiple Projects

When multiple instances are running:
1. First discover all instances to see available ports
2. Ask user which instance to work with if unclear
3. Clearly reference the port number in all operations
4. Keep track of which operations were performed on which instance

**Example Workflow:**
```
User: "Add a door to the project"
Assistant: Let me first discover active Archicad instances...
[Discovers ports 19723, 19724]
Assistant: I found 2 running instances (ports 19723, 19724).
          Which project should I modify?
User: The one on 19723
Assistant: [Proceeds with door creation on port 19723]
```

## Tool Categories

The 137 available tools cover these main categories:

### Element Operations
- Creating elements (walls, doors, windows, slabs, roofs, etc.)
- Modifying element properties
- Deleting elements
- Querying element information
- Element selection and filtering

### Project Management
- Layer management
- View management
- Story/floor management
- Building material queries
- Classification systems

### Data Operations
- Exporting project data
- Importing data
- Property queries
- Quantity takeoffs
- Schedule generation

### 3D/Visualization
- 3D model queries
- Camera positions
- Rendering settings
- Visualization states

## Operational Principles

### 1. Always Discover First

Before any operation:
- Discover active instances
- Confirm correct instance/port
- Verify project is loaded

### 2. Use Natural Language for Tools

Don't try to memorize tool names:
- Describe what you want to do
- Let semantic search find the right tool
- Trust the local AI-powered matching

### 3. Port-Specific Operations

Always specify the port:
- Include port in all API calls
- Track which port is which project
- Ask user if multiple instances exist

### 4. Offline & Private

All operations are local:
- No data leaves the computer
- Semantic search runs locally
- Direct connection to Archicad instances

### 5. Error Handling

If tools fail:
- Verify Archicad instance is still running
- Check if project is still open
- Confirm Tapir Add-On is active
- Try rediscovering instances

## Common Workflows

### Creating Elements

1. Discover instances → Get port
2. Describe element to create in natural language
3. Provide dimensions/properties
4. Execute on specified port

### Querying Project Data

1. Discover instances → Get port
2. Describe what data you need
3. Filter/specify criteria if needed
4. Retrieve data from specified port

### Modifying Existing Elements

1. Discover instances → Get port
2. Query/select target elements
3. Describe modifications needed
4. Apply changes on specified port

### Batch Operations

For multiple similar operations:
- Use semantic search to find bulk/batch tools
- Describe the repetitive task
- Execute with proper parameters

## Best Practices

1. **Start Simple** - Begin with discovery, then simple queries before complex modifications
2. **Verify Before Modify** - Query elements before changing them
3. **Use Descriptive Language** - The more context in your request, the better the tool matching
4. **Track Instances** - Keep mental note of which port is which project
5. **Alpha Software** - This is experimental - expect occasional issues

## Integration with Existing Workflow

### Project Documentation

After Archicad operations, consider:
- Document changes in `Dokumente/01_in Arbeit/`
- Create task lists in `Aufgaben/` for complex workflows
- Use ClickUp for project tracking

### Combining Tools

Archicad works well with:
- **Browser** - Screenshot Archicad for documentation
- **ClickUp** - Track design tasks and changes
- **Scripts** - Export/convert Archicad data
- **RAG** - Index Archicad documentation for reference

## Troubleshooting

### No Instances Found
- Ensure Archicad is running
- Check Tapir Add-On is loaded
- Try restarting Archicad

### Tool Not Found
- Rephrase request in natural language
- Be more specific about the operation
- Check Archicad API documentation

### Connection Lost
- Verify Archicad didn't close
- Rediscover instances
- Check port numbers haven't changed

### Unexpected Results
- Verify correct instance/port
- Check element selection criteria
- Review Archicad project state

## Core Principles

1. **Discover → Describe → Execute** - Always follow this workflow
2. **Natural language over exact tool names** - Let semantic search work
3. **Port awareness** - Always know which instance you're working with
4. **Local & private** - All processing happens on your machine
5. **Experimental approach** - Test carefully, verify results
