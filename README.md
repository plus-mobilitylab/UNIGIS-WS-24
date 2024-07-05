# UNIGIS-WS-24
Material für den UNIGIS-Workshop "Netzwerkanalysen zur Förderung aktiver Mobilität" am 05.07.2024

## Nützliche Links
- Live-Demo Anwendungen des Mobility Labs: https://mobilitylab.zgis.at/demos/
- NetAScore: [Übersicht](https://mobilitylab.zgis.at/netascore-2/) bzw. [Code und Wiki direkt auf GitHub](https://github.com/plus-mobilitylab/netascore): https://github.com/plus-mobilitylab/netascore
- Spatial Betweenness Centrality: [Short Paper](https://doi.org/10.4230/LIPIcs.GIScience.2023.83) sowie [Code, Daten und weitere Beispiele](https://doi.org/10.5281/zenodo.8125632)
- Präsentationsfolien: https://filesender.aco.net/?s=download&token=4c7cd36f-0a0c-4032-ab40-3eeb7e272ae2 

## Voraussetzungen

Die folgenden Voraussetzungen sind nötig, um den Code in diesem Repository ausführen zu können:
- [Visual Studio Code](https://code.visualstudio.com/download) (oder anderer Code-Editor Ihrer Wahl)
- [Conda Paket-Manager](https://docs.anaconda.com/miniconda/)
- ([Python 3.X](https://www.python.org) - wird via Conda verwaltet)

Für NetAScore wird zusätzlich [Docker](https://www.docker.com/products/docker-desktop/) benötigt (oder Python, PostgreSQL, OSGeo cmd utils und weitere - für diese Variante siehe [hier](https://github.com/plus-mobilitylab/netascore/wiki/Run-NetAScore-manually-with-Python)).

## Einrichten der Conda-Umgebung

Als erstes fügen wir den Community-Kanal "conda-forge" zu den Conda-Quellen hinzu:
```
conda config --append channels conda-forge
```

Dann erstellen wir eine neue Conda-Umgebung und installieren die benötigten Pakete:
Im Beispiel verwenden wir dafür den Namen "mobility_ws24". Die zu installierenden Pakete werden aus der Datei "requirements.txt" gelesen.

```
conda create -n mobility_ws24 --file requirements.txt
```

Um mit dieser Umgebung zu arbeiten, müssen wir diese aktivieren:
```
conda activate mobility_ws24
```

Jetzt können wir bei Bedarf noch weitere Pakete zu dieser Umgebung hinzufügen mit dem folgenden Befehl:

```
conda install <package_name>
```

(wobei `<package_name>` durch den Namen des zu installierenden Pakets zu ersetzen ist - Beispiel: `conda install geopandas`)

Weitere Informationen zur Verwendung von Conda gibt es in der Online-Dokumentation: [Conda Documentation](https://docs.conda.io/en/latest/)
