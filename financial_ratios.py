import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import balance_reader as br

def financial_ratios(path):

    # Load data
    df_1 = br.find_variables(path)
    comments_df = pd.read_csv('data/updated_outcomes_with_comments_vf.csv')

    # Clean data
    comments_df ['S_liquidity'] = comments_df ['S_liquidity'].str.lower()
    comments_df ['S_Leverage_Ratio'] = comments_df ['S_Leverage_Ratio'].str.lower()
    comments_df ['S_ROE'] = comments_df ['S_ROE'].str.lower()
    comments_df ['S_Net Revenue Percentage Delta'] = comments_df ['S_Net Revenue Percentage Delta'].str.lower()

    # Assuming data_pivoted is your DataFrame
    #Convert relevant columns to numeric

    #convert Value to string and remove points and commas
    df_1['Value'] = df_1['Value'].astype(str).str.replace('.', '').str.replace(',', '')

    #convert Value to numeric
    df_1['Value'] = pd.to_numeric(df_1['Value'], errors='coerce')

    # Transpone the table to calculate de financial ratios
    data_pivoted = df_1.pivot_table(index='Year', columns='Variable Name', values='Value', aggfunc='first')
    data_pivoted

    # Now calculate the ratios
    data_pivoted['Liquidity Ratio'] = data_pivoted['Current Assets'] / data_pivoted['Current Liabilities']
    data_pivoted['Leverage Ratio'] = data_pivoted['Liabilities'] / data_pivoted['Equity']
    data_pivoted['ROE'] = data_pivoted['Profit'] / data_pivoted['Equity']
    data_pivoted['Net Revenue Percentage Delta'] = data_pivoted['Profit'].pct_change() * 100

    # Now we can create the score columns
    data_pivoted['S_liquidity'] = data_pivoted['Liquidity Ratio'].apply(lambda x: 'green' if x > 1 else ('red' if x < 0.5 else 'yellow'))
    data_pivoted['S_Leverage_Ratio'] = data_pivoted['Leverage Ratio'].apply(lambda x: 'green' if x > 0.8 else ('red' if x < 0.2 else 'yellow'))
    data_pivoted['S_ROE'] = data_pivoted['ROE'].apply(lambda x: 'green' if x > 0.03 else ('red' if x < 0 else 'yellow'))
    data_pivoted['S_Net Revenue Percentage Delta'] = data_pivoted['Net Revenue Percentage Delta'].apply(lambda x: 'green' if x > 0.01 else ('red' if x < 0 else 'yellow'))

    # Merge the data with the comments
    merged_df = pd.merge(data_pivoted, comments_df , on=['S_liquidity', 'S_Leverage_Ratio', 'S_ROE', 'S_Net Revenue Percentage Delta'], how='left')

    ## Individual comments
    # create a new column as liquidity comments which is based on column S_liquidity -	red	-Watch out! Your liquidity is too low. You don't even have half the money to cover your short-term responsibilities,yellow -	You've got some cash to handle your short-term debts, but you're not fully covered. It's time to come up with a strategy to boost your liquidity,green -Congratulations! You've covered all your short-term liabilities. Great job!
    merged_df['Liquidity Comments'] = merged_df['S_liquidity'].apply(lambda x: 'Watch out! Your liquidity is too low. You don\'t even have half the money to cover your short-term responsibilities' if x == 'red' else ('You\'ve got some cash to handle your short-term debts, but you\'re not fully covered. It\'s time to come up with a strategy to boost your liquidity' if x == 'yellow' else 'Congratulations! You\'ve covered all your short-term liabilities. Great job!'))							

    ## create a new column as 'ROE comments' which is based on column S_ROE : 	ROE 	RED		Your profit is in the red, meaning you're not adding value for your shareholders. It's time to rethink your strategy.YELLOW 		Even though you're making some money, there's still work to be done. Your shareholders will be happier with improvements.GREEN 		Amazing job! Your returns look great, but remember, there's always room for improvement.
    merged_df['ROE comments'] = merged_df['S_ROE'].apply(lambda x: 'Your profit is in the red, meaning you\'re not adding value for your shareholders. It\'s time to rethink your strategy.' if x == 'red' else ('Even though you\'re making some money, there\'s still work to be done. Your shareholders will be happier with improvements.' if x == 'yellow' else 'Amazing job! Your returns look great, but remember, there\'s always room for improvement.'))

    #create a new column as 'Leverage Ratio comments' which is based on column S_Leverage_Ratio : RED		Be careful! Your debt is too high. Decrease it as soon as possible (ASAP).YELLOW 	Your debt is high, but you're still within an acceptable range. Try not to increase it further.GREEN 		Congratulations! You're in a very comfortable position with your debt.
    merged_df['Leverage Ratio comments'] = merged_df['S_Leverage_Ratio'].apply(lambda x: 'Be careful! Your debt is too high. Decrease it as soon as possible (ASAP).' if x == 'red' else ('Your debt is high, but you\'re still within an acceptable range. Try not to increase it further.' if x == 'yellow' else 'Congratulations! You\'re in a very comfortable position with your debt.'))

    #create a new column as 'Net Revenue Percentage Delta Comments' which is based on column S_Net Revenue Percentage Delta : 	LEVERAGE RATIO 	RED		Be careful! Your debt is too high. Decrease it as soon as possible (ASAP).YELLOW 		Your debt is high, but you're still within an acceptable range. Try not to increase it further.GREEN 		Congratulations! You're in a very comfortable position with your debt.
    merged_df['Net Revenue Percentage Delta Comments'] = merged_df['S_Net Revenue Percentage Delta'].apply(lambda x: 'Your profit is in the red, meaning you\'re not adding value for your shareholders. It\'s time to rethink your strategy.' if x == 'red' else ('Even though you\'re making some money, there\'s still work to be done. Your shareholders will be happier with improvements.' if x == 'yellow' else 'Amazing job! Your returns look great, but remember, there\'s always room for improvement.'))

    return merged_df