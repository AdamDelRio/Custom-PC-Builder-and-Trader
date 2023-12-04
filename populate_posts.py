import sqlalchemy
import os
from json import load
import dotenv
from faker import Faker
import numpy as np
import multiprocessing
import random


def database_connection_url():
    dotenv.load_dotenv('passwords.env')
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


def edit_prices():
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    with engine.begin() as connection:
        sql = 'SELECT part_id, price from internal_hard_drive_specs'
        result = connection.execute(statement=sqlalchemy.text(sql))
        result = result.all()

        part_dict = {row[0]: (int(str(round(row[1], 2)).split(".")[0]), int(str(round(row[1], 2)).split(".")[1])) for row in result}
        
        for value in part_dict:
            sql = f"UPDATE part_inventory SET dollars = :dollars, cents = :cents WHERE part_id = :part_id"
            parameters = {
                "part_id": value,
                "dollars": part_dict[value][0] if part_dict[value][0] else 0,
                "cents": part_dict[value][1] if part_dict[value][1] else 0
            }
            result = connection.execute(statement=sqlalchemy.text(sql),parameters=parameters)

def add_rows():
    filename = 'internal_hard_drive.json'

    path = f"./src/data/json/{filename}"
    with open(path, "r") as f:
        data = load(f)
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)
    
    with engine.begin() as conn:
        part_type = filename.split(".")[0]
        schemas = [key for key in data[0].keys()]
        for value in data:
            sql = f"INSERT into part_inventory (name, type, quantity) VALUES (:name, :type, :quantity) RETURNING part_id"
            parameters = {
                "name":str(value["name"]),
                "type":str(part_type),
                "quantity":0
            }
            result = conn.execute(statement=sqlalchemy.text(sql),parameters=parameters)
            part_id = result.first()[0]
            #if price = null, skip this iteration of the loop
            if value["price"] == None:
                continue 
            sql = f"INSERT into {part_type}_specs (part_id, {', '.join(schemas)}) VALUES (:part_id,{', '.join([f':{column_name}' for column_name in schemas])})"
            parameters = {
                "part_id": part_id,
            }
            for schema in schemas:
                parameters[schema] = value[schema]
            
            result = conn.execute(statement=sqlalchemy.text(sql),parameters=parameters)

def randomize_quantity():
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    #iterate through all items in part_inventory and update quantity to a random number between 0 and 100
    with engine.begin() as conn:
        parts = conn.execute(sqlalchemy.text("""
        SELECT * FROM part_inventory;
        """)).fetchall()

        for part in parts:
            quantity = np.random.randint(0, 100)
            conn.execute(sqlalchemy.text("""
            UPDATE part_inventory SET quantity = :quantity WHERE part_id = :part_id;
            """), {"quantity": quantity, "part_id": part[0]})

def add_users(num_users):
    # Create a new DB engine based on our connection string
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()

    # create fake posters with fake names and birthdays
    with engine.begin() as conn:
        print("adding users")
        posts = []
        for i in range(num_users):
            # if (i % 1000 == 0):
            #     print(i)
            

            email = fake.unique.email()
            username = email.split('@')[0]
            # check if username exists. Return bool true/false
            while True:
                username_exists = conn.execute(sqlalchemy.text("""
                SELECT * FROM users WHERE username = :username;
                """), {"username": username}).fetchone()
                if username_exists:
                    email = fake.unique.email()
                    username = email.split('@')[0]
                else:
                    break

            # if username exists, skip this iteration of the loop
            id = conn.execute(sqlalchemy.text("""
            INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id;
            """), {"username": username, "email": email, }).fetchone()[0]

            conn.execute(sqlalchemy.text("""
            INSERT INTO customers (name, address, phone, user_id) VALUES (:name, :address, :phone, :user_id);
            """), {"name": fake.name(), "address": fake.address(), "phone": fake.phone_number(), "user_id": id})

