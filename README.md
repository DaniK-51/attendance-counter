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

Results are printed to console and saved to two files (derived from attendance file name):

- `<name>_stats.txt` — per-team attendance count and percentage
- `<name>_details.txt` — absent students, unknown students, corrupted emails

## Files

- `Participants_by_teams.csv` — master roster (20 teams, emails per column)
- `check_attendance.py` — attendance checker script
