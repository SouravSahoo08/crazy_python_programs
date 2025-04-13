from sys import argv
import pandas as pd

def main():
    # accept excel file name, and month(divided the transactions in excel workbook into sheets labeled with months, eg. march25)
    # from arguments
    script, filename, month = argv
    
    # Load data with explicit dtype specification for better performance
    acc_stmt = pd.read_excel(
        filename, 
        sheet_name=month,
        dtype={'Debit': str, 'Details': str}  # Adjust dtypes as needed
    )
    
    # Convert Debit to numeric, treating '-' as NaN since i had some values as '-'
    acc_stmt['Debit'] = pd.to_numeric(acc_stmt['Debit'], errors='coerce').fillna(0)
    
    # Create boolean masks for each category (vectorized operations)
    mask_milk = acc_stmt['Details'].str.lower().str.contains('somnath|puskar', na=False, regex=True)
    mask_gas = acc_stmt['Details'].str.contains('BBPSBP', na=False)
    
    # Calculate totals using vectorized operations
    milk = acc_stmt.loc[mask_milk, 'Debit'].sum()
    gas = acc_stmt.loc[mask_gas, 'Debit'].sum()
    total_spending = acc_stmt['Debit'].sum()
    
    # Print results
    print(f"\nExpense Summary for {month}:")
    print(f"{'Milk':<20}: Rs. {milk:.2f}")
    print(f"{'Gas':<20}: Rs. {gas:.2f}")
    print(f"{'Milk + Gas':<20}: Rs. {gas + milk:.2f}")
    print(f"{'Total Spending':<20}: Rs. {total_spending:.2f}")

if __name__ == "__main__":
    main()