def add_case_specs(num_cases):
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()
    companies = [fake.company() for _ in range(5)]
    # create fake posters with fake names and birthdays
    with engine.begin() as conn:
        print("adding cases")
        posts = []
        for i in range(num_cases):
            # if (i % 1000 == 0):
            #     print(i)

            company_name = fake.random_element(companies)
            model_name = fake.word()
            case_type = fake.random_element(["TypeA", "TypeB", "TypeC"])  # Add your types here
            quantity = fake.random_int(min=0, max=100)
            dollars = fake.random_int(min=1, max=1000)  # Ensure dollars is not negative or 0
            cents = fake.random_int(min=0, max=99)

            # insert into part_inventory
            part_id = conn.execute(sqlalchemy.text("""
                INSERT into part_inventory (name, type, quantity, dollars, cents) 
                VALUES (:name, :type, :quantity, :dollars, :cents) RETURNING id;
            """), {"name": f"{company_name} {model_name}", "type": "case", "quantity": quantity, "dollars": dollars, "cents": cents}).fetchone()[0]

            # insert into case_specs
            color = fake.color_name()
            psu = fake.random_element(elements=(None, 150, 300, 450, 500, 750, 850, 1000))  # Adjust weights as needed
            side_panel = fake.random_element(elements=("None", "Tempered Glass", "Mesh", "Acrylic"))  # Add other options as needed
            external_volume = fake.random_element(elements=(None, fake.random_int(min=0, max=100)))
            internal_35_bays = fake.random_int(min=0, max=15)

            conn.execute(sqlalchemy.text("""
                INSERT into case_specs (part_id, name, type, color, psu, side_panel, external_volume, internal_35_bays) 
                VALUES (:part_id, :name, :type, :color, :psu, :side_panel, :external_volume, :internal_35_bays);
            """), {"part_id": part_id, "name": f"{company_name} {model_name}", "type": case_type, "color": color,
                  "psu": psu, "side_panel": side_panel, "external_volume": external_volume, "internal_35_bays": internal_35_bays})

def add_cpu_specs(num_cpus):
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()
    companies = [fake.company() for _ in range(5)]
    # create fake posters with fake names and birthdays
    with engine.begin() as conn:
        print("adding CPUs")
        for i in range(num_cpus):
            # if (i % 1000 == 0):
            #     print(i)

            company_name = fake.random_element(companies)
            model_name = fake.word()
            cpu_name = f"{company_name} {model_name}"
            cpu_type = "cpu"
            quantity = fake.random_int(min=0, max=100)
            dollars = fake.random_int(min=1, max=1000)  # Ensure dollars is not negative or 0
            cents = fake.random_int(min=0, max=99)

            # insert into part_inventory
            part_id = conn.execute(sqlalchemy.text("""
                INSERT into part_inventory (name, type, quantity, dollars, cents) 
                VALUES (:name, :type, :quantity, :dollars, :cents) RETURNING id;
            """), {"name": cpu_name, "type": "cpu", "quantity": quantity, "dollars": dollars, "cents": cents}).fetchone()[0]

            # insert into cpu_specs
            core_count = fake.random_int(min=2, max=16)  # Adjust the range as needed
            core_clock = fake.random.uniform(2.0, 5.0)  # Adjust the range as needed
            boost_clock = fake.random.uniform(core_clock, core_clock + 2.0)  # Boost clock should be higher than core clock
            tdp = fake.random_int(min=35, max=150)  # Adjust the range as needed
            graphics = fake.random_element(elements=(None, fake.word()))  # Null or random name
            smt = fake.boolean()

            conn.execute(sqlalchemy.text("""
                INSERT into cpu_specs (part_id, name, core_count, core_clock, boost_clock, tdp, graphics, smt) 
                VALUES (:part_id, :name, :core_count, :core_clock, :boost_clock, :tdp, :graphics, :smt);
            """), {"part_id": part_id, "name": cpu_name, "core_count": core_count, 
                  "core_clock": round(core_clock,2), "boost_clock": round(boost_clock,2), "tdp": tdp, "graphics": graphics, "smt": smt})

            
