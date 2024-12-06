from typing import List, Tuple, Dict

def round_robin_tournament_with_referees(num_teams: int, group_name: str) -> Tuple[List[Tuple[str, str, str]], List[Tuple[str, str, str]], List[Tuple[str, str, str]]]:
    """
    Erstelle ein Round-Robin-Turnier mit Schiedsrichtern.

    :param num_teams: Anzahl der Teams in der Gruppe
    :param group_name: Der Name der Gruppe (z. B. "Fun", "Schwitzer")
    :return: Ein Tuple bestehend aus drei Listen:
             - alle Spiele (alle Runden),
             - jedes zweite Spiel (zweite Runde),
             - alle Spiele ohne jedes zweite Spiel
    """
    # Erstelle eine Liste von Teams (1 bis num_teams) mit den Gruppennamen
    teams: List[str] = [f"{group_name} {i + 1}" for i in range(num_teams)]
    # Listen für alle Spiele, jedes zweite Spiel und alle ohne jedes zweite Spiel
    all_matches: List[Tuple[str, str, str]] = []
    second_round_matches: List[Tuple[str, str, str]] = []
    without_second_round_matches: List[Tuple[str, str, str]] = []

    # Jede Runde hat die Spiele für diese Runde
    for round_num in range(num_teams - 1):
        round_matches: List[Tuple[str, str, str]] = []
        available_referees: List[str] = teams.copy()  # Liste der verfügbaren Schiedsrichter

        for i in range(num_teams // 2):
            team1: str = teams[i]
            team2: str = teams[num_teams - 1 - i]

            # Schiedsrichter auswählen, der nicht an diesem Spiel beteiligt ist
            available_referees.remove(team1)
            available_referees.remove(team2)

            # Wenn weniger als 1 Schiedsrichter übrig ist, müssen wir die Liste der Schiedsrichter neu füllen
            if not available_referees:
                available_referees = [team for team in teams if team != team1 and team != team2]

            referee: str = available_referees.pop(0)  # Der erste verfügbare Schiedsrichter wird gewählt

            # Ein Spiel für die Runde hinzufügen, zusammen mit dem Schiedsrichter
            match: Tuple[str, str, str] = (team1, team2, referee)
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


def assign_matches_to_fields(all_matches_group1: List[Tuple[str, str, str]], second_round_matches_group1: List[Tuple[str, str, str]], without_second_round_matches_group1: List[Tuple[str, str, str]],
                             all_matches_group2: List[Tuple[str, str, str]], second_round_matches_group2: List[Tuple[str, str, str]], without_second_round_matches_group2: List[Tuple[str, str, str]],
                             num_fields: int) -> Dict[int, List[Tuple[str, str, str]]]:
    """
    Weist die Spiele den Feldern zu.

    :param all_matches_group1: Alle Spiele der ersten Gruppe
    :param second_round_matches_group1: Alle zweiten Runden der ersten Gruppe
    :param without_second_round_matches_group1: Alle Spiele ohne jedes zweite Spiel der ersten Gruppe
    :param all_matches_group2: Alle Spiele der zweiten Gruppe
    :param second_round_matches_group2: Alle zweiten Runden der zweiten Gruppe
    :param without_second_round_matches_group2: Alle Spiele ohne jedes zweite Spiel der zweiten Gruppe
    :param num_fields: Anzahl der Felder (2 oder 3)
    :return: Ein Dictionary, das jedem Feld eine Liste von Spielen zuweist
    """
    # Basierend auf der Anzahl der Felder werden die Listen den Feldern zugewiesen
    fields: Dict[int, List[Tuple[str, str, str]]] = {1: [], 2: [], 3: []}  # Felder 1, 2, 3

    if num_fields == 2:
        # Feld 1: Alle Spiele Gruppe 1, Feld 2: Alle Spiele Gruppe 2
        fields[1] = all_matches_group1
        fields[2] = all_matches_group2
    elif num_fields == 3:
        # Feld 1: Alle Spiele ohne jedes zweite Spiel aus Gruppe 1
        fields[1] = without_second_round_matches_group1
        # Feld 2: Abwechselnd jedes zweite Spiel von Gruppe 1 und Gruppe 2
        alternating_matches: List[Tuple[str, str, str]] = []
        max_len: int = max(len(second_round_matches_group1), len(second_round_matches_group2))

        for i in range(max_len):
            if i < len(second_round_matches_group1):
                alternating_matches.append(second_round_matches_group1[i])
            if i < len(second_round_matches_group2):
                alternating_matches.append(second_round_matches_group2[i])




        # Überprüfen, ob der Schiedsrichter auf Feld 1 oder 3 gleichzeitig als Spieler aktiv ist
        for match in alternating_matches:
            redo_referee: str = match[2]

            # Überprüfen, ob der Schiedsrichter in Feld 1 oder 3 bereits als Spieler aktiv ist
            all_players_on_fields_1_3: List[str] = [m[0] for m in without_second_round_matches_group1] + [m[1] for m in without_second_round_matches_group1] + [m[2] for m in without_second_round_matches_group1] + \
                                                     [m[0] for m in without_second_round_matches_group2] + [m[1] for m in without_second_round_matches_group2 + [m[2] for m in without_second_round_matches_group2]]

            # Wenn der Schiedsrichter als Spieler auf Feld 1 oder Feld 3 aktiv ist, suche einen neuen Schiedsrichter
            if redo_referee in all_players_on_fields_1_3:
                # Finde einen neuen Schiedsrichter für dieses Match, der nicht als Spieler aktiv ist
                for new_referee in [m[2] for m in without_second_round_matches_group1 + without_second_round_matches_group2]:
                    if new_referee not in all_players_on_fields_1_3:
                        match = (match[0], match[1], new_referee)  # Setze den neuen Schiedsrichter
                        break
            # Spiele auf Feld 2 hinzufügen
            fields[2].append(match)

        #REDO Feld 1
        fields[1] = []
        for match in without_second_round_matches_group1:
            redo_referee_first_field: str = match[2]
            all_players_on_fields_2: List[str] = [m[0] for m in alternating_matches] + [m[1] for m in alternating_matches] + [m[2] for m in alternating_matches]


            if redo_referee_first_field in all_players_on_fields_2:
                for new_referee in [m[2] for m in alternating_matches]:
                    if new_referee not in all_players_on_fields_2:
                        match = (match[0], match[1], new_referee)
                        break
            fields[1].append(match)

        # Feld 3: Alle Spiele ohne jedes zweite Spiel aus Gruppe 2
        fields[3] = without_second_round_matches_group2

        #TODO Prüfe ob Schiedsrichter auf Feld 1 oder 3 gleichzeitig als Spieler auf Feld 2 aktiv ist


    return fields


# Beispiel: Turnier mit 6 Teams für jede Gruppe
num_teams_group1: int = 6
num_teams_group2: int = 6

# Erstelle den Turnierplan für Gruppe 1 (Fun 1-6)
all_matches_group1, second_round_matches_group1, without_second_round_matches_group1 = round_robin_tournament_with_referees(num_teams_group1, "Fun")

# Erstelle den Turnierplan für Gruppe 2 (Schwitzer 7-12)
all_matches_group2, second_round_matches_group2, without_second_round_matches_group2 = round_robin_tournament_with_referees(num_teams_group2, "Schwitzer")

# Benutzer wählt die Anzahl der Felder (2 oder 3)
num_fields: int = int(input("Gib die Anzahl der Felder ein (2 oder 3): "))

# Spiele den Plan den Feldern zuordnen
fields: Dict[int, List[Tuple[str, str, str]]] = assign_matches_to_fields(all_matches_group1, second_round_matches_group1, without_second_round_matches_group1,
                                                                            all_matches_group2, second_round_matches_group2, without_second_round_matches_group2, num_fields)

# Ausgabe der Spiele für jedes Feld
for field, matches in fields.items():
    print(f"\nFeld {field}:")
    for match in matches:
        team1, team2, referee = match
        print(f"{team1} vs {team2} - Schiedsrichter: {referee}")
