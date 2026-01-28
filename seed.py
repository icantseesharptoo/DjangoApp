import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'room_booking_project.settings')
django.setup()

from django.contrib.auth.models import User, Group
from bookings.models import Room

def seed_data():
    # Create Groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    staff_group, _ = Group.objects.get_or_create(name='Staff')

    # Create Users
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin_user.groups.add(admin_group)
        print("Admin user created.")

    if not User.objects.filter(username='staff').exists():
        staff_user = User.objects.create_user('staff', 'staff@example.com', 'staff123')
        staff_user.groups.add(staff_group)
        print("Staff user created.")

    # Create Rooms
    rooms = [
        {
            "name": "Zen Boardroom",
            "capacity": 12,
            "description": "A minimalist, quiet boardroom perfect for high-stakes decision making. Equipped with 4K displays and ergonomic seating.",
            "image_url": "https://images.unsplash.com/photo-1431540015161-0bf868a2d407?auto=format&fit=crop&q=80&w=800"
        },
        {
            "name": "Innovation Hub",
            "capacity": 20,
            "description": "Dynamic space with writable walls, modular furniture, and high-speed fiber connectivity. Ideal for brainstorming sessions.",
            "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=800"
        },
        {
            "name": "The Observatory",
            "capacity": 6,
            "description": "A glass-walled meeting space with panoramic views. Perfect for creative thinking and small group collaborative work.",
            "image_url": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&q=80&w=800"
        }
    ]

    for room_data in rooms:
        Room.objects.get_or_create(**room_data)
        print(f"Room '{room_data['name']}' created.")

if __name__ == '__main__':
    seed_data()