def add_internal_hard_drive_specs(num_drives):
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()
    companies = [fake.company() for _ in range(5)]
    # create fake posters with fake names and birthdays
    with engine.begin() as conn:
        print("adding internal hard drives")
        for i in range(num_drives):
            # if (i % 1000 == 0):
            #     print(i)

            company_name = fake.random_element(companies)
            model_name = fake.word()
            drive_name = f"{company_name} {model_name}"
            drive_type = "internal_hard_drive"
            quantity = fake.random_int(min=0, max=100)
            dollars = fake.random_int(min=1, max=1000)  # Ensure dollars is not negative or 0
            cents = fake.random_int(min=0, max=99)

            # insert into part_inventory
            part_id = conn.execute(sqlalchemy.text("""
                INSERT into part_inventory (name, type, quantity, dollars, cents) 
                VALUES (:name, :type, :quantity, :dollars, :cents) RETURNING id;
            """), {"name": drive_name, "type": drive_type, "quantity": quantity, "dollars": dollars, "cents": cents}).fetchone()[0]

            # insert into internal_hard_drive_specs
            capacity = fake.random_int(min=0, max=100)
            price_per_gb = fake.random_int(min=1, max=10)  # Adjust the range as needed
            drive_types = ["SSD", "Disk", "Hybrid"]
            cache = fake.random_int(min=8, max=256)  # Adjust the range as needed
            form_factor = fake.random_element(elements=["2.5-inch", "3.5-inch", "M.2"])
            interface = fake.word()

            conn.execute(sqlalchemy.text("""
                INSERT into internal_hard_drive_specs (part_id, name, type, capacity, price_per_gb, cache, form_factor, interface) 
                VALUES (:part_id, :name, :type, :capacity, :price_per_gb, :cache, :form_factor, :interface);
            """), {"part_id": part_id, "name": drive_name, "type": drive_type, "capacity": capacity,
                  "price_per_gb": price_per_gb, "cache": cache, "form_factor": form_factor, "interface": interface})

def add_monitor_specs(num_monitors):
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()
    companies = [fake.company() for _ in range(5)]
    # create fake posters with fake names and birthdays
    with engine.begin() as conn:
        print("adding monitors")
        for i in range(num_monitors):
            # if (i % 1000 == 0):
            #     print(i)

            company_name = fake.random_element(companies)
            model_name = fake.word()
            monitor_name = f"{company_name} {model_name}"
            monitor_type = "monitor"
            quantity = fake.random_int(min=0, max=100)
            dollars = fake.random_int(min=1, max=1000)  # Ensure dollars is not negative or 0
            cents = fake.random_int(min=0, max=99)

            # insert into part_inventory
            part_id = conn.execute(sqlalchemy.text("""
                INSERT into part_inventory (name, type, quantity, dollars, cents) 
                VALUES (:name, :type, :quantity, :dollars, :cents) RETURNING id;
            """), {"name": monitor_name, "type": monitor_type, "quantity": quantity, "dollars": dollars, "cents": cents}).fetchone()[0]

            # insert into monitor_specs
            screen_size = fake.random_int(min=17, max=69)
            resolution = f"{fake.random_int(min=800, max=3840)}x{fake.random_int(min=600, max=2160)}"
            refresh_rate = fake.random_int(min=60, max=300)
            response_time = fake.random_digit()
            panel_type = fake.random_element(elements=["IPS", "TN", "VA"])
            aspect_ratio = f"{fake.random_int(min=4, max=21)}:{fake.random_int(min=3, max=9)}"

            conn.execute(sqlalchemy.text("""
                INSERT into monitor_specs (part_id, name, screen_size, resolution, refresh_rate, response_time, panel_type, aspect_ratio) 
                VALUES (:part_id, :name, :screen_size, :resolution, :refresh_rate, :response_time, :panel_type, :aspect_ratio);
            """), {"part_id": part_id, "name": monitor_name, "screen_size": screen_size,
                  "resolution": resolution, "refresh_rate": refresh_rate, "response_time": response_time,
                  "panel_type": panel_type, "aspect_ratio": aspect_ratio})

