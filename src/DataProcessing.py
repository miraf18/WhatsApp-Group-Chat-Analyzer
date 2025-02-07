import re
import pandas as pd
from typing import Set, Tuple, List

class DataProcessing: 
    def load_and_clean_data(gName: str, raw_path: str, processed_path: str):
        print("⏳ Processing and cleaning the chat...") 
        # Read the file
        with open(raw_path, encoding="utf-8") as fp:
            data = fp.read() 

        # Separate Date - User - Message: "[26/09/24, 22:27:42] Raffo🍪: hi girlz"
        # Advanced regex to capture all components
        pattern = r'''
        \[                      # Opening date bracket
        (\d{2}/\d{2}/\d{2})     # Date (dd/mm/yy)
        ,\s
        (\d{1,2}:\d{2}:\d{2})   # Time (hh:mm:ss)
        \]\s
        ([^:]+)                 # Username (everything until the colon)
        :\s
        (.*?)                   # Message (non-greedy)
        (?=\[|\Z)               # Look ahead for the next date or end of text
        '''
        matches = re.findall(pattern, data, re.VERBOSE | re.DOTALL)

        # Build the columns
        parsed_data = []
        for match in matches:
            date = pd.to_datetime(match[0] + ' ' + match[1], format='%d/%m/%y %H:%M:%S')
            user = match[2].strip()
            message = match[3].replace('\n', ' ').strip()  # Combine multiline messages
            
            parsed_data.append({
                'date': date,
                'user': user,
                'message': message
            })

        # Create DataFrame
        df = pd.DataFrame(parsed_data)

        # Replacing user names with more appropriate or simplified labels for the graph
        # This ensures that we have consistent and readable names for users in the plot.
        df['user'] = df['user'].replace({
            'PippoFranco': 'User1',       # Renaming 'PippoFranco' to 'User1'
            'PaoloRuffini': 'User2',       # Renaming 'PaoloRuffini' to 'User2'
            'ElioELeStorieTese' : 'User3',         # ...
            'Brelusconi' : 'User4', 
        })

        # Filtering out system messages and unwanted lines
        # The following filters are applied to exclude unwanted content such as system notifications, deleted messages, and links.
        df_clean = df[
            (~df['user'].str.contains(gName, na=False)) &                           # Exclude messages from the user with the name 'gName' (group's name) (usually a bot or system)
            (~df['message'].str.contains('omitted', na=False)) &                    # Exclude messages that contain 'omitted', which usually indicates hidden content
            (~df['message'].str.contains('@3', na=False)) &
            (~df['message'].str.contains('You deleted this message', na=False)) &
            (~df['message'].str.contains('pinned a message', na=False)) &
            (~df['message'].str.contains('POLL', na=False)) &
            (~df['message'].str.contains('message was deleted', na=False))&
            (~df['message'].str.contains('http', na=False))&
            (~df['message'].str.contains('https', na=False))
            # add other here
        ].copy()

        
        # Replace the unwanted string with an empty space ONLY in messages that contain it
        # Here, we are searching for the phrase "This message was edited"
        # and replacing it with a single space. This helps remove notifications about edited messages.
        df_clean['message'] = df_clean['message'].str.replace(
            r'\s*<This message was edited>\s*',
            ' ', 
            regex=True,
            case=False,
            flags=re.IGNORECASE 
        )


        df_clean['date'] = pd.to_datetime(df_clean['date'])

        # Save the cleaned data to a CSV file while keeping columns separated
        df_clean.to_csv(
            processed_path, 
            index=False, 
            encoding='utf-8'
        )  

        return df_clean