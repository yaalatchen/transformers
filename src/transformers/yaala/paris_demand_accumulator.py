import csv
import datetime
import numpy as np

max_valid_distance_between_lines = 10

def update_final_demand_sum(demand_list, time_skip, time):
    if len(demand_list) < time_skip.total_seconds()/60.0/2 + 2 :
        return 'NAN'

    desired_t = [-i for i in range(int(time_skip.total_seconds()/60)-1, -1, -1)]
    ts = [int((d[0] - time).total_seconds()/60.0) for d in demand_list]
    ys = [d[1] for d in demand_list]
    diff_t = [ts[i] - ts[i-1] for i in range(1, len(demand_list))]
    if max(diff_t) > max_valid_distance_between_lines:
        return 'NAN' # too many missing lines

    desired_y = np.interp(desired_t, ts, ys)

    return sum(desired_y)*1/60 # turn kw to kw*hr



if __name__ == '__main__':
    filename = r'C:\Users\yczohar\Desktop\demand_data\household_power_consumption.txt'
    outfilename = r'C:\Users\yczohar\Desktop\demand_data\my_demand_data.txt'
    starting_point = datetime.datetime(2006, 12, 16, 17, 30, 0)
    ending_point = datetime.datetime(2010, 11, 26, 21, 0, 0)
    time_skip = datetime.timedelta(minutes=30)
    next_time = starting_point + time_skip

    collect_for_time_sum = []
    out_list = ['year,month,day,hour,minute,second,global_active_power\n']
    with open(filename, newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=';')
        is_first_line = True
        first_line = ""
        out_lines = []

        c = 0
        all_data = []
        for l in lines:
            if is_first_line:
                is_first_line = False
                continue
            date = l[0].split('/')
            time = l[1].split(':')
            year = int(date[2])
            month = int(date[1])
            day = int(date[0])
            hour = int(time[0])
            minute = int(time[1])
            second = int(time[2])

            dt = datetime.datetime(year, month, day, hour, minute, second)

            if dt <= starting_point:
                if not l[2] == '?':
                    collect_for_time_sum =[(dt, float(l[2]))]
                continue

            if dt > next_time and not l[2] == '?':
                #update previous point collecting
                collect_for_time_sum.append((dt, float(l[2]))) # in case the last dt in collected list is '?', we might want to use the next dt to help interpolating
                demand = update_final_demand_sum(collect_for_time_sum, time_skip, next_time)
                single_line = str(next_time.year)+','+str(next_time.month)+','+str(next_time.day)+','+\
                              str(next_time.hour)+','+str(next_time.minute)+','+str(next_time.second)+\
                              ','+str(demand)+'\n'
                out_list.append(single_line)
                all_data.append((next_time, demand))
                temp = collect_for_time_sum[-2]
                collect_for_time_sum = [temp] # in case the first is empty, maybe we could interpolate from the last available valid

                # add empty lines if skipped too much
                next_time += time_skip
                while dt > next_time:
                    single_line = str(next_time.year) + ',' + str(next_time.month) + ',' + str(next_time.day) + ',' + \
                                  str(next_time.hour) + ',' + str(next_time.minute) + ',' + str(next_time.second) + \
                                  ',NAN\n'
                    all_data.append((next_time, 'NAN'))
                    out_list.append(single_line)
                    next_time += time_skip


                if dt > ending_point:
                    break

            if not l[2] == '?':
                collect_for_time_sum.append((dt, float(l[2])))

    with open(outfilename, 'w') as f:
        f.writelines(out_list)

    all_times = [a[0] for a in all_data]
    diff_times = [(all_times[i+1] - all_times[i]).total_seconds()/60.0 for i in range(len(all_times)-1)]
    valid_values = []
    for a in all_data:
        if a[1] != 'NAN':
            valid_values.append(a[1])
    b = 0