def add_motherboard_specs(num_motherboards):
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()
    companies = [fake.company() for _ in range(5)]
    # create fake posters with fake names and birthdays
    with engine.begin() as conn:
        print("adding motherboards")
        for i in range(num_motherboards):
            # if (i % 1000 == 0):
            #     print(i)

            company_name = fake.random_element(companies)
            model_name = fake.word()
            motherboard_name = f"{company_name} {model_name}"
            motherboard_type = "motherboard"
            quantity = fake.random_int(min=0, max=100)
            dollars = fake.random_int(min=1, max=1000)  # Ensure dollars is not negative or 0
            cents = fake.random_int(min=0, max=99)

            # insert into part_inventory
            part_id = conn.execute(sqlalchemy.text("""
                INSERT into part_inventory (name, type, quantity, dollars, cents) 
                VALUES (:name, :type, :quantity, :dollars, :cents) RETURNING id;
            """), {"name": motherboard_name, "type": motherboard_type, "quantity": quantity, "dollars": dollars, "cents": cents}).fetchone()[0]

            # insert into motherboard_specs
            socket_types = ["LGA1200", "AM4", "LGA1151", "TR4", "sTRX4", "FM2", "FM2+", "AM3", "AM3+", "LGA2066"]
            socket = fake.random_element(elements=socket_types)
            form_factor_types = ["ATX", "Micro ATX", "Mini ITX", "Extended ATX"]
            form_factor = fake.random_element(elements=form_factor_types)
            max_memory = fake.random_int(min=8, max=128)  # Adjust the range as needed
            memory_slots = fake.random_int(min=1, max=10)
            color = fake.color_name()

            conn.execute(sqlalchemy.text("""
                INSERT into motherboard_specs (part_id, name, socket, form_factor, max_memory, memory_slots, color) 
                VALUES (:part_id, :name, :socket, :form_factor, :max_memory, :memory_slots, :color);
            """), {"part_id": part_id, "name": motherboard_name, "socket": socket,
                  "form_factor": form_factor, "max_memory": max_memory, "memory_slots": memory_slots, "color": color})

def add_power_supply_specs(num_power_supplies):
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()
    companies = [fake.company() for _ in range(5)]
    # create fake posters with fake names and birthdays
    with engine.begin() as conn:
        print("adding power supplies")
        for i in range(num_power_supplies):
            # if (i % 1000 == 0):
            #     print(i)

            company_name = fake.random_element(companies)
            model_name = fake.word()
            power_supply_name = f"{company_name} {model_name}"
            power_supply_type = "power_supply"
            quantity = fake.random_int(min=0, max=100)
            dollars = fake.random_int(min=1, max=1000)  # Ensure dollars is not negative or 0
            cents = fake.random_int(min=0, max=99)

            # insert into part_inventory
            part_id = conn.execute(sqlalchemy.text("""
                INSERT into part_inventory (name, type, quantity, dollars, cents) 
                VALUES (:name, :type, :quantity, :dollars, :cents) RETURNING id;
            """), {"name": power_supply_name, "type": power_supply_type, "quantity": quantity, "dollars": dollars, "cents": cents}).fetchone()[0]

            # insert into power_supply_specs
            power_supply_types = ["ATX", "Micro ATX", "SFX", "TFX"]
            power_supply_type = fake.random_element(elements=power_supply_types)
            wattage = fake.random_int(min=300, max=1200)  # Adjust the range as needed
            modular_options = ["Full", "Semi", "None"]
            modular = fake.random_element(elements=modular_options)
            color = fake.color_name()
            efficiency_options = ["Gold", "Silver", "Bronze", "Platinum"]
            efficiency = fake.random_element(elements=efficiency_options)

            conn.execute(sqlalchemy.text("""
                INSERT into power_supply_specs (part_id, name, type, wattage, modular, color, efficiency) 
                VALUES (:part_id, :name, :type, :wattage, :modular, :color, :efficiency);
            """), {"part_id": part_id, "name": power_supply_name, "type": power_supply_type, "wattage": wattage,
                  "modular": modular, "color": color, "efficiency": efficiency})

