#!/usr/bin/env python3
"""
Script to populate the sell database with test data across different dates
for testing the date filtering functionality.
"""

import sys
import os
from datetime import datetime, timedelta
import random
import pandas as pd
from unittest.mock import patch

# Add the src directory to the path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.business.sell_controller import create_sell, read_sell_data
from src.business.create_stock_controller import read_stock

def get_random_items():
    """Get random items from the stock to create realistic sales."""
    try:
        stock_data = read_stock("")
        if stock_data.empty:
            print("Warning: No stock data found. Using default item codes.")
            return ["1AYB", "1P", "1AP"], ["1", "2", "1"]
        
        # Get random items from stock
        sample_size = min(random.randint(1, 5), len(stock_data))
        sampled_items = stock_data.sample(n=sample_size)
        
        item_codes = []
        quantities = []
        
        for _, item in sampled_items.iterrows():
            item_codes.append(str(item['item_code']))
            quantities.append(str(random.randint(1, 3)))
        
        return item_codes, quantities
    except Exception as e:
        print(f"Error reading stock data: {e}")
        # Fallback to default items
        return ["1AYB", "1P", "1AP"], ["1", "2", "1"]

def create_test_sell(target_date, items, quantities, total):
    """Create a test sell with a specific date."""
    # Create the sell data structure exactly like the app does
    new_sell_data = [{
        "items": "-".join(items),
        "quantities": "-".join(quantities), 
        "total": total,
    }]
    
    # Use mock.patch to override datetime.now in the sell_controller module
    from src.business.sell_controller import create_sell
    
    with patch('src.business.sell_controller.datetime') as mock_datetime:
        # Set up the mock to return our target date
        mock_datetime.now.return_value = target_date
        
        # Use the normal create_sell function
        result = create_sell(new_sell_data)
        return result

def populate_test_data():
    """Populate the database with test sales across different dates."""
    print("🏪 Populating sell database with test data...")
    
    today = datetime.now()
    test_sales = []
    
    # Define test sales with different dates
    test_scenarios = [
        # Today
        (today, "Venta de hoy"),
        
        # Yesterday  
        (today - timedelta(days=1), "Venta de ayer"),
        
        # 3 days ago
        (today - timedelta(days=3), "Venta hace 3 días"),
        
        # 5 days ago
        (today - timedelta(days=5), "Venta hace 5 días"),
        
        # 10 days ago
        (today - timedelta(days=10), "Venta hace 10 días"),
        
        # 20 days ago
        (today - timedelta(days=20), "Venta hace 20 días"),
        
        # 45 days ago (last month)
        (today - timedelta(days=45), "Venta del mes pasado"),
        
        # 60 days ago (2 months ago)
        (today - timedelta(days=60), "Venta hace 2 meses"),
        
        # First day of current month
        (today.replace(day=1), "Primera venta del mes"),
        
        # Mid current month
        (today.replace(day=15) if today.day > 15 else today.replace(day=15) - timedelta(days=30), "Venta a mediados de mes"),
    ]
    
    for i, (target_date, description) in enumerate(test_scenarios, 1):
        try:
            # Get random items for this sale
            items, quantities = get_random_items()
            
            # Calculate a realistic total (random between 5000 and 50000)
            total = random.randint(5000, 50000)
            
            # Create the test sell
            result = create_test_sell(target_date, items, quantities, total)
            
            print(f"✅ Created sale {i:2d}: {description} - {target_date.strftime('%Y-%m-%d')} - ${total:,}")
            print(f"    Items: {'-'.join(items)} | Quantities: {'-'.join(quantities)}")
            
        except Exception as e:
            print(f"❌ Failed to create sale {i}: {e}")
    
    print(f"\n🎉 Finished! Created {len(test_scenarios)} test sales.")
    print("\nYou can now test the date filters:")
    print("• 'Hoy' - Should show today's sales")
    print("• 'Ayer' - Should show yesterday's sales") 
    print("• 'Últimos 7 días' - Should show recent sales")
    print("• 'Últimos 30 días' - Should show this month's sales")
    print("• 'Este mes' - Should show current month sales")
    print("• 'Mes pasado' - Should show last month's sales")

def main():
    """Main function to run the script."""
    print("=" * 60)
    print("📊 SELL DATABASE TEST DATA POPULATOR")
    print("=" * 60)
    
    try:
        # Check if sell database exists, if not create it
        from src.business.sell_controller import initialize_sell_db
        initialize_sell_db()
        
        # Show current state
        try:
            current_data = read_sell_data()
            print(f"📋 Current database has {len(current_data)} sales")
        except:
            print("📋 Database is empty or doesn't exist")
        
        # Ask for confirmation
        response = input("\n🤔 Do you want to add test data? (y/N): ").strip().lower()
        
        if response in ['y', 'yes', 'sí', 'si']:
            populate_test_data()
            
            # Show final state
            try:
                final_data = read_sell_data()
                print(f"\n📊 Final database has {len(final_data)} sales")
                print("\n📅 Sales by date:")
                if not final_data.empty:
                    final_data['date'] = pd.to_datetime(final_data['date'])
                    date_counts = final_data.groupby(final_data['date'].dt.date).size()
                    for date, count in date_counts.items():
                        print(f"  {date}: {count} sale(s)")
            except Exception as e:
                print(f"Error showing final state: {e}")
        else:
            print("❌ Operation cancelled.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 