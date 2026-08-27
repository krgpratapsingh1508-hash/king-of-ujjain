import csv

# 1. User se input lein ki kaun sa semester chahiye
target_sem = input("Kaun sa Semester chahiye? (1 se 10 ke beech koi bhi number dalein): ").strip()

# Semester ke hisab se numerical year ki mapping
sem_to_year_num = {
    "1": "1", "2": "1",
    "3": "2", "4": "2",
    "5": "3", "6": "3",
    "7": "4", "8": "4",
    "9": "5", "10": "5"
}

target_num = sem_to_year_num.get(target_sem)

if not target_num:
    print("❌ Galat semester number! Kripya 1 se 10 ke beech ka number dalein.")
    exit()

college_name = "GOVT. K.R.G. POST-GRADUATE AUTONOMOUS COLLEGE, GWALIOR (M.P.)"
exam_info = f"Examination :- CCE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; B.A. LL.B. {target_sem}th SEMESTER"

roll_numbers = []

# 2. Master Sheet se data filter karna
try:
    with open('master_sheet.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            roll = row.get('Roll No.', row.get('Roll No', '')).strip()
            student_year = row.get('year', row.get('YEAR', row.get('Year', ''))).strip().lower()
            status = row.get('Status', row.get('STATUS', '')).strip().upper()
            row_sem = row.get('Semester', row.get('SEMESTER', row.get('sem', ''))).strip()
            
            if not roll:
                continue
            
            # Regular aur Ex-students filter logic
            if target_num in student_year and 'REGULAR' in status:
                roll_numbers.append(roll)
            elif 'EX-STUDENT' in status or 'EX' in status:
                if row_sem == target_sem or target_num in student_year or not row_sem:
                    roll_numbers.append(roll)

    # Unique karke sequence me lagayein
    roll_numbers = sorted(list(set(roll_numbers)))

except FileNotFoundError:
    print("❌ Error: 'master_sheet.csv' file nahi mili! Pehle check karein ki file folder me hai.")
    exit()

if not roll_numbers:
    print(f"\n⚠️ Koi data nahi mila! Check karein ki master sheet me sahi data hai ya nahi.")
    exit()


# --- DATA SPLITTING FOR LEFT & RIGHT FOIL TABLES ---
# Pehle 30 students Left Foil ke liye, baaki ke (31 se 60 tak) Right Foil ke liye
left_side_rolls = roll_numbers[:30]
right_side_rolls = roll_numbers[30:60]

# Agar 30 se zyada bacche hain toh poori layout ki width 900px hogi, varna single table ke liye 450px
body_width = "900px" if len(roll_numbers) > 30 else "450px"

# 3. HTML Structure aur CSS Design
html_content = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: Arial, sans-serif; width: {body_width}; margin: auto; padding: 10px; border: 1px solid black; }}
    .top-fields {{ display: flex; justify-content: space-between; margin-bottom: 5px; font-weight: bold; font-size: 13px; }}
    .header-box {{ text-align: center; border-top: 2px solid black; border-bottom: 2px solid black; padding: 5px 0; margin-top: 5px; font-weight: bold; font-size: 15px; }}
    .sub-box {{ border-bottom: 2px solid black; padding: 5px 0; font-size: 12px; font-weight: bold; }}
    .marks-info {{ display: flex; justify-content: space-between; padding: 5px 0; font-weight: bold; border-bottom: 2px solid black; font-size: 12px; }}
    
    /* Side-by-Side Tables Layout */
    .tables-container {{ display: flex; justify-content: space-between; margin-top: 10px; }}
    .foil-block {{ width: { "48%" if len(roll_numbers) > 30 else "100%" }; }}
    
    .foil-title {{ text-align: center; font-weight: bold; background-color: #f2f2f2; border: 1px solid black; border-bottom: none; padding: 4px 0; font-size: 13px; }}
    
    table {{ width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; }}
    th, td {{ border: 1px solid black; padding: 4px; }}
    .col-header-num {{ font-size: 10px; background-color: #f9f9f9; }}
    
    .note {{ font-size: 11px; padding: 8px 4px; border-top: 2px solid black; border-bottom: 2px solid black; text-align: justify; margin-top: 15px; }}
    .footer-fields {{ margin-top: 15px; font-size: 12px; font-weight: bold; line-height: 1.8; }}
</style>
</head>
<body>

    <div class="top-fields">
        <div></div><div>Paper Code....................</div>
    </div>
    <div class="top-fields">
        <div></div><div>Bundle No....................</div>
    </div>

    <div class="header-box">{college_name}</div>
    <div class="sub-box">{exam_info}</div>
    <div class="sub-box">Subject............................................................. Paper...................................</div>
    
    <div class="marks-info">
        <div>Maximum Marks:.............................</div>
<div>Minimum Pass Marks:........................</div>
    </div>
    
    <!-- Left aur Right Tables Ka Container -->
    <div class="tables-container">
    
        <!-- LEFT SIDE FOIL (Rows 1 to 30) -->
        <div class="foil-block">
            <div class="foil-title">FOIL</div>
            <table>
                <tr>
                    <th style="width: 15%;" class="col-header-num">1</th>
                    <th style="width: 85%;" colspan="3" class="col-header-num">2</th>
                </tr>
                <tr>
                    <th rowspan="2">Code No.</th>
                    <th rowspan="2">Roll No.</th>
                    <th colspan="2">Marks Obtained</th>
                </tr>
                <tr>
                    <th style="width: 25%;">In Figures</th>
                    <th>In Words</th>
                </tr>
    """

# Left foil table ki rows generate karna (1 se 30)
for index, roll in enumerate(left_side_rolls, start=1):
    html_content += f"""
                <tr>
                    <td><b>{index}</b></td>
                    <td>{roll}</td>
                    <td></td>
                    <td></td>
                </tr>"""

html_content += """
            </table>
        </div>
"""

# Agar 30 se zyada students hain, toh RIGHT SIDE FOIL table automatic banegi (31 se 60)
if right_side_rolls:
    html_content += f"""
        <!-- RIGHT SIDE FOIL (Rows 31 to 60) -->
        <div class="foil-block">
            <div class="foil-title">FOIL</div>
            <table>
                <tr>
                    <th style="width: 15%;" class="col-header-num">1</th>
                    <th style="width: 85%;" colspan="3" class="col-header-num">2</th>
                </tr>
                <tr>
                    <th rowspan="2">Code No.</th>
                    <th rowspan="2">Roll No.</th>
                    <th colspan="2">Marks Obtained</th>
                </tr>
                <tr>
                    <th style="width: 25%;">In Figures</th>
                    <th>In Words</th>
                </tr>
    """
    
    for index, roll in enumerate(right_side_rolls, start=31):
        html_content += f"""
                <tr>
                    <td><b>{index}</b></td>
                    <td>{roll}</td>
                    <td></td>
                    <td></td>
                </tr>"""
                
    html_content += """
            </table>
        </div>
    """

# Layout ka baki ka hissa aur signatures closure
html_content += """
    </div>
    <!-- Tables Container Ends -->

    <div class="note">
        <b>Note:</b> Roll Number and Marks awarded to the candidate may be entered under respective columns very carefully. Marks and Roll Number should be legible. These may be checked again to ensure that no mistake remains.
    </div>

    <div class="footer-fields">
        Signature of Examiner...........................................................................<br>
        Name of Examiner.................................................................................<br>
        <div style="display: flex; justify-content: space-between;">
            <div>Place...................................................</div>
            <div>Date:___/____/2026</div>
        </div>
    </div>

</body>
</html>
"""

output_filename = f"cce_foil_sem_{target_sem}.html"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\n✅ Success! Total {len(roll_numbers)} students ke sath Left-Right Foil format me '{output_filename}' ban gayi hai.")
