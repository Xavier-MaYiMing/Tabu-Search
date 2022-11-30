### Tabu Search

##### Reference: Glover, Fred. Tabu Search-- Part I.[J]. ORSA Journal on Computing, 1989.

##### The tabu search for the traveling salesman problem

| Variables  | Meaning                                                      |
| ---------- | ------------------------------------------------------------ |
| x          | The x coordinates of cities (list)                           |
| y          | The y coordinates of cities (list)                           |
| iter       | The maximum number of iterations                             |
| city_num   | The number of cities                                         |
| na         | The number of actions                                        |
| dis        | The distance matrix, dis\[i\]\[j\] denotes the distances between city i and city j |
| TC         | The tabu counter (list)                                      |
| TL         | The tabu length                                              |
| gbest      | The length of the global best path                           |
| gbest_path | The global best path (list)                                  |
| iter_best  | The length of the global best path of each iteration (list)  |
| con_iter   | The last iteration number when "gbest" is updated            |

#### Example

```python
if __name__ == '__main__':
    min_coord = 0
    max_coord = 10
    city_num = 30
    iter = 50
    x = [random.uniform(min_coord, max_coord) for _ in range(city_num)]
    y = [random.uniform(min_coord, max_coord) for _ in range(city_num)]
    print(main(x, y, iter))
```

##### Output:

![](https://github.com/Xavier-MaYiMing/Tabu-Search/blob/main/TS-for-TSP.gif)

![](https://github.com/Xavier-MaYiMing/Tabu-Search/blob/main/convergence%20iteration.png)

The TS converges at its 20-th iteration, and the global best value is 46.273638987858966. 

```python
{
    'best length': 46.273638987858966, 
    'best path': [16, 6, 15, 20, 24, 25, 5, 21, 12, 22, 18, 28, 14, 4, 0, 26, 2, 27, 7, 10, 9, 17, 11, 19, 23, 3, 29, 13, 1, 8], 
    'convergence iteration': 20
}
```

