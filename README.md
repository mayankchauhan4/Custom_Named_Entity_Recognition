# Custom_Named_Entity_Recognition
Named entity recognition from CSV file or database. Provide the list of entities in CSV and Extract label from sentences

You can use spacy or google naural language API to extract entities from text ,you can train your own model or use their pretrained models but the accuracy is not always 100% for some names or entities. if your data is sensitive and there cannnot be a spelling mistake or missing word . you can use this code.

Step 1 - Open the CSV file ,Check the columns I have created .Just paste your data in the same format, thats it. run the code and extract entites from text.

You can store your data in database in the same format and connect the database insted of CSV file. 

You can create alias name for entities you want to find it from diffrent name.

Example for CONDITIONAL_ALIAS :

Jammu & kashmir - Jammu & kashmir 

Jammu & kashmir - Jammu and kashmir

Jammu & kashmir - J & K

Open the CSV and look for this exmaple. If your entity have a alias name you have to set 'yes' in CONDITIONAL_ALIAS Column else 'no'.

