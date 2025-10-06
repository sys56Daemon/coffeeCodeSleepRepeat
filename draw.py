import os
import subprocess
import shutil
import time
from datetime import datetime, timedelta
import random

# ==========================
# Style and Colors
# ==========================
class style:
    RESET = '\033[0m'
    BOLD = '\033[01m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'

BANNER = style.GREEN + style.BOLD + r"""
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⣿⡏⣿⡿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⡍⣉⠽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣾⣿⣷⠲⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣷⢻⣷⣮⣝⡻⢿⣿⣿⣿⣿⣿⢣⣿⣿⣿⣿⡄⠀⠀⢸⣿⣿⣿⣿⣿⣿⠿⠛⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣟⡊⣿⣿⣿⣿⣷⣬⣛⠛⣻⢃⣿⣿⣿⣿⣿⣧⠀⠀⠀⣛⣻⣿⠟⣋⣵⡞⠀⣿⣟⣛⠛⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⡘⣿⣿⣿⣿⣿⣿⣷⣍⣼⣿⣿⣿⣿⣿⣿⡄⠀⢀⣨⣭⣶⣿⣿⣿⠁⠰⠟⠋⠁⢰⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣷⡹⣿⣿⣿⣿⣿⣿⡿⢟⣛⣫⣭⣽⣛⣻⠷⣾⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡹⣿⣿⣿⢛⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⡻⣿⣿⣿⣿⠃⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿
                            ⣫⢿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣿⡿⣱⣿⣿⣿⣿⠿⣛⡭⢟⣩⣽⣿⠿⠿⠿⣎⢿⣿⣿⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿
                            ⣿⣷⣮⠛⢿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣟⣻⣴⣭⡷⢟⣻⣭⠷⣞⣛⣯⣥⣾⣦⢻⣿⣦⣤⣤⣄⡀⢉⣬⡉⠙⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣦⡝⢿⣿⣿⣿⣿⡏⡾⢛⣯⣭⣭⡵⠶⢟⣫⣥⣶⢿⣿⣿⣿⣷⣭⡻⣏⢿⣿⣿⣿⠟⣡⡿⠋⠐⠺⠿⠿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣬⣛⢿⣿⣿⡇⣷⡶⣾⣶⣶⣿⣶⣝⢿⣿⢧⣿⡿⠿⠟⢛⣿⣧⡸⡜⣿⣿⠋⠒⠉⠀⠀⠀⠀⠀⢀⣠⣾
                            ⣿⣿⣿⣿⣿⣿⣿⠿⣃⣼⣿⡇⠟⣼⣿⣿⣿⠿⢟⣛⣃⢿⡄⣶⣾⣿⣶⣿⣿⣿⢃⣇⢿⣿⣷⣄⡀⠀⠀⠀⣠⣶⣿⣿⣿
                            ⣿⣿⡟⠟⣛⣭⣵⣾⣿⣿⣿⣷⢰⢙⣭⣷⣦⣼⣿⣿⡟⣸⣷⣝⠿⣿⣿⣿⠿⣫⣾⣿⠸⣿⣿⣿⡿⢂⣤⠀⠙⠿⢿⣿⣿
                            ⣿⣿⣿⣷⣮⣝⡻⢿⣿⣿⣿⣿⡸⣧⡹⢿⣿⣿⡿⢟⣵⢻⣿⡏⣿⣶⣶⣶⠟⠋⣰⣿⠄⣭⡻⡏⠰⠛⠁⠀⠀⠀⠙⠻⣿
                            ⣿⣿⣿⣿⣿⣿⣦⡄⠈⠙⢿⣿⡇⢿⣿⢷⣶⣶⡾⢟⣽⡇⣿⣿⢸⣦⣤⣤⣴⣾⣿⣿⠀⢸⡿⢠⠀⠀⠀⠀⠀⠀⣠⣴⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⣸⣿⢋⣸⣿⣷⣶⣶⣿⣿⣿⣿⡜⠟⣸⣿⣿⣿⣿⣿⣿⣿⠀⠀⢠⣿⡄⣄⠀⢠⣶⣶⣶⣾⣿
                            ⣿⣿⣿⣿⣿⣿⡿⢟⣩⣾⣿⡇⣿⣧⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⣯⡉⠀⡈⠐⠒⠛⠉⠀⠀⠙⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣭⣤⣭⣭⣛⣛⡍⣮⣙⡘⣿⣿⣿⣿⡿⢛⡩⣽⣶⣶⢇⣾⣿⣿⣿⡿⠁⠁⣷⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣁⠀⣿⣿⣷⡹⣇⠻⣵⣾⣿⣿⢶⡹⣿⢹⠿⣿⣿⣿⠏⡀⠈⠉⠁⠀⠀⠰⣶⣶⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣃⣟⣋⡡⠀⡙⣿⣿⣿⣿⣿⣤⣿⣶⣾⣤⣼⡿⠋⠀⠁⠀⠀⠀⠀⢀⣀⣹⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠉⢈⡻⢿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⠀⣈⢩⣝⣛⣫⣭⣄⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⡶⢖⡂⡄⣨⣛⡿⠿⠿⢟⡀⠀⠀⣀⠰⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿
                            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣋⣵⣾⡟⣵⠇⣿⣿⣿⣿⣿⣿⣿⡄⣷⡩⣽⡶⣭⡛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿
""" + style.RESET

