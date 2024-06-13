import csv
import datetime
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

def GetDateTime(date_time_string):
    date = date_time_string.split('T')[0]
    time = date_time_string.split('T')[1]
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    hour = int(time.split(':')[0])
    minute = int(time.split(':')[1])
    second = int(time.split(':')[2])

    dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    return dt


def GetInterpolatedValues(value_index, max_interpolation_time, time_array, line_time_delta):

    counter = 0
    prev_time = time_array[counter] - line_time_delta
    first_time = time_array[counter]
    final_value_array = []
    final_time_array = []

    prev_valid_value = float(all_lines[counter][value_index])
    prev_valid_time = time_array[counter]

    all_valid_values = []
    all_valid_time = []
    while (prev_time + line_time_delta) < first_time + relativedelta(years=1):

        next_time = prev_time + line_time_delta
        curr_line_time = time_array[counter]
        curr_next_diff = (next_time - curr_line_time).total_seconds() / 60.0
        if curr_next_diff <= 5 and (counter + 1 >= len(all_lines) or curr_next_diff < (
                next_time - time_array[counter + 1]).total_seconds() / 60.0):
            # 5 minutes difference is close enough, we can use it as is
            curr_line_time = next_time
        if next_time > curr_line_time:
            if not all_lines[counter][value_index] == " " and not all_lines[counter][value_index] == "":
                prev_valid_value = float(all_lines[counter][value_index])
                prev_valid_time = time_array[counter]
            counter += 1
            continue

        if not all_lines[counter][value_index] == " " and not all_lines[counter][value_index] == "":  # and prev_valid_time <= next_time:

            if curr_line_time not in all_valid_time:
                all_valid_time.append(curr_line_time)
                all_valid_values.append(float(all_lines[counter][value_index]))

            if (curr_line_time - prev_valid_time).total_seconds() > max_interpolation_time.total_seconds() and next_time != curr_line_time:
                final_value_array.append("NAN")
            elif next_time == curr_line_time:
                final_value_array.append(float(all_lines[counter][
                                                   value_index]))  # prev_valid_value * 0.5 + float(all_lines[counter][value_index]) * 0.5)  # interpolate()) # TODO TODO TODO TODO !!!!!
                prev_valid_value = float(all_lines[counter][value_index])
                prev_valid_time = time_array[counter]
            else:
                diff = (prev_valid_value - float(all_lines[counter][value_index]))
                ratio = (prev_valid_time - next_time).total_seconds() / (
                            prev_valid_time - curr_line_time).total_seconds()
                interpolated_value = prev_valid_value - diff * ratio
                final_value_array.append(
                    interpolated_value)  # prev_valid_value * 0.5 + float(all_lines[counter][value_index]) * 0.5)  # interpolate()) # TODO TODO TODO TODO !!!!!
                # prev_valid_value = float(all_lines[counter][value_index])
                # prev_valid_time = time_array[counter]
            final_time_array.append(next_time)
            prev_time = next_time
        else:
            counter += 1
            if counter+1 >= len(all_lines):
                final_value_array.append("NAN")
                final_time_array.append(next_time)
                break


    return (final_time_array, final_value_array, all_valid_time, all_valid_values)

