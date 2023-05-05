class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False


class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)

    def complete_task(self, index):
        self.tasks[index].completed = True

    def delete_task(self, index):
        del self.tasks[index]

    def display_all_tasks(self):
        for i, task in enumerate(self.tasks):
            status = "completed" if task.completed else "not completed"
            print(f"{i+1}. {task.title}: {task.description} ({status})")


class TestTodoList:
    def test_add_task(self):
        todo_list = TodoList()
        todo_list.add_task("Do laundry", "Wash the clothes")
        assert len(todo_list.tasks) == 1
        assert todo_list.tasks[0].title == "Do laundry"
        assert todo_list.tasks[0].description == "Wash the clothes"
        assert not todo_list.tasks[0].completed

    def test_complete_task(self):
        todo_list = TodoList()
        todo_list.add_task("Do laundry", "Wash the clothes")
        todo_list.add_task("Buy groceries", "Milk, bread, eggs")
        todo_list.complete_task(0)
        assert todo_list.tasks[0].completed
        assert not todo_list.tasks[1].completed

    def test_delete_task(self):
        todo_list = TodoList()
        todo_list.add_task("Do laundry", "Wash the clothes")
        todo_list.add_task("Buy groceries", "Milk, bread, eggs")
        todo_list.delete_task(0)
        assert len(todo_list.tasks) == 1
        assert todo_list.tasks[0].title == "Buy groceries"

    def test_display_all_tasks(self, capsys):
        todo_list = TodoList()
        todo_list.add_task("Do laundry", "Wash the clothes")
        todo_list.add_task("Buy groceries", "Milk, bread, eggs")
        todo_list.complete_task(0)
        todo_list.display_all_tasks()
        captured = capsys.readouterr()
        assert "1. Do laundry: Wash the clothes (completed)" in captured.out
        assert "2. Buy groceries: Milk, bread, eggs (not completed)" in captured.out

    def test_add_test_delete(self):
        todo_list = TodoList()
        todo_list.add_task("Do laundry", "Wash the clothes")
        todo_list.add_task("Buy groceries", "Milk, bread, eggs")
        todo_list.delete_task(1)
        todo_list.delete_task(0)
        assert len(todo_list.tasks) == 0
