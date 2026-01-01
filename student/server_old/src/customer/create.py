from utils.db import get_pg_con, get_schema

async def execute_sql(queries: list):
    conn = await get_pg_con()
    for sql in queries:
        try:
            await conn.execute(sql)
        except Exception as e:
            print(f"Error executing SQL: {sql}")
            print(e)
    await conn.commit()
    conn.close()

async def create_customer_schemas(customer_id: str):
    from customer.templates.schema import schemas
    schemas_sql = schemas.substitute(customer_id=customer_id)
    await execute_sql([schemas_sql])

async def create_customer_quiz(customer_id: str):
    from customer.templates.quiz_tables import TABLE_TEMPLATES
    queries = []
    for table in TABLE_TEMPLATES:
        queries.append(table.substitute(customer_id=customer_id))
    await execute_sql(queries)

async def create_customer_content(customer_id: str):
    from customer.templates.content_tables import TABLE_TEMPLATES
    queries = []
    for table in TABLE_TEMPLATES:
        queries.append(table.substitute(customer_id=customer_id))
    await execute_sql(queries)

async def create_customer_users(customer_id: str):
    from customer.templates.users import TABLE_TEMPLATES
    queries = []
    for table in TABLE_TEMPLATES:
        queries.append(table.substitute(customer_id=customer_id))
    await execute_sql(queries)


async def create_customer_tables()-> str:
    """
    Create all customer information"""
    pass



async def create_customer(customer_id: str, name: str, admin_email: str, address: str):
    # sql = f"""
    # INSERT INTO customers.customer (customer_id, name, admin_email, address,  create_schema, is_active )
    # VALUES ('{customer_id}','{name}', '{admin_email}','{address}', TRUE, TRUE)
    # """   
    # await execute_sql([sql])
    await create_customer_schemas(customer_id)
    await create_customer_quiz(customer_id)
    await create_customer_content(customer_id)
    await create_customer_users(customer_id)



async def create_base_tables():
    from customer.templates.customer import schemas, TABLE_TEMPLATES
    queries = []
    queries.append(schemas.substitute())
    for table in TABLE_TEMPLATES:
        queries.append(table.substitute())
    await execute_sql(queries)