if __name__ == "__main__":

    line_time_delta = datetime.timedelta(minutes=30)


    input_files = [r"C:\Users\yczohar\Desktop\weather_underground_data\2006_extracted.csv",
                   r"C:\Users\yczohar\Desktop\weather_underground_data\2007_extracted.csv",
                   r"C:\Users\yczohar\Desktop\weather_underground_data\2008_extracted.csv",
                   r"C:\Users\yczohar\Desktop\weather_underground_data\2009_extracted.csv",
                   r"C:\Users\yczohar\Desktop\weather_underground_data\2010_extracted.csv"]

    output_files = [r"C:\Users\yczohar\Desktop\weather_underground_data\2006_interpolated.csv",
                    r"C:\Users\yczohar\Desktop\weather_underground_data\2007_interpolated.csv",
                    r"C:\Users\yczohar\Desktop\weather_underground_data\2008_interpolated.csv",
                    r"C:\Users\yczohar\Desktop\weather_underground_data\2009_interpolated.csv",
                    r"C:\Users\yczohar\Desktop\weather_underground_data\2010_interpolated.csv"]


    for i in range(len(input_files)):
        all_lines = []
        time_array = []
        with open(input_files[i], newline='') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            is_first_line = True
            first_time = ''

            for l in lines:
                if is_first_line:
                    is_first_line = False
                else:
                    time_array.append(GetDateTime(l[0]))
                    all_lines.append(l)

        temperature_index = 1
        small_interpolation_time = datetime.timedelta(minutes=60)
        (final_time_array1, final_temperature_array, all_valid_time, all_valid_temperature) = \
            GetInterpolatedValues(temperature_index, small_interpolation_time, time_array, line_time_delta)

        dew_index = 2
        (final_time_array2, final_dew_array, all_valid_time, all_valid_dew) = \
            GetInterpolatedValues(dew_index, small_interpolation_time, time_array, line_time_delta)

        wind_d_index = 3
        (final_time_array3, final_wind_d_array, all_valid_time, all_valid_wind_d) = \
            GetInterpolatedValues(wind_d_index, small_interpolation_time, time_array, line_time_delta)

        wind_s_index = 4
        (final_time_array4, final_wind_s_array, all_valid_time, all_valid_wind_s) = \
            GetInterpolatedValues(wind_s_index, small_interpolation_time, time_array, line_time_delta)

        wind_g_index = 5
        (final_time_array5, final_wind_g_array, all_valid_time, all_valid_wind_g) = \
            GetInterpolatedValues(wind_g_index, small_interpolation_time, time_array, line_time_delta)

        pressure_index = 6
        large_interpolation_time = datetime.timedelta(minutes=90)
        (final_time_array6, final_pressure_array, all_valid_time, all_valid_pressure) = \
            GetInterpolatedValues(pressure_index, large_interpolation_time, time_array, line_time_delta)

        sky_index = 7
        (final_time_array7, final_sky_array, all_valid_time, all_valid_sky) = \
            GetInterpolatedValues(sky_index, small_interpolation_time, time_array, line_time_delta)


        # arranged_time = []
        # arranged_val = []
        # for i in range(len(final_dew_array)):
        #     if not final_dew_array[i] == "NAN":
        #         arranged_val.append(final_dew_array[i])
        #         arranged_time.append(final_time_array[i])
        #
        # plt.figure(1)
        # plt.plot(arranged_time, arranged_val, '.r')
        # plt.plot(all_valid_time, all_valid_dew, '.b')
        #
        # plt.figure(2)
        # plt.plot(all_valid_time, all_valid_dew, '.b')
        # plt.plot(arranged_time, arranged_val, '.r')




        if (len(final_time_array1) != len(final_temperature_array)
            or len(final_time_array1) != len(final_time_array2)
            or len(final_time_array1) != len(final_dew_array)
            or len(final_time_array1) != len(final_time_array3)
            or len(final_time_array1) != len(final_wind_d_array)
            or len(final_time_array1) != len(final_time_array4)
            or len(final_time_array1) != len(final_wind_s_array)
            or len(final_time_array1) != len(final_time_array5)
            or len(final_time_array1) != len(final_wind_g_array)
            or len(final_time_array1) != len(final_time_array6)
            or len(final_time_array1) != len(final_pressure_array)
            or len(final_time_array1) != len(final_time_array7)
            or len(final_time_array1) != len(final_sky_array)):
            print("ERROR, different lengths")
            exit(0)

        header = "year,month,day,hour,minute,second,temperature,dew_point,wind_direction,wind_speed,wind_gust_speed,pressure,sky_coverage\n"
        lines = []
        lines.append(header)
        for j in range(len(final_time_array1)):
            if(final_time_array1[j] != final_time_array2[j]
            or final_time_array1[j] != final_time_array3[j]
            or final_time_array1[j] != final_time_array4[j]
            or final_time_array1[j] != final_time_array5[j]
            or final_time_array1[j] != final_time_array6[j]
            or final_time_array1[j] != final_time_array7[j]):
                print("ERROR, different tims")
                exit(0)

            single_line = str(final_time_array1[j].year) + ',' + str(final_time_array1[j].month) + ',' + str(final_time_array1[j].day) + ','\
                          + str(final_time_array1[j].hour) + ',' + str(final_time_array1[j].minute) + ',' + str(final_time_array1[j].second) + ',' \
                          + str(final_temperature_array[j]) + ',' + str(final_dew_array[j]) + ',' + str(final_wind_d_array[j]) + ','\
                          + str(final_wind_s_array[j]) + ',' + str(final_wind_g_array[j]) + ',' + str(final_pressure_array[j]) + ',' + str(final_sky_array[j]) + '\n'

            lines.append(single_line)

        with open(output_files[i], 'w') as f:
            f.writelines(lines)
        a = 0