def add_video_card_specs(num_video_cards):
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()
    companies = [fake.company() for _ in range(5)]
    # create fake posters with fake names and birthdays
    with engine.begin() as conn:
        print("adding video cards")
        for i in range(num_video_cards):
            # if (i % 1000 == 0):
            #     print(i)

            company_name = fake.random_element(companies)
            model_name = fake.word()
            video_card_name = f"{company_name} {model_name}"
            video_card_type = "video_card"
            quantity = fake.random_int(min=0, max=100)
            dollars = fake.random_int(min=1, max=1000)  # Ensure dollars is not negative or 0
            cents = fake.random_int(min=0, max=99)

            # insert into part_inventory
            part_id = conn.execute(sqlalchemy.text("""
                INSERT into part_inventory (name, type, quantity, dollars, cents) 
                VALUES (:name, :type, :quantity, :dollars, :cents) RETURNING id;
            """), {"name": video_card_name, "type": video_card_type, "quantity": quantity, "dollars": dollars, "cents": cents}).fetchone()[0]

            # insert into video_card_specs
            chipset = fake.word()
            memory = fake.random_int(min=1, max=50)
            core_clock = fake.random_int(min=800, max=2000)  # Adjust the range as needed
            boost_clock = fake.random_int(min=core_clock, max=core_clock + 500)  # Boost clock should be higher than core clock
            color = fake.color_name()
            length = fake.random_int(min=8, max=20)  # Adjust the range as needed

            conn.execute(sqlalchemy.text("""
                INSERT into video_card_specs (part_id, name, chipset, memory, core_clock, boost_clock, color, length) 
                VALUES (:part_id, :name, :chipset, :memory, :core_clock, :boost_clock, :color, :length);
            """), {"part_id": part_id, "name": video_card_name, "chipset": chipset,
                  "memory": memory, "core_clock": core_clock, "boost_clock": boost_clock, "color": color, "length": length})

def add_user_parts(num_entries):
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()
    
    # Fetch all user IDs and part IDs
    with engine.connect() as conn:
        user_ids = conn.execute(sqlalchemy.text("SELECT id FROM users")).fetchall()
        part_ids = conn.execute(sqlalchemy.text("SELECT id FROM part_inventory")).fetchall()

    print("adding user_parts")
    
    with engine.begin() as conn:
        for i in range(num_entries):
            # if (i % 100 == 0):
            #     print(i)

            # Get random user_id and part_id from the pre-fetched lists
            user_id = random.choice(user_ids)[0]
            part_id = random.choice(part_ids)[0]

            quantity = fake.random_int(min=1, max=50)
            dollars = fake.random_int(min=1, max=1000)
            cents = fake.random_int(min=0, max=99)

            conn.execute(sqlalchemy.text("""
                INSERT into user_parts (user_id, part_id, quantity, dollars, cents) 
                VALUES (:user_id, :part_id, :quantity, :dollars, :cents);
            """), {"user_id": user_id, "part_id": part_id, "quantity": quantity, "dollars": dollars, "cents": cents})


