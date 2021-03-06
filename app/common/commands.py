import click

from flask import Blueprint, current_app
from app import db, models
from faker import Faker

from app.common.util import find_user_by_email


commands = Blueprint("commands", __name__)


@commands.cli.command("add-sys-admin")
@click.argument("email")
@click.argument("password")
@click.argument("first_name")
@click.argument("last_name")
@click.argument("phone_number")
def add_sys_admin(email, password, first_name, last_name, phone_number):
    exists_root = [user_role for user_role in models.UserRole.query.all() if user_role.role == models.Role.ROOT]
    if exists_root:
        print("There is already a sys admin")
        return
    
    root = models.User(email=email, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number)
    root.add_role(models.Role.CUSTOMER)
    root.add_role(models.Role.EMPLOYEE)
    root.add_role(models.Role.ADMIN)
    root.add_role(models.Role.ROOT)

    employee_root = models.Employee(user=root)
    db.session.add(employee_root)
    db.session.commit()


@commands.cli.command("create-database")
def create_database():
    db.drop_all()
    db.create_all()


@commands.cli.command("seed-database")
def seed_database():
    if current_app.config["ENV"] != "development":
        return
    
    fake = Faker()


    def generate_users():
        users = []
        for _ in range(10):
            user = models.User(first_name=fake.first_name(),
                               last_name=fake.last_name(),
                               address=fake.address(),
                               phone_number=fake.phone_number(),
                               email=fake.email(),
                               password=fake.password())
            db.session.add(user)
            users.append(user)

        db.session.commit()
        return users


    def generate_roles(users):
        roles = [role for role in models.Role if role != models.Role.ROOT]
        for i, user in enumerate(users):
            user_role = models.UserRole(user=user, role=roles[i % len(roles)])
            db.session.add(user_role)
        
        db.session.commit()

    
    def generate_remember_hashes(users):
        for x in range(5):
            remember = models.Remember(users[x].id)
            db.session.add(remember)

        db.session.commit()
        

    def generate_offices():
        offices = []
        for _ in range(10):
            office = models.Office(address=fake.address())
            db.session.add(office)
            offices.append(office)
        
        db.session.commit()
        return offices


    def generate_employees(users, offices):
        employees = []
        for i in range(5):
            office = None
            if i % 2 == 0:
                office = offices[i]

            employee = models.Employee(user=users[i], office=office)
            db.session.add(employee)
            employees.append(employee)
        
        db.session.commit()
        return employees


    def generate_shipments(acceptor, deliverer, users, offices):
        shipments = []

        for i in range(9):
            from_office = offices[i]
            to_office = offices[i + 1]
            from_address = fake.address()
            to_address = fake.address()
            
            from_address = models.ShippingAddress(office=from_office, address=from_address)
            to_address = models.ShippingAddress(office=to_office, address=to_address)

            shipment = models.Shipment(weight=abs(fake.pyfloat()),
                                       price=abs(fake.pyfloat()),
                                       from_address=from_address,
                                       to_address=to_address,
                                       sender=users[i],
                                       receiver=users[i+1],
                                       acceptor=acceptor,
                                       deliverer=deliverer)
            db.session.add(shipment)
            shipments.append(shipment)

        db.session.commit()
        return shipments


    users = generate_users()
    generate_roles(users)
    generate_remember_hashes(users)
    offices = generate_offices()
    employees = generate_employees(users, offices)
    generate_shipments(employees[0], employees[1], users, offices)
    