# Stackoverflow insight 2022

<br>
<div align="center">
<img src="https://mms.businesswire.com/media/20210623005665/en/887084/23/logo-stackoverflow-2.jpg" width='600' height='300'>
</div>
<br>

### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## 1. Installation <a name="installation"></a>

- Beyond the Anaconda distribution of Python, there are two libraries needed to be installed: `squarify` and `networkx`
- The code should run with no issues using Python versions 3.*. Currently using Python `3.11.3`

## 2. Project Motivation<a name="motivation"></a>

For this project, I was interested in using Stack Overflow survey data in 2022 to better understand:
1. How do developers learn and level up their coding skill?
2. Which IT career option is interested in advanced education that goes beyond bachelor's degree?
3. Which technologies have been commonly used by developers?

**Note**: `Developers` here mean someone who write code


## 3. File Descriptions <a name="files"></a>

Due to file size limit in Github, Stack Overflow survey data couldn't be pushed to this repo. You can download the full set of data [here](https://info.stackoverflowsolutions.com/rs/719-EMH-566/images/stack-overflow-developer-survey-2022.zip)

There are three notebooks you can find to address the above questions:
-  [Code_Learning_Method.ipynb](https://github.com/hongtranthianh/STACKOVERFLOW-INSIGHT-2022/blob/main/Code_Learning_Method.ipynb) - `Question 1`
- [Education_and_Career.ipynb](https://github.com/hongtranthianh/STACKOVERFLOW-INSIGHT-2022/blob/main/Education_and_Career.ipynb) - `Question 2`
- [Technology.ipynb](https://github.com/hongtranthianh/STACKOVERFLOW-INSIGHT-2022/blob/main/Technology.ipynb) - `Question 3`

There is also three `.py` files in that runs the necessary code across the notebooks.
- [Wrangling_functions.py](https://github.com/hongtranthianh/STACKOVERFLOW-INSIGHT-2022/blob/main/Wrangling_functions.py)
- [Plot_functions.py](https://github.com/hongtranthianh/STACKOVERFLOW-INSIGHT-2022/blob/main/Plot_functions.py)
- [Networkx_function.py](https://github.com/hongtranthianh/STACKOVERFLOW-INSIGHT-2022/blob/main/Networkx_function.py)

## 4. Results<a name="results"></a>

The main findings of the code can be found at the post available [here](https://github.com/hongtranthianh/hongtranthianh.github.io/blob/main/_posts/Stack-Overflow-insight-2022.md)

## 5. Licensing, Authors, Acknowledgements<a name="licensing"></a>

Data is directly taken from [StackOverflow](https://insights.stackoverflow.com/survey/) and licensed under the [ODbL license](https://opendatacommons.org/licenses/odbl/1-0/).

TLDR: Free to use the data

Feel free to use the code here as you would like.

