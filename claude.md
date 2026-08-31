 # AI & Data Engineering — Personal Learning

## Who I am
Former SQL Server DBA, now Snowflake ETL developer at Princess Cruises.
Transitioning into modern Data Engineering and AI tooling.
Python beginner. New to Mac. Building skills daily to get ahead in AI/DE space.
Goal: become a well-rounded Data Engineer who builds and deploys real pipelines
and works confidently with AI tooling.

## My background advantage
- SQL Server DBA roots → strong on relational theory, indexes, query tuning
- Snowflake ETL experience → pipelines, ODS views, reconciliation, migrations
- Cruise industry domain → voyages, reservations, pricing data at scale
- These are STRENGTHS in DE — most Python-first DE people lack this foundation

## My learning goals (in order of priority)
1. Python fluency for data work (pandas, file I/O, APIs)
2. Building real ETL pipelines in Python (not just SQL)
3. Git workflows — branching, PRs, working like a real dev
4. Understanding modern DE stack (dbt, Airflow concepts)
5. Working with APIs and data ingestion patterns
6. AI/ML foundations relevant to DE (the plumbing, not the modeling)
7. Cloud data concepts (Azure focus — matches my AVD/Snowflake ecosystem)
8. Docker basics — containerizing pipelines
9. Spark concepts — large scale processing beyond Snowflake

## My current skill map
| Skill              | Level        | Notes                                      |
|--------------------|--------------|--------------------------------------------|
| SQL Server         | Strong       | DBA background — my original home base     |
| Snowflake SQL      | Strong       | Current work environment                   |
| ETL concepts       | Strong       | Pipeline design, reconciliation, migrations|
| Python             | Beginner     | 3 projects built — venv, pandas, requests  |
| pandas             | Beginner     | read_csv, filter, groupby, merge done      |
| Git                | Beginner     | Committing locally, GitHub push next       |
| Terminal/Mac       | Beginner     | Comfortable with basic commands            |
| VS Code            | Beginner     | Learning as editor                         |
| REST APIs          | Beginner     | Built working API pipeline (Project 02)    |
| dbt                | Heard of it  | Want to learn — relates to my ETL work     |
| Airflow            | Heard of it  | Want to learn — scheduling pipelines       |
| Azure/ADF          | Aware        | Work in Azure ecosystem via AVD            |
| Docker             | Unknown      | Haven't touched yet                        |
| Spark              | Unknown      | Haven't touched yet                        |

## How I learn best
- SQL-first analogies — always map new concepts to SQL equivalents
- Show full picture first, then zoom into detail
- Real examples over theoretical — use data pipeline scenarios
- Explain terminal commands before running them
- Build things I can actually use or show — not toy examples
- One concept at a time — don't overwhelm with 5 new tools at once

## How I want Claude to help
- Be my senior DE mentor, not just a code generator
- When introducing any new tool or concept always answer:
  * What problem does this solve?
  * How does this relate to what I already do in Snowflake/SQL Server?
  * What's the simplest version I can build today?
- Push back if I'm overcomplicating things
- Suggest what to learn NEXT based on what we just built
- Flag when something is "good enough to ship" vs needs more work
- Remind me my SQL background is valuable — don't let me underestimate it

## My dev environment
- Machine: Mac (personal learning sandbox)
- Work: AVD (Azure Virtual Desktop) — separate, corporate Snowflake
- Editor: VS Code
- Shell: zsh
- Python: learning via Claude Code projects
- Git: just set up, building habits
- Claude Code: installed, projects in ~/learning/DataEngineering_AI

## Project patterns I want to build (in order)
1. ✅ CSV/JSON → Python → local output (first real pipeline)
2. ⏭ CSV/JSON → Python → Snowflake loader (skipped — no trial account yet)
3. ✅ REST API → pull data → store locally → analyze with pandas
4. ✅ Data quality checker (reusable reconciliation tool — I know this problem well)
5. Simple pipeline scheduler (understand what Airflow solves before using it)
6. dbt project on free Snowflake trial account
7. AI API integration (call Claude/OpenAI API, process results, store output)
8. End-to-end portfolio project combining all of the above

