import os, pandas as pd

def save_to_new_folder(data, file_name):
    df = pd.DataFrame(data)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    new_folder_name = pd.Timestamp.now().strftime('%Y-%m-%d')
    new_folder_path = os.path.join(script_dir, new_folder_name)
    file_path = os.path.join(new_folder_path, file_name)

    # if not os.path.exists(new_folder_path):
    #     os.makedirs(new_folder_path)
    # file_path = os.path.join(new_folder_path, 'output.csv')
    # df.to_csv(file_path, index = False)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        df.to_csv(file_path, index=False)
    else:
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, index=False)

data = []
data.append({'job_title': 'frontend',
            'company_name': 'pt xyz',
            'job_location': 'surabaya'})
file_name = 1 
save_to_new_folder(data,'output.csv')


