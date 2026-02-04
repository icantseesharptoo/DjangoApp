# Migration Helper Script for PostgreSQL
# This script helps you migrate from SQLite to PostgreSQL

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'room_booking_project.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_database_type():
    """Check which database is currently being used"""
    db_engine = connection.settings_dict['ENGINE']
    db_name = connection.settings_dict['NAME']
    
    if 'postgresql' in db_engine:
        return 'PostgreSQL', db_name
    elif 'sqlite' in db_engine:
        return 'SQLite', db_name
    else:
        return 'Unknown', db_name

def backup_data():
    """Backup data from current database"""
    print_header("Step 1: Backing up data")
    
    backup_file = BASE_DIR / 'data_backup.json'
    
    try:
        print(f"Creating backup at: {backup_file}")
        call_command(
            'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '-e', 'contenttypes',
            '-e', 'auth.Permission',
            '--indent', '2',
            output=str(backup_file)
        )
        print(f"✓ Backup created successfully: {backup_file}")
        return True
    except Exception as e:
        print(f"✗ Error creating backup: {e}")
        return False

def show_database_info():
    """Display current database information"""
    print_header("Current Database Information")
    
    db_type, db_name = check_database_type()
    db_settings = connection.settings_dict
    
    print(f"Database Type: {db_type}")
    print(f"Database Name: {db_name}")
    
    if db_type == 'PostgreSQL':
        print(f"Host: {db_settings.get('HOST', 'N/A')}")
        print(f"Port: {db_settings.get('PORT', 'N/A')}")
        print(f"User: {db_settings.get('USER', 'N/A')}")
    
    print()

def verify_data():
    """Verify data in the database"""
    print_header("Verifying Database Data")
    
    try:
        from bookings.models import Room, Booking
        from django.contrib.auth.models import User
        
        user_count = User.objects.count()
        room_count = Room.objects.count()
        booking_count = Booking.objects.count()
        
        print(f"Users: {user_count}")
        print(f"Rooms: {room_count}")
        print(f"Bookings: {booking_count}")
        print(f"\n✓ Total records: {user_count + room_count + booking_count}")
        
        return True
    except Exception as e:
        print(f"✗ Error verifying data: {e}")
        return False

def main():
    """Main migration helper function"""
    print_header("PostgreSQL Migration Helper")
    
    print("This script will help you migrate from SQLite to PostgreSQL.\n")
    print("Available commands:")
    print("  1. Show current database info")
    print("  2. Backup data from current database")
    print("  3. Verify data in database")
    print("  4. Run all checks")
    print("  0. Exit")
    
    while True:
        choice = input("\nEnter your choice (0-4): ").strip()
        
        if choice == '1':
            show_database_info()
        elif choice == '2':
            backup_data()
        elif choice == '3':
            verify_data()
        elif choice == '4':
            show_database_info()
            backup_data()
            verify_data()
        elif choice == '0':
            print("\nExiting migration helper. Good luck with your migration!")
            break
        else:
            print("Invalid choice. Please enter 0-4.")

if __name__ == '__main__':
    main()