CREDITS = style.CYAN + "                                                *[BURPS]* " + style.RESET

DISCLAIMER = f"""
{style.YELLOW}{style.BOLD}Disclaimer:{style.RESET}{style.YELLOW}
This tool modifies your Git history. It's strongly recommended to use it on a new, dedicated repository.
The creator is not responsible for any unintended consequences.
If you dislike the result, you will need to manually delete the repository.{style.RESET}
"""

# ==========================
# ASCII Art & Animations
# ==========================
FONT = {
    'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001'], 'B': ['11110', '10001', '10001', '11110', '10001', '10001', '11110'],
    'C': ['01110', '10001', '10000', '10000', '10000', '10001', '01110'], 'D': ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
    'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'], 'F': ['11111', '10000', '10000', '11110', '10000', '10000', '10000'],
    'G': ['01110', '10001', '10000', '10111', '10001', '10001', '01110'], 'H': ['10001', '10001', '10001', '11111', '10001', '10001', '10001'],
    'I': ['01110', '00100', '00100', '00100', '00100', '00100', '01110'], 'J': ['00011', '00001', '00001', '00001', '10001', '10001', '01110'],
    'K': ['10001', '10010', '10100', '11000', '10100', '10010', '10001'], 'L': ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
    'M': ['10001', '11011', '10101', '10101', '10001', '10001', '10001'], 'N': ['10001', '11001', '10101', '10011', '10001', '10001', '10001'],
    'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'], 'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
    'Q': ['01110', '10001', '10001', '10001', '10101', '10010', '01111'], 'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
    'S': ['01111', '10000', '10000', '01110', '00001', '00001', '11110'], 'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
    'U': ['10001', '10001', '10001', '10001', '10001', '10001', '01110'], 'V': ['10001', '10001', '10001', '10001', '10001', '01010', '00100'],
    'W': ['10001', '10001', '10001', '10101', '10101', '11011', '10001'], 'X': ['10001', '10001', '01010', '00100', '01010', '10001', '10001'],
    'Y': ['10001', '10001', '01010', '00100', '00100', '00100', '00100'], 'Z': ['11111', '00001', '00010', '00100', '01000', '10000', '11111'],
    '0': ['01110', '10001', '10101', '10101', '10101', '10001', '01110'], '1': ['00100', '01100', '00100', '00100', '00100', '00100', '01110'],
    '2': ['01110', '10001', '00001', '00010', '00100', '01000', '11111'], '3': ['11110', '00001', '00001', '01110', '00001', '00001', '11110'],
    '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'], '5': ['11111', '10000', '10000', '11110', '00001', '10001', '01110'],
    '6': ['01110', '10001', '10000', '11110', '10001', '10001', '01110'], '7': ['11111', '00001', '00010', '00100', '01000', '01000', '01000'],
    '8': ['01110', '10001', '10001', '01110', '10001', '10001', '01110'], '9': ['01110', '10001', '10001', '01111', '00001', '10001', '01110'],
    ' ': ['00000', '00000', '00000', '00000', '00000', '00000', '00000'], '!': ['00100', '00100', '00100', '00100', '00100', '00000', '00100'],
    '?': ['01110', '10001', '00001', '00010', '00100', '00000', '00100'], '.': ['00000', '00000', '00000', '00000', '00000', '00100', '00100'],
    ',': ['00000', '00000', '00000', '00000', '00100', '00100', '00010'], '-': ['00000', '00000', '00000', '11111', '00000', '00000', '00000'],
    '_': ['00000', '00000', '00000', '00000', '00000', '00000', '11111'], ':': ['00000', '00100', '00100', '00000', '00100', '00100', '00000'],
    ';': ['00000', '00100', '00100', '00000', '00100', '00100', '00010'], '\'': ['00100', '00100', '00000', '00000', '00000', '00000', '00000'],
    '"': ['01010', '01010', '00000', '00000', '00000', '00000', '00000'], '+': ['00000', '00100', '00100', '11111', '00100', '00100', '00000'],
    '❤': ['01010', '11111', '11111', '01110', '00100', '00000', '00000'],
}

