import random
from collections import Counter
import numpy


average_time_between_clients, minimum_service_time, maximum_service_time, number_of_barbers = map(int, input().split())
maximum_waiting_time_list = []
maximum_waiting_time_list_b = []
more_than_five = 0
more_than_five_b = 0
closing_delay_sum = 0
closing_delay_sum_b = 0
iterations = 33000


for _ in range(iterations):
    arrival = 0
    customer_arrival_list = []
    barber_info_list = []
    barber_info_list_b = []
    number_of_barbers_b = number_of_barbers -1
    list_of_waiting_minutes = []
    list_of_waiting_minutes_b = []
    maximum_waiting_time = 0
    maximum_waiting_time_b = 0
    number_of_customers = int(numpy.ceil(420 / average_time_between_clients))
    for barber in range(number_of_barbers):
        barber_info_list.append([0, 0])
    for barber in range(number_of_barbers_b ):
        barber_info_list_b.append([0, 0])
    while True:
        arrival += numpy.random.exponential(scale=average_time_between_clients)
        if arrival > 420:
            break
        customer_arrival_list.append(int(arrival))


    for index in range(len(customer_arrival_list)):
        service_time = numpy.random.randint(minimum_service_time, maximum_service_time + 1)
        arrival_time = customer_arrival_list.pop(0)
        customer_waiting_time_list = []
        customer_waiting_time_list_b = []
        serving_barber_index = 0
        # This loop adds the info idle _time of each barber to the barber_info_list
        for barber_index in range(number_of_barbers):
            barber_info_list[barber_index][1] = arrival_time - barber_info_list[barber_index][0]
        for barber_index in range(number_of_barbers_b):
            barber_info_list_b[barber_index][1] = arrival_time - barber_info_list_b[barber_index][0]
        # This function finds out the longest idle _time and defines the serving_barber.
        serving_barber_index, _ = max(enumerate(barber_info_list), key=lambda x: x[1][1])
        serving_barber_index_b, _ = max(enumerate(barber_info_list_b), key=lambda x: x[1][1])
        # This part of the code defines the customer waiting _time
        customer_waiting_time = abs(min(0, barber_info_list[serving_barber_index][1]))
        customer_waiting_time_b = abs(min(0, barber_info_list_b[serving_barber_index_b][1]))
        # print(customer_waiting_time)
        maximum_waiting_time = max(customer_waiting_time, maximum_waiting_time)
        maximum_waiting_time_b = max(customer_waiting_time_b, maximum_waiting_time_b)
        # This part of the code defines the barber x finish _time
        start_time = arrival_time + customer_waiting_time
        start_time_b = arrival_time + customer_waiting_time_b
        finish_time = start_time + service_time
        finish_time_b = start_time_b + service_time
        barber_info_list[serving_barber_index][0] = finish_time
        barber_info_list_b[serving_barber_index_b][0] = finish_time_b
        list_of_waiting_minutes += range(arrival_time, start_time)
        list_of_waiting_minutes_b += range(arrival_time, start_time_b)

    maximum_number_of_people_in_line = Counter(list_of_waiting_minutes).most_common(1)[0][1] if list_of_waiting_minutes else 0
    maximum_number_of_people_in_line_b = Counter(list_of_waiting_minutes_b).most_common(1)[0][1] if list_of_waiting_minutes_b else 0
    maximum_waiting_time_list.append(maximum_waiting_time)
    maximum_waiting_time_list_b.append(maximum_waiting_time_b)
    closing_delay = max(0, finish_time - 420)
    closing_delay_b = max(0, finish_time_b - 420)
    closing_delay_sum += closing_delay
    closing_delay_sum_b += closing_delay_b
    if maximum_number_of_people_in_line > 5:
        more_than_five += 1
    if maximum_number_of_people_in_line_b > 5:
        more_than_five_b += 1

waiting_time_95_quantile = numpy.percentile(maximum_waiting_time_list, 95)
waiting_time_95_quantile_b = numpy.percentile(maximum_waiting_time_list_b, 95)
average_closing_delay = closing_delay_sum / iterations
average_closing_delay_b = closing_delay_sum_b / iterations
probability_more_than_five = (more_than_five / iterations)
probability_more_than_five_b = (more_than_five_b / iterations)

print(waiting_time_95_quantile_b - waiting_time_95_quantile, "\n",
      average_closing_delay_b - average_closing_delay,"\n",
      probability_more_than_five_b - probability_more_than_five, sep=" ")
