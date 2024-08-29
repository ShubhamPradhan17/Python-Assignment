# Create function to check if date is in given range

from datetime import datetime

def is_date_in_range(date, start_date, end_date):

    date = datetime.strptime(date_to_check, "%Y-%m-%d")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    
    return start_date <= date <= end_date

print(is_date_in_range("2024-08-01", "2024-07-01", "2024-09-01")) 
print(is_date_in_range("2024-10-01", "2024-07-01", "2024-09-01")) 


