# SMALL USE EXPLANATION FOR OTHERS

This is our project's library: ... .

To use it from outside like in a notebook, here's a sample of code.

```py
# In case you need to add it's path cause your notebook is in a subfolder
import sys
import os
library_path = os.path.abspath(os.path.join(os.getcwd(), '..'))
if library_path not in sys.path:
    sys.path.append(library_path)

# And in every case
from library import *
```