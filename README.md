# IBC 2026 Attendance Checker

Checks lecture attendance against the team roster.

## Usage

```bash
python3 check_attendance.py <attendance_file.txt>
```

The attendance file name is required. Example:

```bash
python3 check_attendance.py "IU Day 1-attendance.txt"
```

## Output

- **Per-team attendance** — count and percentage
- **Absent students** — sorted by team (email + team)
- **Unknown students** — in attendance but not in any team
- **Corrupted emails** — malformed lines from the attendance file

## Files

- `Participants_by_teams.csv` — master roster (20 teams, emails per column)
- `check_attendance.py` — attendance checker script
