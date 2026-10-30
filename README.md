# DCP 2026 Assignment
Assignment for Data Centric Programming 2026

# Description
This project will analyse my daily commute from Kildare into Dublin Heuston. I will be comparing the actual arrival time of trains compared to their scheduled times, the origin of the train, the amount of stops before and after my destination and also the actual arrival time in comparison to the expected one.


# CSV File
My CSV contains 13 attributes

| Column | Type of Data | Purpose |
|---|---|---|
| ID | Primary Key | The ID is simply here to act as a unique identifier, as I usually get similarly timed trains, this just acts as the primary key|
| Date | Date | Date will show what day the train was taken on, as previously mentioned I get similarly timed trains so this can be used to see which days of the week tend to be busiest |
| My_origin | Categorical | This displays the stop which I get on the train |
| Train_origin | Categorical | Where the train originated |
| My_destination | Categorical | The station where I plan to get off the train |
| Train_destination | Categorical | Where the train terminates |
| Due_time | Numerical / Time | The time when the train is scheduled to arrive at my_origin |
| Actual_due_time | Numerical / Time | The time when the train arrives at my_origin |
| Arrival_time | Numerical / Time | The time when the train is scheduled to reach my_destination |
| Actual_arrival_time | Numerical / Time | The when the train actually reachs my_destionation |
| Previous_stops | Numerical | The number before my_origin |
| Later_stops | Numerical | Number of stops between my_origin and my_destination |
| Comments | String | An additional column to account for anything that might delay the train significantly and potentially skew the results |
