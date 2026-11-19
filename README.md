# hire-agent

## Database setup

1. Run the `db_Tech.sql` script provided with the assignment. It creates the `Tech` database and the `Schedule` table, seeded with interview slots for **2024**.
2. After running the script, update the year of all the dates to **2026**, so the bot has current dates to offer:

   ```sql
   USE Tech;
   UPDATE Schedule SET date = DATEADD(YEAR, 2, date) WHERE YEAR(date) = 2024;
   ```

   Only the year changes. The availability of every slot (`available`), the times and the positions stay exactly as they were in the original script.
