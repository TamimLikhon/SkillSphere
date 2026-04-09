# Database Schema Design

Based on your requirements, here are the proposed tables and constraints for the student-company matching app.

### 1. `student_profiles`

Stores information about students.

- `id` (UUID, Primary Key) - References `auth.users(id)` from Supabase Auth.
- `full_name` (Text)
- `qualifications` (Text) - Details about the student's qualifications.
- `current_company_id` (UUID, Nullable) - References `company_profiles(id)`. This is populated when a student is successfully hired.
- `created_at` (Timestamp)

**Constraints:**

- `id` must be a valid user in `auth.users` (Foreign Key, On Delete Cascade).
- `current_company_id` must be a valid company in `company_profiles` (Foreign Key, On Delete Set Null).

### 2. `company_profiles`

Stores information about companies.

- `id` (UUID, Primary Key) - References `auth.users(id)` from Supabase Auth.
- `company_name` (Text, Not Null)
- `expectations` (Text) - What the company expects (used to match against student qualifications).
- `created_at` (Timestamp)

**Constraints:**

- `id` must be a valid user in `auth.users` (Foreign Key, On Delete Cascade).

### 3. `matches` (or `interactions`)

This is the core table that handles the swiping, matching, history, and hiring pipeline. It supports a student matching with multiple companies simultaneously until they are hired.

- `id` (UUID, Primary Key)
- `student_id` (UUID, Not Null) - References `student_profiles(id)`.
- `company_id` (UUID, Not Null) - References `company_profiles(id)`.
- `student_liked` (Boolean, Default: false) - True if the student swiped left / expressed interest in the company.
- `match_rating` (Numeric, Nullable) - The calculated rating between company expectation and student qualification.
- `is_shortlisted` (Boolean, Default: false) - True if the candidate passes the initial selection / qualifies for the company.
- `interview_date` (Timestamp, Nullable) - The date and time given by the company for an interview.
- `status` (Text Check / Enum) - Current stage of the match (e.g., `'pending'`, `'interview_scheduled'`, `'hired'`, `'rejected'`).
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

**Constraints:**

- **UNIQUE(`student_id`, `company_id`)**: A student and a company can only have one active interaction record. However, one student can have records with many different companies, allowing them to match and interview with multiple companies concurrently.
- Foreign key `student_id` referencing `student_profiles(id)` (On Delete Cascade).
- Foreign key `company_id` referencing `company_profiles(id)` (On Delete Cascade).

## How it fulfills your requirements:

1. **Students see companies and swipe**: `student_liked` is set to `true`.
2. **Match rating**: A calculation is run (or stored) comparing `qualifications` and `expectations`, saved to `match_rating`.
3. **Company shortlist**: Based on the rating, if it matches well, `is_shortlisted` becomes `true` for initial candidates.
4. **Match History**: Querying the `matches` table by `student_id` yields the student's swiped companies. Querying by `company_id` shows the company their matched/shortlisted candidates.
5. **Interview Date**: `interview_date` handles the scheduled interview from the company.
6. **Final Selection**: When a company selects a candidate, `status` updates to `'hired'`, and `student_profiles.current_company_id` is updated so the student profile officially displays their new workplace.
