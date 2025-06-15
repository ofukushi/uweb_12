
r"""
cd /mnt/c/geekom_python_projects/git_projects/uweb_12
cd /mnt/c/fujitsu_python_projects/git_projects/uweb_12
cd C:\geekom_python_projects\git_projects\uweb_12

python3 -m venv .venv
source .venv/bin/activate  
# .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Step into your project directory
cd /mnt/c/geekom_python_projects/git_projects/<your_project>

# Step 1: Initialize Git (if not done already)
git init

# Step 2: Add and commit
git add .
git commit -m "Initial commit for Github"

# Step 3: Ensure branch is named 'main'
git branch -M main

# Step 4: Add remote (if not already added)
git remote add origin git@github.com:ofukushi/<your_repo_name>.git 2>/dev/null || \
git remote set-url origin git@github.com:ofukushi/<your_repo_name>.git

🚀 If Repo Doesn’t Exist Yet
Then replace Step 4 with:
bash
gh repo create <your_repo_name> --public --source=. --push
gh repo create umineko_db_pool --public --source=. --push
gh repo create uweb_12 --public --source=. --push

# Step 5: Push to GitHub
git push -u origin main
"""

uweb_12
project/
├── .env
├── .gitignore
├── app.py
├── Dockerfile
├── Procfile
├── README.md
├── requirements.txt
└── application/
       ├── backend/
       |      ├── __init__.py
       |      ├── auth.py
       |      ├── db_select.py
       |      ├── fetch_company_data.py
       |      ├── filtered_table.py     
       |      └── stock_price.py  #fetch_company_data.pyで呼ばれている
       ├── fonts/
       ├── routes/
       |      ├── __init__.py
       |      ├── dividend_route.py
       |      ├── growth_route.py
       |      ├── record_w52_high_route.py
       |      ├── recordhigh_route.py
       |      └── value_route.py
       ├── static/
       |      ├── css/
       |      ├── js/
       |      └── images/
       ├── templates/
       |       ├── dividend.html
       |       ├── filtered_results.html
       |       ├── growth.html
       |       ├── index.html
       |       ├── login.html
       |       ├── plot.html
       |       ├── record_w52_high.html
       |       ├── recordhigh.html
       |       └── value.html
       ├── __init__.py
       ├── plot_fins_all_bps_opvalues.py
       ├── plot_fins_all_netsales.py
       └── 

