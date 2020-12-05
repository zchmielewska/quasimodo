quasimodo facilitates data comparison

How quasimodo behaves when comparing...?

**Numerical values**

Left   

|v1|v2|
|--|--|
| 1| 4|
| 2| 5|
| 3| 6|

Right

|v1|v2|
|--|--|
| 1| 1|
| 1| 1|  
| 1| 1|

Output

|v1|v2|  
|--|--|  
| 0| 3|
| 1| 4|
| 2| 5|

Output contains the values from the left table minus the values from the right table.

**Characters**

Left     

|v1|v2|  
|--|--|  
| a| d|  
| b| e|  
| c| f|  

Right    

|v1|v2|  
|--|--|  
| a| e|  
| a| e|  
| a| e|  

Output

|v1   |v2   |  
|-----|-----|  
|TRUE |FALSE|  
|FALSE|TRUE |  
|FALSE|FALSE|  

Output contains TRUE if the strings are the same and FALSE otherwise.

**Numerical and characters**

Left     

|v1|v2|  
|--|--|  
| 1| d|  
| 2| e|  
| 3| f|  

Right    

|v1|v2|  
|--|--|  
| a| e|  
| a| e|  
| a| e|  

Output

|v1   |v2   |  
|-----|-----|  
|FALSE|FALSE|  
|FALSE|TRUE |  
|FALSE|FALSE|  

Numerical values are converted into characters and compared in the same way as characters.

**Different column names**

Left     

|v1|v2|  
|--|--|  
| 1| 4|  
| 2| 5|  
| 3| 6|  

Right    

|v1|v3|  
|--|--|  
| 1| d|  
| 1| e|  
| 1| f|  

Output

|v1|v2          |v3           |
|--|------------|-------------|
| 0|only_in_left|only_in_right|
| 1|only_in_left|only_in_right|
| 2|only_in_left|only_in_right|

If there are columns in only one of the tables, the output contains the information either "only_in_left" or "only_in_right".

**Different number of rows**

Left

|v1|v2|  
|--|--|  
| 1| d|  
| 2| e|  
| 3| f|           

Right

|v1|v2|  
|--|--|  
| 1| e|  
| 1| e|  

Output

|v1|v2    |  
|--|------|  
| 0| FALSE|  
| 1| TRUE |  
| 3| FALSE|  

The missing row is filled with zeros for numerical values and empty strings for characters.
