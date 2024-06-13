import csv
import numpy as np
import datetime

if __name__ == '__main__':

    weather_file = r'C:\Users\yczohar\Desktop\demand_data\paris_weather\2006-20010_weather.csv'
    calander_weather_file = r'C:\Users\yczohar\Desktop\demand_data\paris_weather\2006-20010_weather_and_calander.csv'

    special_days_names = [
        ('new_years_eve',  ['31.12.06', '31.12.07', '31.12.08', '31.12.09', '31.12.10']),
        ('new_years_day',  ['1.1.06',   '1.1.07',   '1.1.08',   '1.1.09',   '1.1.10']),
        ('easter_day_1',   ['16.4.06',  '8.4.07',   '23.3.08',  '12.4.09',  '4.4.10']),
        ('easter_day_2',   ['17.4.06',  '9.4.07',   '24.3.08',  '13.4.09',  '5.4.10']),
        ('may_day',        ['1.5.06',   '1.5.07',   '1.5.08',   '1.5.09',   '1.5.10']),
        ('victory_day',    ['8.5.06',   '8.5.07',   '8.5.08',   '8.5.09',   '8.5.10']),
        ('ascention_day',  ['25.5.06',  '17.5.07',  '1.5.08',   '21.5.09',  '13.5.10']),
        ('mothers_day',    ['28.5.06',  '3.6.07',   '25.5.08',  '7.6.09',   '30.5.10']),
        ('whit_sunday',    ['4.6.06',   '27.5.07',  '11.5.08',  '31.5.09',  '23.5.10']),
        ('whit_monday',                            ['12.5.08',  '1.6.09',   '24.5.10']),
        ('fathers_day',    ['18.6.06',  '17.6.07',  '15.6.08',  '21.6.09',  '20.6.10']),
        ('bastille_day',   ['14.7.06',  '14.7.07',  '14.7.08',  '14.7.09',  '14.7.10']),
        ('assumption_day', ['15.8.06' , '15.8.07',  '15.8.08',  '15.8.09',  '15.8.10']),
        ('all_saints_day', ['1.11.06',  '1.11.07',  '1.11.08',  '1.11.09',  '1.11.10']),
        ('armistice_day',  ['11.11.06', '11.11.07', '11.11.08', '11.11.09', '11.11.10']),
        ('christmas_eve',  ['24.12.06', '24.12.07', '24.12.08', '24.12.09', '24.12.10']),
        ('christmas_day',  ['25.12.06', '25.12.07', '25.12.08', '25.12.09', '25.12.10'])
    ]

    header = 'year,month,day,hour,minute,second,temperature,dew_point,wind_direction,wind_speed,wind_gust_speed,pressure,sky_coverage'
    header_addition = ',day_of_week'
    for s in special_days_names:
        header_addition += ','+s[0]

    out_lines = []
    out_lines.append(header + header_addition + '\n')

    nucleus = datetime.datetime(2006, 1, 1)

    with open(weather_file, newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',', quotechar='"')
        is_first_line = True
        first_line = ""

        for l in lines:
            if is_first_line:
                is_first_line = False
                continue
            year = l[0]
            month = l[1]
            day = l[2]
            date_string =  day + '.' + month + '.' + year[-2:]
            date = datetime.datetime(int(year), int(month), int(day))
            days_from_nucleous = (int)((date - nucleus).total_seconds()/60/60/24)
            day_of_the_week = days_from_nucleous % 7 + 1

            addition_calander = np.zeros(len(special_days_names)+1)
            addition_calander[0] = day_of_the_week
            for i in range(len(special_days_names)):
                if date_string in special_days_names[i][1]:
                    addition_calander[i+1] = 1

            single_line_list = np.hstack((l, addition_calander))
            single_line = ""
            for e in single_line_list:
                single_line += e + ','
            single_line = single_line[:-1] + '\n'
            out_lines.append(single_line)


    with open(calander_weather_file, 'w') as f:
        f.writelines(out_lines)