def add_carts_and_cart_items(num_carts):
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()
    with engine.begin() as conn:
        print("adding carts and cart_items")
        for i in range(num_carts):
            # if (i % 1000 == 0):
            #     print(i)

            # Get random user_id
            user_id = conn.execute(sqlalchemy.text("SELECT id FROM users ORDER BY RANDOM() LIMIT 1")).fetchone()[0]

            # Insert into carts table and get cart_id
            cart_id = conn.execute(sqlalchemy.text("""
                INSERT into carts (user_id) 
                VALUES (:user_id) RETURNING cart_id;
            """), {"user_id": user_id}).fetchone()[0]

            # Randomized amount of cart items per cart (1-10 items)
            num_cart_items = fake.random_int(min=1, max=10)

            # Maintain a set of unique part_ids for each cart
            unique_part_ids = set()

            for _ in range(num_cart_items):
                # Decide whether it's a user_item or not
                user_item = fake.boolean()

                # If it's a user_item, get part_id and quantity from user_parts, else get part_id and quantity from part_inventory
                if user_item:
                    # Get random user_part
                    if unique_part_ids:
                        user_part = conn.execute(sqlalchemy.text("SELECT * FROM user_parts WHERE user_id = :user_id AND part_id NOT IN :unique_part_ids ORDER BY RANDOM() LIMIT 1"), {"user_id": user_id, "unique_part_ids": tuple(unique_part_ids)}).fetchone()
                    else:
                        user_part = None

                    if user_part:
                        part_id = user_part.part_id
                        quantity = fake.random_int(min=1, max=user_part.quantity)
                        unique_part_ids.add(part_id)
                    else:
                        # If there are no user_parts for the user, default to part_inventory
                        part_info = conn.execute(sqlalchemy.text("SELECT part_id, quantity FROM part_inventory ORDER BY RANDOM() LIMIT 1")).fetchone()
                        if part_info:
                            part_id = part_info.part_id
                            quantity = fake.random_int(min=1, max=part_info.quantity)
                            unique_part_ids.add(part_id)
                else:
                    # Get random part_id and quantity from part_inventory
                    if unique_part_ids:
                        part_info = conn.execute(sqlalchemy.text("SELECT part_id, quantity FROM part_inventory WHERE part_id NOT IN :unique_part_ids ORDER BY RANDOM() LIMIT 1"), {"unique_part_ids": tuple(unique_part_ids)}).fetchone()
                    else:
                        part_info = conn.execute(sqlalchemy.text("SELECT part_id, quantity FROM part_inventory WHERE 1 = 0")).fetchone()

                    if part_info:
                        part_id = part_info.part_id
                        quantity = fake.random_int(min=1, max=part_info.quantity)
                        unique_part_ids.add(part_id)

                # Random boolean for checked_out
                checked_out = fake.boolean()

                # Insert into cart_items
                conn.execute(sqlalchemy.text("""
                    INSERT into cart_items (cart_id, user_item, part_id, quantity, checked_out) 
                    VALUES (:cart_id, :user_item, :part_id, :quantity, :checked_out);
                """), {"cart_id": cart_id, "user_item": user_item, "part_id": part_id, "quantity": quantity, "checked_out": checked_out})

