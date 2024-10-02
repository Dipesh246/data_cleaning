import nepali_datetime
import datetime
 
english_date = datetime.date.today()
nepali_date = nepali_datetime.date.from_datetime_date(english_date)

print(english_date)
print(nepali_date.strftime('%B'))


