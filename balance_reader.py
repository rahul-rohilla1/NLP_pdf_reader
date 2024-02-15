import pytesseract
from pdf2image import convert_from_path
import re
import pandas as pd
from io import StringIO
from openai import OpenAI


#API key
client = OpenAI(api_key=st.secrets["openai_key"])

#Configure the prompt from OpenAI
def get_response(prompt):
  # Create a request to the chat completions endpoint
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    # Assign the role and content for the message
    messages=[{"role": "user", "content": prompt}],
    temperature = 0
    #seed = 123
    )
  return response.choices[0].message.content

#Calculate the percentage of words that are numbers. For Relevant Pages
def numbers_percentage(text):
    cleaned_text = text.replace('\n', ' ').replace('.', '').replace(',', '')
    numbers = re.findall(r'\b\d+\b', cleaned_text)
    total_words = len(cleaned_text.split())
    total_numbers = len(numbers)
    percentage_numbers = total_numbers / total_words
    return percentage_numbers

#Define the prompt on the retrieve text from the PDF
def look_variables_in_text(text):
    response = get_response("Generate only a table with columns for Company Name, Year, Variable Name, and Value. Start and finish the table with '|'. The desired variables are Current Assets, Assets, Equity, Current Liabilities, Liabilities, and Profit. If any variable is not found, do not retrieve it. Only create rows for the variables that are found. Look in the following text: "
                           + text)
    return response

#Generates the dataframe from the output text of OpenAI
def generate_dataframe(text):
    
    table_text = text[text.index('|'):text.rindex('|')+1] #Only values inside the table delimitator |
    df = pd.read_csv(StringIO(table_text), sep='|', skiprows=0, skipinitialspace=True) #Simulate a csv file where separator is |
    df.columns = df.columns.str.strip() #Trim all empty spaces con column names
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  #Trim all empty spaces con values names
    df = df.iloc[1:, 1:-1] #Remove first and last column + first row.
    
    return df

# Perform OCR and IR on pages. Stop when all variables are filled
def find_variables(path):
    pages = convert_from_path(path) # Convert PDF to images
    
    wanted_variables = ['Current Assets', 'Assets', 'Equity', 'Current Liabilities', 'Liabilities', 'Profit']

    text_data = []  #Individual text of relevant pages
    concat_text = ''  #Concatenated pages
    count_pages = 0   #Counter on how many pages are concatenated
    count_promt = 0   #Counter on how many times we have execute a prompt

    final_dataframe = pd.DataFrame()

    #For Loop to perform Early Stoping. Will stop when all variables have been found. 
    for page in pages:
        text = pytesseract.image_to_string(page, config='--psm 6')
        perc_number = numbers_percentage(text) 
        if perc_number > 0.2:  #Relevant page has more than 20% on numbers over total of words
            count_pages += 1
            text_data.append(text) #NON relevant
            concat_text = concat_text + text
            if count_pages == 3:  #Group 3 relevat pages befores searching

                count_promt += 1 #+1 Prompt executed concatenated
                count_pages = 0   #Restart page counter

                prompt_output = look_variables_in_text(concat_text)   #Generate and execute prompt. Retrieve response
                retrieved_variables = generate_dataframe(prompt_output)  #Generate dataframe from prompt output

                concat_text = ''  #Restart string for prompt

                if 'Variable Name' not in retrieved_variables.columns:
                    print("Warning: DataFrame does not have a column named 'Variable Name'. Skipping this value.")
                    continue
                remove_wanted = []
                for value in wanted_variables:
                    if value in retrieved_variables['Variable Name'].values:
                        final_dataframe = pd.concat([final_dataframe, retrieved_variables[retrieved_variables['Variable Name'] == value]], ignore_index=True)
                        remove_wanted.append(value)
                wanted_variables = [x for x in wanted_variables if x not in remove_wanted]

                #Breaks if all variables have been found. 
                if len(wanted_variables) == 0:
                    break
    return final_dataframe