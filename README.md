# pyeda_example

this simple script take file with truth table in format:

and generate random expression.

you may see help message by typing argument -h:
```bash
$ ./pyeda_generate_expressions.py -h
usage: pyeda_generate_expressions.py [-h] [-s RANDOM_SEED] [-f FILE_PATH]
                                     [-o OUTPUT_FILE_PICTURE]

Generate random expresion from csv table

optional arguments:
  -h, --help            show this help message and exit
  -s RANDOM_SEED, --random-seed RANDOM_SEED
                        random seed value
  -f FILE_PATH, --file-path FILE_PATH
                        path to file with truth table
  -o OUTPUT_FILE_PICTURE, --output-file-picture OUTPUT_FILE_PICTURE
                        path to file where will be saved png picture
 ```
 
 for example, you may run it via following command:
 ```bash
 
 ./pyeda_generate_expressions.py -f ./test_tt1.csv -o graph
 ```
 
