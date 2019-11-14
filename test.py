from sqlite.operation_functions import Operations

op = Operations()

id = "6789876545678"
check = op.check_user_exist_id(id)
op.conn.close()
print(check)