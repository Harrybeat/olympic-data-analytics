# Entity-Relationship-Diagramm (ERD)

Dieses Diagramm beschreibt die relationale Datenbankstruktur des `olympic-data-analytics`-Projekts.

![ERD Diagramm](images/erd_diagram.png)

## Tabellenstruktur & Beziehungen
- **athletes**: Stammdaten der Athleten (`athlete_id`, `name`, `sex`)
- **events**: Wettkampf- und Sportart-Informationen (`event_id`, `sport`, `event`)
- **countries**: Zuordnung der NOC-Ländercodes (`noc`, `country`)
- **athlete_event**: Verknüpfungstabelle für Teilnahmen inklusive dynamischer Attribute (`age`, `height`, `weight`, `medal`)
