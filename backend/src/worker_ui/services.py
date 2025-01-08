from admins_panel.models import Worker, Operations

def process_operation(worker_id, operation_id, quantity):
    worker = Worker.objects.get(id=worker_id)
    operation = Operations.objects.get(id=operation_id)
    amount = operation.price * quantity
    worker.add_salary(amount)

def pay_salary(worker_id, amount):
    worker = Worker.objects.get(id=worker_id)
    worker.deduct_salary(amount)