## Code style preferences
- Beginner-friendly but not dumbed down
- Comments on every non-obvious line
- Small functions, one job each (explain why this matters)
- requirements.txt for every project (teach me dependency management)
- README.md in every project folder (build the habit early)
- Use f-strings for string formatting
- Explicit over clever — readability always wins at my stage
- .gitignore in every project — never commit secrets or venv folders

## Python ↔ SQL cheat sheet (update as I learn)
| Python / pandas          | SQL equivalent                      |
|--------------------------|-------------------------------------|
| pd.read_csv()            | COPY INTO / external stage          |
| df.head()                | SELECT * ... LIMIT 10               |
| df.groupby().agg()       | GROUP BY with aggregates            |
| df.merge()               | JOIN                                |
| df[df['col'] > x]        | WHERE col > x                       |
| df.fillna()              | COALESCE()                          |
| df.drop_duplicates()     | DISTINCT                            |
| df.sort_values()         | ORDER BY                            |
| df.rename(columns={})    | column aliases in SELECT            |
| for loop over df rows    | row-by-row cursor (avoid in SQL!)   |
| try / except             | error handling (no SQL equivalent)  |
| def my_function()        | stored procedure (but more flexible)|

## Recurring task triggers
- "start a new project" → scaffold folder + CLAUDE.md + requirements.txt + README.md + .gitignore
- "explain this tool" → what it is, SQL analogy, when to use it, simplest example
- "build a pipeline" → CSV/API source → transform with pandas → output to file or Snowflake
- "review my code" → correctness, readability, error handling, beginner pitfalls
- "what should I learn next" → suggest logical next skill based on current project
- "make this production ready" → add error handling, logging, config file, README
- "show me the SQL way first" → explain concept in SQL then translate to Python

## DE concepts backlog (work through in order)
- [x] Python virtual environments (venv) — isolating project dependencies
- [x] REST APIs — GET/POST, requests library, JSON parsing (Project 02)
- [x] Push projects to GitHub — set up remote repo (done 2026-06-03)
- [ ] Git branching basics — working safely on features
- [ ] pandas deep dive — groupby, merge, reshape
- [ ] File formats — CSV vs JSON vs Parquet (why Parquet matters in DE)
- [ ] PySpark basics — DataFrame API, transformations, actions (HIGH PRIORITY — job market demand)
- [ ] PySpark SQL — running SQL queries on Spark DataFrames
- [ ] PySpark ETL pipeline — read large file, transform, write Parquet output
- [ ] Schema drift handling — detecting and managing schema changes in pipelines
- [ ] Kafka concepts — what it is, why DE uses it, basic producer/consumer
- [ ] dbt fundamentals — models, tests, sources
- [ ] Airflow concepts — DAGs, tasks, scheduling
- [ ] Azure Data Factory — bridges my AVD work with DE concepts
- [ ] Docker basics — what it is and why DE uses it (needed for Spark local setup)
- [ ] LLM APIs — calling Claude/OpenAI, parsing responses
- [ ] Vector databases — what they are, why AI apps need them
- [ ] Data lakehouse concepts — Delta Lake, Iceberg
- [ ] HackerRank / StrataScratch — SQL + Python coding challenge practice (interview prep)

## Mindset reminders (for Claude to reinforce)
- Progress over perfection — ship the simple version first
- Every script I write is portfolio material — treat it that way
- The terminal is not scary — it's just a faster way to do things
- SQL Server DBA + Snowflake ETL is a rare combo — most DE people lack it
- SQL skills are a superpower in the AI/DE world — don't underestimate them
- Consistency beats intensity — 30 min daily beats 5 hours on weekends
- I am not starting from zero — I am adding to a strong foundation