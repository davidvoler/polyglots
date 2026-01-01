from string import Template


schemas = Template(
    """
    CREATE SCHEMA IF NOT EXISTS ${customer_id}_quiz;
    CREATE SCHEMA IF NOT EXISTS ${customer_id}_content;
    CREATE SCHEMA IF NOT EXISTS ${customer_id}_users;
    """
)