def add_pc_templates_and_parts(num_templates):
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()
    with engine.begin() as conn:
        print("adding pc_templates and pc_template_parts")
        for i in range(num_templates):
            # if (i % 1000 == 0):
            #     print(i)

            # Get random user_id
            user_id = conn.execute(sqlalchemy.text("SELECT id FROM users ORDER BY RANDOM() LIMIT 1")).fetchone()[0]

            # Insert into pc_templates table and get template_id
            template_id = conn.execute(sqlalchemy.text("""
                INSERT into pc_templates (user_id) 
                VALUES (:user_id) RETURNING id;
            """), {"user_id": user_id}).fetchone()[0]

            # Randomized number of parts per template (1-5 parts)
            num_template_parts = fake.random_int(min=1, max=5)

            # Maintain a set of unique part_ids for each template
            unique_part_ids = set()

            for _ in range(num_template_parts):
                # Decide whether it's a user_part or not
                user_part = fake.boolean()

                # If it's a user_part, get part_id and quantity from user_parts, else get part_id and quantity from part_inventory
                if user_part:
                    # Get random user_part
                    if unique_part_ids:
                        user_part_info = conn.execute(sqlalchemy.text("SELECT * FROM user_parts WHERE user_id = :user_id AND part_id NOT IN :unique_part_ids ORDER BY RANDOM() LIMIT 1"), {"user_id": user_id, "unique_part_ids": tuple(unique_part_ids)}).fetchone()
                    else:
                        user_part_info = None

                    if user_part_info:
                        part_id = user_part_info.part_id
                        min_quantity = 1
                        max_quantity = max(2, user_part_info.quantity)  # Ensure there is a valid range
                        quantity = fake.random_int(min=min_quantity, max=max_quantity)
                        unique_part_ids.add(part_id)
                    else:
                        # If there are no user_parts for the user, default to part_inventory
                        part_info = conn.execute(sqlalchemy.text("SELECT part_id, quantity FROM part_inventory ORDER BY RANDOM() LIMIT 1")).fetchone()
                        if part_info:
                            part_id = part_info.part_id
                            quantity = fake.random_int(min=1, max=part_info.quantity)
                            unique_part_ids.add(part_id)
                else:
                    # Get random part_id and quantity from part_inventory
                    if unique_part_ids:
                        part_info = conn.execute(sqlalchemy.text("SELECT part_id, quantity FROM part_inventory WHERE part_id NOT IN :unique_part_ids ORDER BY RANDOM() LIMIT 1"), {"unique_part_ids": tuple(unique_part_ids)}).fetchone()
                    else:
                        part_info = conn.execute(sqlalchemy.text("SELECT part_id, quantity FROM part_inventory ORDER BY RANDOM() LIMIT 1")).fetchone()

                    if part_info:
                        part_id = part_info.part_id
                        min_quantity = 1
                        max_quantity = max(2, part_info.quantity)  # Ensure there is a valid range
                        quantity = fake.random_int(min=min_quantity, max=max_quantity)
                        unique_part_ids.add(part_id)

                # Insert into pc_template_parts with user_id
                conn.execute(sqlalchemy.text("""
                    INSERT into pc_template_parts (template_id, user_part, user_id, part_id, quantity) 
                    VALUES (:template_id, :user_part, :user_id, :part_id, :quantity);
                """), {"template_id": template_id, "user_part": user_part, "user_id": user_id, "part_id": part_id, "quantity": quantity})







def main():
    quants = {
        "add_users": 50000,
        "add_case_specs": 100000,
        "add_cpu_specs": 100000,
        "add_internal_hard_drive_specs": 100000,
        "add_monitor_specs": 100000,
        "add_motherboard_specs": 100000,
        "add_power_supply_specs": 100000,
        "add_video_card_specs": 100000,
        "add_user_parts": 100000,
        "add_carts_and_cart_items": 100000,
        "add_pc_templates_and_parts": 100000
    }

    processes = []

    # Define task groups based on dependencies
    task_groups = [
        [add_users,
         add_cpu_specs],
        [add_internal_hard_drive_specs],
        [add_monitor_specs],
        [add_motherboard_specs],
        [add_power_supply_specs],
        [add_video_card_specs],
        [add_case_specs],
        [add_user_parts],
        [
            add_carts_and_cart_items,
            add_pc_templates_and_parts
        ]
    ]

    # Start tasks in each group sequentially
    for group in task_groups:
        group_processes = []
        for task in group:
            process = multiprocessing.Process(target=task, args=(quants[task.__name__],))
            group_processes.append(process)
            process.start()
        # Wait for processes in the current group to finish before moving to the next group
        for process in group_processes:
            process.join()

if __name__ == "__main__":
    main()