ANIMATIONS = [
    [ # Dancing Girl
        r"""
( o_o)/""",
        r"""
\(o_o )""",
        r"""
(o_o )/""",
        r"""
\( o_o)""",
    ],
    [
        r"(>'-')>",
        r"<('-'<)",
        r"^('-')^",
        r"v('-')v",
    ],
    [
        r"\n /\_/\  \n( o.o ) \n > ^ <  \n",
        r"\n /\_/\  \n( o.o ) \n> ^ <   \n( ( ) )  \n`\"\"\"\"`  \n",
    ]
]

# ==========================
# Core Functions
# ==========================
def build_grid(text, total_columns=52):
    spacing = 1; rows = 7; grid = [[] for _ in range(rows)]; unsupported_chars = set()
    for char in text.upper():
        if char in FONT:
            for r, row_pattern in enumerate(FONT[char]): grid[r].extend(list(row_pattern))
            for r in range(rows): grid[r].extend(["0"] * spacing)
        else: unsupported_chars.add(char)
    if unsupported_chars: print(f"{style.YELLOW}Warning: Unsupported characters will be skipped: {''.join(unsupported_chars)}{style.RESET}")
    if not any(grid): return [[0] * total_columns for _ in range(rows)]
    factor = total_columns / len(grid[0]) if len(grid[0]) > 0 else 1
    return [[grid[r][int(c / factor)] for c in range(total_columns)] for r in range(rows)]

def get_start_date(year):
    d = datetime(year, 1, 1)
    while d.weekday() != 6: d -= timedelta(days=1)
    return d

