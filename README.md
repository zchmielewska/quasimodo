quasimodo facilitates data comparison

How quasimodo behaves when...?

**Example: Numerical values**

Left     Right    Output

|v1|v2|  |v1|v2|  |v1|v2|  
|--|--|  |--|--|  |--|--|  
| 1| 4|  | 1| 1|  | 0| 3|  
| 2| 5|  | 1| 1|  | 1| 4|  
| 3| 6|  | 1| 1|  | 2| 5|  

Output contains the values from the left table less the value from the right table.

**Example: Characters**

Left     Right    Output

|v1|v2|  |v1|v2|  |v1   |v2   |  
|--|--|  |--|--|  |-----|-----|  
| a| d|  | a| e|  |TRUE |FALSE|  
| b| e|  | a| e|  |FALSE|TRUE |  
| c| f|  | a| e|  |FALSE|FALSE|  

Output contains TRUE if the strings are the same and FALSE otherwise.

**Example: Numerical and characters**

Left     Right    Output

|v1|v2|  |v1|v2|  |v1   |v2   |  
|--|--|  |--|--|  |-----|-----|  
| 1| d|  | a| e|  |FALSE|FALSE|  
| 2| e|  | a| e|  |FALSE|TRUE |  
| 3| f|  | a| e|  |FALSE|FALSE|  

Numerical values are compared as characters.

**Example: Different columns**

Left     Right    Output

|v1|v2|  |v1|v3|  |v1|v2          |v3           |
|--|--|  |--|--|  |--|------------|-------------|
| 1| 4|  | 1| a|  | 0|only_in_left|only_in_right|
| 2| 5|  | 2| b|  | 0|only_in_left|only_in_right|
| 3| 6|  | 3| c|  | 0|only_in_left|only_in_right|

**Example: Different number of rows**

|v1|v2|  |v1|v2|  |v1|v2|  
|--|--|  |--|--|  |--|--|  
| 1| 4|  | 1| 1|  | 0| 3|  
| 2| 5|  | 1| 1|  | 1| 4|  
| 3| 6|           | 2| 5|  
