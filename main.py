from pulp import *

# Prompt the user to enter the number of resources and tasks
num_resources = int(input("Enter the number of resources: "))
num_tasks = int(input("Enter the number of tasks: "))

# Initialize empty lists to store resource and task names/indices
resource_names = []
task_names = []

# Prompt the user to enter the names/indices of the resources
print("Enter the names/indices of the resources:")
for i in range(num_resources):
    name = input(f"Resource {i+1}: ")
    resource_names.append(name)

# Prompt the user to enter the names/indices of the tasks
print("Enter the names/indices of the tasks:")
for i in range(num_tasks):
    name = input(f"Task {i+1}: ")
    task_names.append(name)

# Initialize empty dictionary to store distances between resources and tasks
distances = {}

# Prompt the user to enter the distances between each resource and task
print("Enter the distances between each resource and task:")
for resource in resource_names:
    for task in task_names:
        distance = float(input(f"Distance between {resource} and {task}: "))
        distances[(resource, task)] = distance

# Initialize empty dictionary to store availability of resources
availability = {}

# Prompt the user to enter the availability of each resource for each task
print("Enter the availability of each resource for each task:")
for resource in resource_names:
    for task in task_names:
        available = int(input(f"{resource} availability for {task}: "))
        availability[(resource, task)] = available

# Initialize empty dictionary to store capacity of resources
capacity = {}

# Prompt the user to enter the capacity of each resource
print("Enter the capacity of each resource:")
for resource in resource_names:
    cap = int(input(f"Capacity of {resource}: "))
    capacity[resource] = cap

# Initialize empty dictionary to store capacity of tasks
task_capacity = {}

# Prompt the user to enter the capacity of each task
print("Enter the capacity of each task:")
for task in task_names:
    cap = int(input(f"Capacity of {task}: "))
    task_capacity[task] = cap

# Initialize the LP problem
prob = LpProblem("Task Allocation Problem", LpMinimize)

# Create decision variables
task_vars = LpVariable.dicts("Task", task_names, lowBound=0, cat='Integer')

# Define the objective function
prob += lpSum([distances[(resource, task)] * task_vars[task] for resource in resource_names for task in task_names])

# Define the capacity constraint for each resource
for resource in resource_names:
    prob += lpSum([availability[(resource, task)] * task_vars[task] for task in task_names]) <= capacity[resource]

# Define the capacity constraint for each task
for task in task_names:
    prob += task_vars[task] <= task_capacity[task]

# Solve the LP problem
prob.solve()

# Print the results
print("Task allocation:")
for task in task_names:
    for resource in resource_names:
        if task_vars[task].value() == availability[(resource, task)] and task_vars[task].value() > 0:
            print(f"{resource} is allocated to {task}")

# Print the total distance
print(f"Total distance: {value(prob.objective)}")