def make_commit(commit_date, message):
    with open("commit.txt", "a") as f: f.write(f"Commit for {commit_date.isoformat()}\n")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_date.isoformat()
    env["GIT_COMMITTER_DATE"] = commit_date.isoformat()
    commit_message = message if message else f"ghART commit for {commit_date.strftime('%Y-%m-%d')}"
    subprocess.run(["git", "add", "commit.txt"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", commit_message, "--date", commit_date.isoformat()], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_commit_dates(year, mode, text=""):
    start_date = get_start_date(year); dates = []
    if mode == 'text':
        grid = build_grid(text)
        for col in range(len(grid[0])):
            for row in range(len(grid)):
                if grid[row][col] == "1":
                    commit_date = start_date + timedelta(weeks=col, days=row)
                    if commit_date.year == year: dates.append(commit_date)
    else:
        day_iterator = timedelta(days=1); current_date = datetime(year, 1, 1); end_date = datetime(year, 12, 31)
        while current_date <= end_date:
            if mode == 'fill' or (mode == 'random' and random.random() < 0.4): dates.append(current_date)
            current_date += day_iterator
    return dates

# ==========================
# Git & Safety Functions
# ==========================
def is_git_installed(): return shutil.which("git") is not None

# ==========================
# UI & Execution Functions
# ==========================
def get_user_params(mode):
    params = {}
    while True:
        try: 
            year_prompt = f"Enter the year to draw in [{style.BOLD}{datetime.now().year}{style.RESET}]: "
            year_input = input(year_prompt)
            params['year'] = int(year_input) if year_input else datetime.now().year
            break
        except ValueError: print(f"{style.RED}Invalid input. Please enter a number.{style.RESET}")
    
    if mode == 'text':
        while True:
            try: 
                level_input = input(f"Enter commit count for each pixel (e.g., 5) [{style.BOLD}1{style.RESET}]: ")
                level = int(level_input) if level_input else 1
                if level > 0: params['min_commits'] = params['max_commits'] = level; break
                else: print(f"{style.RED}Please enter a positive number.{style.RESET}")
            except ValueError: print(f"{style.RED}Invalid input. Please enter a number.{style.RESET}")
    else: # Fill or Random
        while True:
            try: 
                min_input = input(f"Enter minimum commits per day [{style.BOLD}1{style.RESET}]: ")
                params['min_commits'] = int(min_input) if min_input else 1
                max_input = input(f"Enter maximum commits per day [{style.BOLD}5{style.RESET}]: ")
                params['max_commits'] = int(max_input) if max_input else 5
                if params['min_commits'] > 0 and params['max_commits'] >= params['min_commits']:
                    break
                else: print(f"{style.RED}Invalid range. Ensure min is not negative and max is >= min.{style.RESET}")
            except ValueError: print(f"{style.RED}Invalid input. Please enter a number.{style.RESET}")

    params['message'] = input(f"Enter a custom commit message (optional): ")
    return params

def run_ghart(mode, params):
    commit_dates = get_commit_dates(params['year'], mode, text=params.get('text', ""))
    if not commit_dates: 
        print(f"{style.YELLOW}No commit dates were generated. Exiting.{style.RESET}"); return

    min_c, max_c = params['min_commits'], params['max_commits']
    animation = random.choice(ANIMATIONS)
    total_days = len(commit_dates)
    
    print(f"\nGenerating commits for {style.BOLD}{params['year']}{style.RESET}. This may take a moment...")
    with open("commit.txt", "w") as f: f.write("ghART commit log\n")

    print(style.HIDE_CURSOR, end="")
    try:
        for i, date in enumerate(sorted(commit_dates)):
            # Animation display - simplified to clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            frame = animation[i % len(animation)]
            print(f"{style.GREEN}{frame}{style.RESET}")
            print(f"{style.BOLD}Processing day {i+1}/{total_days}...{style.RESET}")

            commits_today = random.randint(min_c, max_c)
            for _ in range(commits_today):
                make_commit(date, params['message'])
            time.sleep(0.05)

    finally:
        print(style.SHOW_CURSOR, end="")

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{style.BOLD}{style.GREEN}✅ Done! All commits have been created locally.{style.RESET}")
    time.sleep(1)
    print(f"\n{style.YELLOW}Please note:{style.RESET} It may take a few minutes for your contributions to appear on your GitHub graph.")
    print(f"\n{style.BOLD}Next steps:{style.RESET}")
    print(f"1. Set your remote repository: {style.CYAN}git remote add origin https://github.com/user/repo.git{style.RESET}")
    print(f"2. Push your changes: {style.CYAN}git push -u origin main --force{style.RESET}")

def main():
    if not is_git_installed():
        print(f"{style.RED}Error: Git is not installed or not found in PATH. Please install Git to use this tool.{style.RESET}"); return
    if not os.path.exists(".git"): 
        print(f"{style.GREEN}Initializing new git repository...{style.RESET}"); subprocess.run(["git", "init"], stdout=subprocess.DEVNULL)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(BANNER)
        print(CREDITS)
        print(DISCLAIMER)
        print(f"\n{style.BOLD}--- Main Menu ---{style.RESET}")
        print("1. Create Text Art")
        print("2. Fill The Graph")
        print("3. Randomize The Graph")
        print("4. Exit")
        choice = input(f"\nEnter your choice (1-4): ")

        try:
            if choice == '1':
                params = get_user_params('text')
                params['text'] = input("Enter the text to draw: ")
                if not params['text']: 
                    print(f"\n{style.RED}Text cannot be empty for this mode.{style.RESET}")
                    time.sleep(1.5)
                    continue
                run_ghart('text', params)
            elif choice == '2':
                params = get_user_params('fill')
                run_ghart('fill', params)
            elif choice == '3':
                params = get_user_params('random')
                run_ghart('random', params)
            elif choice == '4':
                print(f"{style.GREEN}Goodbye!{style.RESET}"); break
            else:
                print(f"\n{style.RED}Invalid choice. Please enter a number between 1 and 4.{style.RESET}")
                time.sleep(1)
                continue
            
            input(f"\n{style.BOLD}Press Enter to return to the main menu...{style.RESET}")

        except (KeyboardInterrupt, EOFError):
            print(f"\n{style.RED}Aborted by user.{style.RESET}")
            break # Exit on Ctrl+C

if __name__ == "__main__":
    main()