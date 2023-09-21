# ibis-birdbrain

An AI assistant for your data project, powered by [Ibis](https://ibis-project.org/) and Marvin(https://github.com/prefectHQ/marvin).

## demo

```python
(venv) user@machine ibis-birdbrain % python example_data.py
(venv) user@machine ibis-birdbrain % birdbrain ai -i
birdbrain:
access to: birdbrain
state: {'config': {}}
Python 3.11.5 (main, Sep 14 2023, 13:17:51) [Clang 14.0.3 (clang-1403.0.22.14.1)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.15.0 -- An enhanced Interactive Python. Type '?' for help.

[ins] In [1]: bot("what tables do you have access to?")
birdbrain:

I have access to the following tables:

1. imdb_name_basics
2. imdb_title_akas
3. imdb_title_basics
4. imdb_title_crew
5. imdb_title_episode
6. imdb_title_principals
7. imdb_title_ratings

[ins] In [2]: bot("what's in the name basics table?")
birdbrain:

The `imdb_name_basics` table contains the following information:

- `nconst`: A unique identifier for a name/person.
- `primaryName`: The name of the person.
- `birthYear`: The birth year of the person.
- `deathYear`: The death year of the person.
- `primaryProfession`: The primary professions of the person.
- `knownForTitles`: Known titles that the person has been associated with.

[ins] In [3]: bot("what are some sample rows?")
birdbrain:

Here are some sample rows from the `imdb_name_basics` table:

1. Fred Astaire:
   - `nconst`: nm0000001
   - `birthYear`: 1899
   - `deathYear`: 1987
   - `primaryProfession`: soundtrack, actor, miscellaneous
   - `knownForTitles`: tt0053137, tt0072308, tt0045537, tt0050419

2. Lauren Bacall:
   - `nconst`: nm0000002
   - `birthYear`: 1924
   - `deathYear`: 2014
   - `primaryProfession`: actress, soundtrack
   - `knownForTitles`: tt0037382, tt0117057, tt0075213, tt0038355

3. Brigitte Bardot:
   - `nconst`: nm0000003
   - `birthYear`: 1934
   - `deathYear`: N/A
   - `primaryProfession`: actress, soundtrack, music_department
   - `knownForTitles`: tt0057345, tt0054452, tt0049189, tt0056404

4. John Belushi:
   - `nconst`: nm0000004
   - `birthYear`: 1949
   - `deathYear`: 1982
   - `primaryProfession`: actor, soundtrack, writer
   - `knownForTitles`: tt0072562, tt0078723, tt0077975, tt0080455

5. Ingmar Bergman:
   - `nconst`: nm0000005
   - `birthYear`: 1918
   - `deathYear`: 2007
   - `primaryProfession`: writer, director, actor
   - `knownForTitles`: tt0083922, tt0069467, tt0050976, tt0050986

[ins] In [4]: bot("find the rows for Tom Cruise")
birdbrain:

Tom Cruise's details in the `imdb_name_basics` table are as follows:

- `nconst`: nm0000129
- `primaryName`: Tom Cruise
- `birthYear`: 1962
- `deathYear`: N/A
- `primaryProfession`: Actor, Producer, Soundtrack
- `knownForTitles`: tt0120755, tt0325710, tt0116695, tt0092099

[ins] In [5]: bot("search for those known titles as the tconst in the titles table and give some examples")
birdbrain:

Here are some known titles for Tom Cruise:

1. "Top Gun" (tt0092099) - An action, drama movie released in 1986 with a runtime of 109 minutes.

2. "Jerry Maguire" (tt0116695) - A comedy, drama, romance movie released in 1996 with a runtime of 139 minutes.

3. "Mission: Impossible II" (tt0120755) - An action, adventure, thriller movie released in 2000 with a runtime of 123 minutes.

4. "The Last Samurai" (tt0325710) - An action, drama movie released in 2003 with a runtime of 154 minutes.

[ins] In [6]: print(bot.ai.history)
History(
    messages=[
        Message(
            role=<Role.USER: 'USER'>,
            content='what tables do you have access to?',
            name=None,
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 7, 275172, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={}
        ),
        Message(
            role=<Role.FUNCTION_RESPONSE: 'FUNCTION_RESPONSE'>,
            content="['imdb_name_basics', 'imdb_title_akas', 'imdb_title_basics', 'imdb_title_crew', 'imdb_title_episode', 'imdb_title_principals',
'imdb_title_ratings']",
            name='list_tables',
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 9, 65361, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={
                'name': 'list_tables',
                'arguments': {},
                'is_error': False,
                'result': [
                    'imdb_name_basics',
                    'imdb_title_akas',
                    'imdb_title_basics',
                    'imdb_title_crew',
                    'imdb_title_episode',
                    'imdb_title_principals',
                    'imdb_title_ratings'
                ]
            }
        ),
        Message(
            role=<Role.ASSISTANT: 'ASSISTANT'>,
            content='I have access to the following tables:\n\n1. imdb_name_basics\n2. imdb_title_akas\n3. imdb_title_basics\n4. imdb_title_crew\n5.
imdb_title_episode\n6. imdb_title_principals\n7. imdb_title_ratings',
            name=None,
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 11, 929576, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={}
        ),
        Message(
            role=<Role.USER: 'USER'>,
            content="what's in the name basics table?",
            name=None,
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 14, 895413, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={}
        ),
        Message(
            role=<Role.FUNCTION_RESPONSE: 'FUNCTION_RESPONSE'>,
            content='ibis.Schema {\n  nconst             string\n  primaryName        string\n  birthYear          int64\n  deathYear          int64\n
primaryProfession  string\n  knownForTitles     string\n}',
            name='get_table_schema',
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 16, 623592, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={
                'name': 'get_table_schema',
                'arguments': {'table_name': 'imdb_name_basics'},
                'is_error': False,
                'result': 'ibis.Schema {\n  nconst             string\n  primaryName        string\n  birthYear          int64\n  deathYear          int64\n
primaryProfession  string\n  knownForTitles     string\n}'
            }
        ),
        Message(
            role=<Role.ASSISTANT: 'ASSISTANT'>,
            content='The `imdb_name_basics` table contains the following information:\n\n- `nconst`: A unique identifier for a name/person.\n-
`primaryName`: The name of the person.\n- `birthYear`: The birth year of the person.\n- `deathYear`: The death year of the person.\n- `primaryProfession`:
The primary professions of the person.\n- `knownForTitles`: Known titles that the person has been associated with.',
            name=None,
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 20, 224294, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={}
        ),
        Message(
            role=<Role.USER: 'USER'>,
            content='what are some sample rows?',
            name=None,
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 27, 586922, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={}
        ),
        Message(
            role=<Role.FUNCTION_RESPONSE: 'FUNCTION_RESPONSE'>,
            content='┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━┓\n┃ nconst    ┃ primaryName     ┃ birthYear ┃ deathYear ┃ primaryProfession                       ┃ knownForTitles
┃\n┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ string
│ string          │ int64     │ int64     │ string                                  │ string
│\n├───────────┼─────────────────┼───────────┼───────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤\n│ nm0000001
│ Fred Astaire    │      1899 │      1987 │ soundtrack,actor,miscellaneous          │ tt0053137,tt0072308,tt0045537,tt0050419 │\n│ nm0000002 │ Lauren Bacall
│      1924 │      2014 │ actress,soundtrack                      │ tt0037382,tt0117057,tt0075213,tt0038355 │\n│ nm0000003 │ Brigitte Bardot │      1934 │
NULL │ actress,soundtrack,music_department     │ tt0057345,tt0054452,tt0049189,tt0056404 │\n│ nm0000004 │ John Belushi    │      1949 │      1982 │
actor,soundtrack,writer                 │ tt0072562,tt0078723,tt0077975,tt0080455 │\n│ nm0000005 │ Ingmar Bergman  │      1918 │      2007 │
writer,director,actor                   │ tt0083922,tt0069467,tt0050976,tt0050986
│\n└───────────┴─────────────────┴───────────┴───────────┴─────────────────────────────────────────┴─────────────────────────────────────────┘',
            name='query_table',
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 31, 714652, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={
                'name': 'query_table',
                'arguments': {'question': 'What are some sample rows from the imdb_name_basics table?'},
                'is_error': False,
                'result':
'┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ nconst    ┃
primaryName     ┃ birthYear ┃ deathYear ┃ primaryProfession                       ┃ knownForTitles
┃\n┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ string
│ string          │ int64     │ int64     │ string                                  │ string
│\n├───────────┼─────────────────┼───────────┼───────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤\n│ nm0000001
│ Fred Astaire    │      1899 │      1987 │ soundtrack,actor,miscellaneous          │ tt0053137,tt0072308,tt0045537,tt0050419 │\n│ nm0000002 │ Lauren Bacall
│      1924 │      2014 │ actress,soundtrack                      │ tt0037382,tt0117057,tt0075213,tt0038355 │\n│ nm0000003 │ Brigitte Bardot │      1934 │
NULL │ actress,soundtrack,music_department     │ tt0057345,tt0054452,tt0049189,tt0056404 │\n│ nm0000004 │ John Belushi    │      1949 │      1982 │
actor,soundtrack,writer                 │ tt0072562,tt0078723,tt0077975,tt0080455 │\n│ nm0000005 │ Ingmar Bergman  │      1918 │      2007 │
writer,director,actor                   │ tt0083922,tt0069467,tt0050976,tt0050986
│\n└───────────┴─────────────────┴───────────┴───────────┴─────────────────────────────────────────┴─────────────────────────────────────────┘\n'
            }
        ),
        Message(
            role=<Role.ASSISTANT: 'ASSISTANT'>,
            content='Here are some sample rows from the `imdb_name_basics` table:\n\n1. Fred Astaire:\n   - `nconst`: nm0000001\n   - `birthYear`: 1899\n
- `deathYear`: 1987\n   - `primaryProfession`: soundtrack, actor, miscellaneous\n   - `knownForTitles`: tt0053137, tt0072308, tt0045537, tt0050419\n\n2.
Lauren Bacall:\n   - `nconst`: nm0000002\n   - `birthYear`: 1924\n   - `deathYear`: 2014\n   - `primaryProfession`: actress, soundtrack\n   -
`knownForTitles`: tt0037382, tt0117057, tt0075213, tt0038355\n\n3. Brigitte Bardot:\n   - `nconst`: nm0000003\n   - `birthYear`: 1934\n   - `deathYear`:
N/A\n   - `primaryProfession`: actress, soundtrack, music_department\n   - `knownForTitles`: tt0057345, tt0054452, tt0049189, tt0056404\n\n4. John
Belushi:\n   - `nconst`: nm0000004\n   - `birthYear`: 1949\n   - `deathYear`: 1982\n   - `primaryProfession`: actor, soundtrack, writer\n   -
`knownForTitles`: tt0072562, tt0078723, tt0077975, tt0080455\n\n5. Ingmar Bergman:\n   - `nconst`: nm0000005\n   - `birthYear`: 1918\n   - `deathYear`:
2007\n   - `primaryProfession`: writer, director, actor\n   - `knownForTitles`: tt0083922, tt0069467, tt0050976, tt0050986',
            name=None,
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 46, 119148, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={}
        ),
        Message(
            role=<Role.USER: 'USER'>,
            content='find the rows for Tom Cruise',
            name=None,
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 52, 897376, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={}
        ),
        Message(
            role=<Role.FUNCTION_RESPONSE: 'FUNCTION_RESPONSE'>,
            content='┏━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
\n┃ nconst    ┃ primaryName ┃ birthYear ┃ deathYear ┃ primaryProfession                       ┃ knownForTitles
┃\n┡━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ string    │
string      │ int64     │ int64     │ string                                  │ string
│\n├───────────┼─────────────┼───────────┼───────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤\n│ nm0000129 │
Tom Cruise  │      1962 │      NULL │ actor,producer,soundtrack               │ tt0120755,tt0325710,tt0116695,tt0092099
│\n└───────────┴─────────────┴───────────┴───────────┴─────────────────────────────────────────┴─────────────────────────────────────────┘',
            name='query_table',
            timestamp=datetime.datetime(2023, 9, 21, 23, 13, 57, 545612, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={
                'name': 'query_table',
                'arguments': {'question': 'Find the rows for Tom Cruise in the imdb_name_basics table'},
                'is_error': False,
                'result':
'┏━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ nconst    ┃
primaryName ┃ birthYear ┃ deathYear ┃ primaryProfession                       ┃ knownForTitles
┃\n┡━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ string    │
string      │ int64     │ int64     │ string                                  │ string
│\n├───────────┼─────────────┼───────────┼───────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤\n│ nm0000129 │
Tom Cruise  │      1962 │      NULL │ actor,producer,soundtrack               │ tt0120755,tt0325710,tt0116695,tt0092099
│\n└───────────┴─────────────┴───────────┴───────────┴─────────────────────────────────────────┴─────────────────────────────────────────┘\n'
            }
        ),
        Message(
            role=<Role.ASSISTANT: 'ASSISTANT'>,
            content="Tom Cruise's details in the `imdb_name_basics` table are as follows:\n\n- `nconst`: nm0000129\n- `primaryName`: Tom Cruise\n-
`birthYear`: 1962\n- `deathYear`: N/A\n- `primaryProfession`: Actor, Producer, Soundtrack\n- `knownForTitles`: tt0120755, tt0325710, tt0116695, tt0092099",
            name=None,
            timestamp=datetime.datetime(2023, 9, 21, 23, 14, 2, 209072, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={}
        ),
        Message(
            role=<Role.USER: 'USER'>,
            content='search for those known titles as the tconst in the titles table and give some examples',
            name=None,
            timestamp=datetime.datetime(2023, 9, 21, 23, 14, 45, 404627, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={}
        ),
        Message(
            role=<Role.FUNCTION_RESPONSE: 'FUNCTION_RESPONSE'>,
            content='┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━
━━━━━━━━━━━━━━━━━━━━┓\n┃ tconst    ┃ titleType ┃ primaryTitle              ┃ originalTitle            ┃ isAdult ┃ startYear ┃ endYear ┃ runtimeMinutes ┃
genres
┃\n┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━
━━┩\n│ string    │ string    │ string                    │ string                   │ int64   │ int64     │ string  │ int64          │ string
│\n├───────────┼───────────┼───────────────────────────┼──────────────────────────┼─────────┼───────────┼─────────┼────────────────┼────────────────────────
──┤\n│ tt0092099 │ movie     │ Top Gun                   │ Top Gun                  │       0 │      1986 │ NULL    │            109 │ Action,Drama
│\n│ tt0116695 │ movie     │ Jerry Maguire             │ Jerry Maguire            │       0 │      1996 │ NULL    │            139 │ Comedy,Drama,Romance
│\n│ tt0120755 │ movie     │ Mission: Impossible II    │ Mission: Impossible II   │       0 │      2000 │ NULL    │            123 │
Action,Adventure,Thrill… │\n│ tt0325710 │ movie     │ The Last Samurai          │ The Last Samurai         │       0 │      2003 │ NULL    │            154
│ Action,Drama
│\n└───────────┴───────────┴───────────────────────────┴──────────────────────────┴─────────┴───────────┴─────────┴────────────────┴────────────────────────
──┘',
            name='query_table',
            timestamp=datetime.datetime(2023, 9, 21, 23, 14, 51, 256616, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={
                'name': 'query_table',
                'arguments': {
                    'question': 'What are the details for the titles tt0120755, tt0325710, tt0116695, tt0092099 in the imdb_title_basics table?'
                },
                'is_error': False,
                'result':
'┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━
┓\n┃ tconst    ┃ titleType ┃ primaryTitle              ┃ originalTitle            ┃ isAdult ┃ startYear ┃ endYear ┃ runtimeMinutes ┃ genres
┃\n┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━
━━┩\n│ string    │ string    │ string                    │ string                   │ int64   │ int64     │ string  │ int64          │ string
│\n├───────────┼───────────┼───────────────────────────┼──────────────────────────┼─────────┼───────────┼─────────┼────────────────┼────────────────────────
──┤\n│ tt0092099 │ movie     │ Top Gun                   │ Top Gun                  │       0 │      1986 │ NULL    │            109 │ Action,Drama
│\n│ tt0116695 │ movie     │ Jerry Maguire             │ Jerry Maguire            │       0 │      1996 │ NULL    │            139 │ Comedy,Drama,Romance
│\n│ tt0120755 │ movie     │ Mission: Impossible II    │ Mission: Impossible II   │       0 │      2000 │ NULL    │            123 │
Action,Adventure,Thrill… │\n│ tt0325710 │ movie     │ The Last Samurai          │ The Last Samurai         │       0 │      2003 │ NULL    │            154
│ Action,Drama
│\n└───────────┴───────────┴───────────────────────────┴──────────────────────────┴─────────┴───────────┴─────────┴────────────────┴────────────────────────
──┘\n'
            }
        ),
        Message(
            role=<Role.ASSISTANT: 'ASSISTANT'>,
            content='Here are some known titles for Tom Cruise:\n\n1. "Top Gun" (tt0092099) - An action, drama movie released in 1986 with a runtime of 109
minutes.\n\n2. "Jerry Maguire" (tt0116695) - A comedy, drama, romance movie released in 1996 with a runtime of 139 minutes.\n\n3. "Mission: Impossible II"
(tt0120755) - An action, adventure, thriller movie released in 2000 with a runtime of 123 minutes.\n\n4. "The Last Samurai" (tt0325710) - An action, drama
movie released in 2003 with a runtime of 154 minutes.',
            name=None,
            timestamp=datetime.datetime(2023, 9, 21, 23, 15, 0, 472982, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            data={}
        )
    ],
    max_messages=None
)
```

## ...

coming soon!
