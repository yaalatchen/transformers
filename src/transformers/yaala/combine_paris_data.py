import csv
import datetime

if __name__ == '__main__':
    weather_data_file = r"C:\Users\yczohar\Desktop\demand_data\paris_weather\2006-20010_weather_and_calander.csv"
    demand_data = r"C:\Users\yczohar\Desktop\demand_data\my_demand_data.txt"
    outfile = r"C:\Users\yczohar\Desktop\demand_data\full_demand_weather_data.txt"

    end_time = datetime.datetime(2010, 11, 26, 21, 0, 0)

    header = 'date,year,month,day,hour,minute,second,temperature,dew_point,wind_direction,wind_speed,wind_gust_speed,pressure,sky_coverage,' \
             'day_of_week,new_years_eve,new_years_day,easter_day_1,easter_day_2,may_day,victory_day,ascention_day,mothers_day,' \
             'whit_sunday,whit_monday,fathers_day,bastille_day,assumption_day,all_saints_day,armistice_day,christmas_eve,christmas_day,demand\n'
    out_lines = [header]
    with open(weather_data_file) as wf:
        with open(demand_data) as df:
            w_lines = wf.readlines()
            d_lines = df.readlines()
            demand_index = 1
            start_demand_line = d_lines[demand_index].split(',')
            start_time = datetime.datetime(int(start_demand_line[0]), int(start_demand_line[1]), int(start_demand_line[2]), int(start_demand_line[3]), int(start_demand_line[4]))
            weather_index = 1
            found_start_time = False
            while not found_start_time:
                curr_line = w_lines[weather_index].split(',')
                curr_weather_time = datetime.datetime(int(curr_line[0]), int(curr_line[1]), int(curr_line[2]), int(curr_line[3]), int(curr_line[4]))
                if curr_weather_time != start_time:
                    weather_index += 1
                else:
                    found_start_time = True

            while weather_index < len(w_lines) and demand_index < len(d_lines):
                w_line = w_lines[weather_index].split(',')
                d_line = d_lines[demand_index].split(',')
                w_time = datetime.datetime(int(w_line[0]), int(w_line[1]), int(w_line[2]), int(w_line[3]), int(w_line[4]))
                d_time = datetime.datetime(int(d_line[0]), int(d_line[1]), int(d_line[2]), int(d_line[3]), int(d_line[4]))
                if w_time != d_time:
                    print("ERROR, d_line " + demand_index + " w_line " + weather_index + " difference seconds " + (w_time-d_time).total_seconds())
                    exit(0)
                date_string = w_time.strftime("%m/%d/%Y %H:%M:%S")
                new_line = date_string + ',' + w_lines[weather_index][:-1] + "," + d_line[-1]
                out_lines.append(new_line)
                weather_index += 1
                demand_index += 1

    a = 0
    with open(outfile, 'w') as f:
        f.writelines(out_lines)






