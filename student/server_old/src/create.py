from customer.create import create_base_tables, create_customer
import asyncio



# 
# asyncio.run(create_base_tables())
asyncio.run(create_customer("polyglots", name="polyglots", admin_email="david@polyglots.social", address=""))



