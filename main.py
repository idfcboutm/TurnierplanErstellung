def round_robin_tournament_with_referees(num_teams, group_name):
    # Erstelle eine Liste von Teams (1 bis num_teams) mit den Gruppennamen
    teams = [f"{group_name} {i + 1}" for i in range(num_teams)]

    # Listen für alle Spiele, jedes zweite Spiel und alle ohne jedes zweite Spiel
    all_matches = []
    second_round_matches = []
    without_second_round_matches = []

    # Jede Runde hat die Spiele für diese Runde
    for round_num in range(num_teams - 1):
        round_matches = []
        available_referees = teams.copy()  # Liste der verfügbaren Schiedsrichter

        for i in range(num_teams // 2):
            team1 = teams[i]
            team2 = teams[num_teams - 1 - i]

            # Schiedsrichter auswählen, der nicht an diesem Spiel beteiligt ist
            available_referees.remove(team1)
            available_referees.remove(team2)

            # Wenn weniger als 1 Schiedsrichter übrig ist, müssen wir die Liste der Schiedsrichter neu füllen
            if not available_referees:
                available_referees = [team for team in teams if team != team1 and team != team2]

            referee = available_referees.pop(0)  # Der erste verfügbare Schiedsrichter wird gewählt

            # Ein Spiel für die Runde hinzufügen, zusammen mit dem Schiedsrichter
            match = (team1, team2, referee)
            round_matches.append(match)

            # Jedes zweite Spiel zusätzlich in der zweiten Liste speichern
            if (i + 1) % 2 == 0:
                second_round_matches.append(match)

            # Schiedsrichter zurück in die Liste der verfügbaren Schiedsrichter setzen
            available_referees.append(referee)

        all_matches.extend(round_matches)  # Alle Spiele in die "all_matches" Liste einfügen
        without_second_round_matches.extend([match for i, match in enumerate(round_matches) if (i + 1) % 2 != 0])

        # Teams rotieren (der erste spielt gegen den letzten, der zweite gegen den vorletzten usw.)
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    return all_matches, second_round_matches, without_second_round_matches


def assign_matches_to_fields(all_matches_group1, second_round_matches_group1, without_second_round_matches_group1,
                              all_matches_group2, second_round_matches_group2, without_second_round_matches_group2, num_fields):
    # Basierend auf der Anzahl der Felder werden die Listen den Feldern zugewiesen
    fields = {1: [], 2: [], 3: []}  # Felde 1, 2, 3

    if num_fields == 2:
        # Feld 1: Alle Spiele Gruppe 1, Feld 2: Alle Spiele Gruppe 2
        fields[1] = all_matches_group1
        fields[2] = all_matches_group2
    elif num_fields == 3:
        # Feld 1: Alle Spiele ohne jedes zweite Spiel aus Gruppe 1
        fields[1] = without_second_round_matches_group1
        # Feld 2: Abwechselnd jedes zweite Spiel von Gruppe 1 und Gruppe 2
        alternating_matches = []
        max_len = max(len(second_round_matches_group1), len(second_round_matches_group2))
        for i in range(max_len):
            if i < len(second_round_matches_group1):
                alternating_matches.append(second_round_matches_group1[i])
            if i < len(second_round_matches_group2):
                alternating_matches.append(second_round_matches_group2[i])
        fields[2] = alternating_matches
        # Feld 3: Alle Spiele ohne jedes zweite Spiel aus Gruppe 2
        fields[3] = without_second_round_matches_group2

    return fields


# Beispiel: Turnier mit 6 Teams für jede Gruppe
num_teams_group1 = 6
num_teams_group2 = 6

# Erstelle den Turnierplan für Gruppe 1 (Schwitzer 1-6)
all_matches_group1, second_round_matches_group1, without_second_round_matches_group1 = round_robin_tournament_with_referees(num_teams_group1, "Fun")

# Erstelle den Turnierplan für Gruppe 2 (Schwitzer 7-12)
all_matches_group2, second_round_matches_group2, without_second_round_matches_group2 = round_robin_tournament_with_referees(num_teams_group2, "Schwitzer")

# Benutzer wählt die Anzahl der Felder (2 oder 3)
num_fields = int(input("Gib die Anzahl der Felder ein (2 oder 3): "))

# Spiele den Plan den Feldern zuordnen
fields = assign_matches_to_fields(all_matches_group1, second_round_matches_group1, without_second_round_matches_group1,
                                  all_matches_group2, second_round_matches_group2, without_second_round_matches_group2, num_fields)

# Ausgabe der Spiele für jedes Feld
for field, matches in fields.items():
    print(f"\nFeld {field}:")
    for match in matches:
        team1, team2, referee = match
        print(f"{team1} vs {team2} - Schiedsrichter: {referee}")
