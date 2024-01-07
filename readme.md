 ### BBS671 HW 2 - Earliest Deadline First (EDF) & Rate Monotonic (RM) Scheduling Implementation

## How to run
1. Clone the repository
2. Run the following command in the terminal: `python3 schedular.py --taskset <taskset> --save_log <save_log> --show_plot <show_plot> `

## Example TaskSet
````jsonj
{
    "tasks": [
        {
            "execution_time": 2,
            "period": 10
        },
        {
            "execution_time": 1,
            "period": 10
        },
        {
            "execution_time": 1,
            "period": 5
        },
        {
            "execution_time": 3,
            "period": 15
        },
        {
            "execution_time": 4,
            "period": 15
        }
    ]
}
````
#### Test 0_1
![Test0_1_EarliestDeadLineFirstStrategy.png](outputs%2FTest0_1_EarliestDeadLineFirstStrategy.png)
![Test0_1_RateMonotonicStrategy.png](outputs%2FTest0_1_RateMonotonicStrategy.png)

#### Test 0_2
![Test0_2_EarliestDeadLineFirstStrategy.png](outputs%2FTest0_2_EarliestDeadLineFirstStrategy.png)
![Test0_2_RateMonotonicStrategy.png](outputs%2FTest0_2_RateMonotonicStrategy.png)

#### Test 1
![Test1_EarliestDeadLineFirstStrategy.png](outputs%2FTest1_EarliestDeadLineFirstStrategy.png)
![Test1_RateMonotonicStrategy.png](outputs%2FTest1_RateMonotonicStrategy.png)

#### Test 2
![Test2_EarliestDeadLineFirstStrategy.png](outputs%2FTest2_EarliestDeadLineFirstStrategy.png)
![Test2_RateMonotonicStrategy.png](outputs%2FTest2_RateMonotonicStrategy.png)

#### Test 3
![Test3_EarliestDeadLineFirstStrategy.png](outputs%2FTest3_EarliestDeadLineFirstStrategy.png)
![Test3_RateMonotonicStrategy.png](outputs%2FTest3_RateMonotonicStrategy.png)

#### Test 4
![Test4_EarliestDeadLineFirstStrategy.png](outputs%2FTest4_EarliestDeadLineFirstStrategy.png)
![Test4_RateMonotonicStrategy.png](outputs%2FTest4_RateMonotonicStrategy.png)

#### Test 5
![Test5_EarliestDeadLineFirstStrategy.png](outputs%2FTest5_EarliestDeadLineFirstStrategy.png)
![Test5_RateMonotonicStrategy.png](outputs%2FTest5_RateMonotonicStrategy.png)