import os
import sys
import pandas as pd
from datetime import datetime

def check_arguments():
    if len(sys.argv) != 2:
        print("Error: Please provide the path to the sales data CSV file.")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    
    if not os.path.isfile(csv_file_path):
        print(f"Error: The file {csv_file_path} does not exist.")
        sys.exit(1)
    
    return csv_file_path

def create_orders_directory():
    today_date = datetime.now().strftime('%Y-%m-%d')
    orders_directory = f"Orders_{today_date}"
    
    if not os.path.exists(orders_directory):
        os.makedirs(orders_directory)
    
    return orders_directory

def process_orders(csv_file_path, orders_directory):
    df = pd.read_csv(csv_file_path)
    
    for order_id, order_df in df.groupby('ORDER ID'):
        # Sort by ITEM NUMBER
        order_df = order_df.sort_values('ITEM NUMBER')
        
        # Calculate total price
        order_df['TOTAL PRICE'] = order_df['ITEM QUANTITY'] * order_df['ITEM PRICE']
        
        # Calculate grand total
        grand_total = order_df['TOTAL PRICE'].sum()
        
        # Create Excel file
        excel_path = os.path.join(orders_directory, f"Order_{order_id}.xlsx")
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            order_df.to_excel(writer, sheet_name='Order Details', index=False)
            
            # Get workbook and worksheet objects
            workbook  = writer.book
            worksheet = writer.sheets['Order Details']
            
            # Format the total price column
            money_format = workbook.add_format({'num_format': '$#,##0.00'})
            worksheet.set_column('D:D', 18, money_format)
            
            # Add grand total row
            worksheet.write_string(len(order_df) + 1, 0, 'Grand Total')
            worksheet.write_formula(len(order_df) + 1, 3, f'SUM(D2:D{len(order_df) + 1})', money_format)
            
            # Adjust column widths
            worksheet.set_column('A:A', 12)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 15)

def main():
    csv_file_path = check_arguments()
    orders_directory = create_orders_directory()
    process_orders(csv_file_path, orders_directory)

if __name__ == "__main__":
    main()
