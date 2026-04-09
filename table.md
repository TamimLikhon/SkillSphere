Database Schema and Constraints

This document outlines the structure of the database tables used for the student-company matching application. It details the Primary Keys (PK), Foreign Keys (FK), and specific constraints for each table.

1. student_profiles
   Stores information about students seeking employment.

Column Name: id

- Data Type: UUID
- Key: PK
- Constraints / Description: References auth.users(id) from Supabase Auth. On Delete Cascade.

Column Name: full_name

- Data Type: Text
- Constraints / Description: Not Null

Column Name: qualifications

- Data Type: Text
- Constraints / Description: Details about the student's background and skills.

Column Name: current_company_id

- Data Type: UUID
- Key: FK
- Constraints / Description: References company_profiles(id). Populated when hired. On Delete Set Null.

Column Name: created_at

- Data Type: Timestamp
- Constraints / Description: Default is now()

2. company_profiles
   Stores information about companies hiring students.

Column Name: id

- Data Type: UUID
- Key: PK
- Constraints / Description: References auth.users(id) from Supabase Auth. On Delete Cascade.

Column Name: company_name

- Data Type: Text
- Constraints / Description: Not Null

Column Name: expectations

- Data Type: Text
- Constraints / Description: What the company requires from candidates.

Column Name: created_at

- Data Type: Timestamp
- Constraints / Description: Default is now()

3. matches (Interactions)
   The core table orchestrating interactions, swiping, evaluations, and hiring history. A single student can match with multiple companies concurrently.

Column Name: id

- Data Type: UUID
- Key: PK
- Constraints / Description: Default is gen_random_uuid()

Column Name: student_id

- Data Type: UUID
- Key: FK
- Constraints / Description: References student_profiles(id). On Delete Cascade.

Column Name: company_id

- Data Type: UUID
- Key: FK
- Constraints / Description: References company_profiles(id). On Delete Cascade.

Column Name: student_liked

- Data Type: Boolean
- Constraints / Description: Default is false. True if student swiped left/expressed interest.

Column Name: match_rating

- Data Type: Numeric
- Constraints / Description: Nullable. Calculated compatibility score.

Column Name: is_shortlisted

- Data Type: Boolean
- Constraints / Description: Default is false. True if candidate passes initial selection.

Column Name: interview_date

- Data Type: Timestamp
- Constraints / Description: Nullable. Date given by company for an interview.

Column Name: status

- Data Type: Text
- Constraints / Description: Default is 'pending'. Check constraint: Must be one of ('pending', 'interview_scheduled', 'hired', 'rejected').

Column Name: created_at

- Data Type: Timestamp
- Constraints / Description: Default is now()

Column Name: updated_at

- Data Type: Timestamp
- Constraints / Description: Default is now(). Automatically updated by a trigger before every update.

Table Constraints for matches

- UNIQUE(student_id, company_id): A student and a company can only have one active interaction record forming their complete history. However, one student can have multiple records with different companies.
