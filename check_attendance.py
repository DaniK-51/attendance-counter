import csv
import sys
from pathlib import Path

RATING_DIR = Path(__file__).parent
TEAMS_CSV = RATING_DIR / "Participants_by_teams.csv"


def load_teams(csv_path: Path) -> dict[str, list[str]]:
    """Returns {team_name: [email, ...]} from the CSV."""
    teams: dict[str, list[str]] = {}
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        team_names = [h.strip() for h in header]
        for team in team_names:
            teams[team] = []
        for row in reader:
            for i, email in enumerate(row):
                if i < len(team_names) and email.strip():
                    teams[team_names[i]].append(email.strip().lower())
    return teams


def load_attendance(txt_path: Path) -> tuple[set[str], list[str]]:
    """Returns (valid_emails, corrupted_lines) from the attendance file."""
    emails = set()
    corrupted: list[str] = []
    for line in txt_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.count("@") != 1 or "," in line or " " in line:
            corrupted.append(line)
        else:
            emails.add(line.lower())
    return emails, corrupted


def check_attendance(teams_csv: Path, attendance_txt: Path) -> None:
    teams = load_teams(teams_csv)
    attended, corrupted = load_attendance(attendance_txt)

    # Build email -> team lookup
    email_to_team: dict[str, str] = {}
    for team, members in teams.items():
        for email in members:
            email_to_team[email] = team

    all_members = set(email_to_team.keys())

    def team_sort_key(team_name: str) -> int:
        digits = "".join(c for c in team_name if c.isdigit())
        return int(digits) if digits else 0

    # ── Per-team stats ──
    print("=" * 60)
    print("PER-TEAM ATTENDANCE")
    print("=" * 60)
    total_present = 0
    total_members = 0
    for team, members in sorted(teams.items(), key=lambda kv: team_sort_key(kv[0])):
        if not members:
            continue
        present = [m for m in members if m in attended]
        count = len(present)
        pct = count / len(members) * 100 if members else 0
        total_present += count
        total_members += len(members)
        print(f"{team:12s}  {count:3d}/{len(members):3d}  ({pct:5.1f}%)")
    overall_pct = total_present / total_members * 100 if total_members else 0
    print("-" * 60)
    print(f"{'TOTAL':12s}  {total_present:3d}/{total_members:3d}  ({overall_pct:5.1f}%)")

    # ── Absent students (sorted by team number, then email) ──
    absent = sorted(all_members - attended, key=lambda e: (team_sort_key(email_to_team[e]), e))
    print(f"\n{'=' * 60}")
    print(f"ABSENT STUDENTS ({len(absent)})")
    print("=" * 60)
    current_team = None
    for email in absent:
        team = email_to_team[email]
        if team != current_team:
            if current_team is not None:
                print()
            current_team = team
        print(f"  {email:45s}  {team}")

    # ── Unknown students (in attendance but not in any team) ──
    unknown = sorted(attended - all_members)
    print(f"\n{'=' * 60}")
    print(f"UNKNOWN STUDENTS — in attendance but NOT in teams ({len(unknown)})")
    print("=" * 60)
    for email in unknown:
        print(f"  {email}")

    # ── Corrupted / unparseable emails ──
    if corrupted:
        print(f"\n{'=' * 60}")
        print(f"CORRUPTED EMAILS ({len(corrupted)})")
        print("=" * 60)
        for line in corrupted:
            print(f"  {line}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 check_attendance.py <attendance_file.txt>")
        sys.exit(1)
    attendance_file = Path(sys.argv[1])
    if not attendance_file.exists():
        print(f"File not found: {attendance_file}")
        sys.exit(1)
    check_attendance(TEAMS_CSV, attendance_file)
