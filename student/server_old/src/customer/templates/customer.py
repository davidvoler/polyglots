from string import Template


schemas = Template(
    """
    CREATE SCHEMA IF NOT EXISTS customers;
    """
)

customer_table = Template(
    """
    CREATE TABLE IF NOT EXISTS  customers.customer (
    customer_id VARCHAR(300) NOT NULL,
    name VARCHAR(300),
    phone VARCHAR(300),
    address VARCHAR(300),
    is_active BOOLEAN DEFAULT TRUE,
    create_schema BOOLEAN DEFAULT FALSE,
    langs CHAR(8)[],
    to_langs CHAR(8)[],
    admin_email VARCHAR(300),
    PRIMARY KEY (customer_id)
    );
    """
)


TABLE_TEMPLATES = [
    customer_table,
]
