# Drug Discovery Data Pipeline
## Objectif
L'objectif de ce projet est de créer un **pipeline de traitement des données** qui analyse des publications scientifiques (PubMed) et des essais cliniques (Clinical Trials) pour identifier les mentions de médicaments dans les titres. Le résultat **final** est un fichier JSON représentant un graphe de liaison entre les médicaments et leurs mentions dans les journaux associés aux publications.

En plus, deux fonctions sont fournies pour :

1. Trouver le journal qui mentionne le plus de médicaments différents.
2. Identifier les médicaments mentionnés par les mêmes journaux pour un médicament donné (dans PubMed mais pas dans Clinical Trials).

## Structure du projet

```
drug_discovery/  
├── src/
│   ├── pipeline/
│   │   ├── CustomPipelineOptions.py     # Classe pour gérer les options de la pipeline.
│   │   ├── main.py                      # Point d'entrée principal pour exécuter la pipeline.
│   │   ├── MentionsExtractor.py         # DoFn pour extraire les mentions de médicaments.
│   │   ├── combiner_fn.py               # Fonctions personnalisées pour combiner les résultats.
│   ├── utils/
│   │   └── utils.py                     # Fonctions utilitaires pour le traitement.
│   └── functions/
│       └── functions.py                 # Contient les fonctions bonus décrites ci-dessus.
├── data/
│   ├── drugs.csv                        # Données des médicaments.
│   ├── clinical_trials.csv              # Publications scientifiques sur les essais cliniques.
│   ├── pubmed.csv                       # Publications PubMed (format CSV).
│   └── pubmed.json                      # Publications PubMed (format JSON).
├── output/                              # Contiendra les fichiers générés par la pipeline.
├── tests/
│   ├── unit_tests/
│   │   ├── pipeline_unit_test.py        # Tests unitaires pour les étapes de la pipeline.
│   │   └── utils_test.py                # Tests unitaires pour les fonctions utilitaires.
│   └── e2e_tests/
│       └── pipeline_e2e_test.py         # Tests bout-en-bout de la pipeline.
├── README.md                            # Documentation du projet (ce fichier).
└── requirements.txt                     # Liste des dépendances nécessaires au projet.
```
## Hypothèses
Pour la rélisation de ce pipeline nous supposons que :
* le traitement des données sera fait en batch
* nous recevons fichier par type de données (*`drugs.csv`*, *`clinical_trials.csv`*, *`pubmed.csv`*)
* les données dans les fichiers en input sont pré-processé et nettoyer ...
## Étapes de la pipeline
1. **Lecture des données**
Lecture des fichiers `drugs.csv`, `clinical_trials.csv`, `pubmed.csv` pour créer un ensemble de données consolidé.
le chemin du dossier contenant ces fichier doit être fourni par l'utilisateur via le parametre *`data_folder_path`*.

1. **Extraction des mentions**
Identification des mentions de médicaments dans les titres des publications en utilisant les règles de gestion:
* Un médicament est mentionné si son nom apparaît dans le titre.
* La mention est associée au journal de la publication.
  
1. **Création du graphe**
Génération d'un graphe JSON représentant :
* Les médicaments.
* Les journaux dans lesquels ils sont mentionnés.
1. **Écriture des résultats**
Sauvegarde du graphe dans un fichier JSON sous le répertoire fourni par l'utilisateur via le parametre  *`output_folder_path`*.

1. **Fonctions Bonus**
Deux fonctions sont définies pour des analyses ad-hoc :

* Extraction du journal mentionnant le plus de médicaments différents.
* Identification des médicaments mentionnés par des journaux spécifiques à PubMed.

## Installation
### Prérequis
* Python 3.8+
* Apache Beam
```
pip install -r requirements.txt
```
## Exécution
#### Exécuter la pipeline
Le fichier `main.py` est le point d'entrée de la pipeline. Vous pouvez le lancer comme suit :
```
-m src.pipeline.main --data_folder_path  "/data" --output_folder_path "output"
```
Après génération du fichier `output.json` vous pouvez lancer les deux fonctions suivantes:
#### Fonctions Bonus
###### Journal mentionnant le plus de médicaments
Exécuter cette fonction pour obtenir le journal mentionnant le plus de médicaments différents :
La fonction accepte comme paramètre :
* le chemin du dossier contenant le fichier *`output.json`* 
```
python3 -m src.functions.journal_with_most_drugs -i "output/output.json"
```
###### Médicaments mentionnés par les mêmes journaux
Trouver les médicaments mentionnés par les mêmes journaux pour un médicament donné :
La fonction accepte comme paramètre :
* le chemin du dossier contenant le fichier *`output.json`* 
* nom du médicament 
```
python3 -m src.functions.journal_with_most_drugs -i "output/output.json" -d "TETRACYCLINE"
```
## Tests
#### Unit Tests
Pour lancer les tests unitaires vérifient les différentes fonctions et modules de la pipeline :
```
python3 -m test.unit_tests.pipeline_unit_test
```
#### End-to-End Tests
Pour valider l'intégration complète de la pipeline :
```
python3 -m test.e2e_tests.pipeline_e2e_test
```

## Choix Techniques
pour l'ingestion des données nous avons opté pour apache 
#### 1. Modularité

* Séparation claire des responsabilités : pipeline, utilitaires, et fonctions bonus.
* Chaque composant peut être réutilisé indépendamment, ce qui facilite l'extension et la maintenance.
* Prêt pour une intégration future avec un orchestrateur comme Airflow ou Luigi pour automatiser les workflows complexes.
#### 2.Apache Beam pour le traitement des données
Apache Beam a été choisi pour sa capacité à gérer des pipelines de données de manière distribuée et scalable, tout en offrant une API unifiée. Il permet d'écrire une seule fois le pipeline et de l'exécuter sur plusieurs moteurs (Dataflow, Spark, etc.), ce qui répond aux besoins de flexibilité, réutilisabilité, et intégration future avec des orchestrateurs comme Airflow.
#### 3.Tests Complets

* Couverture par des tests unitaires pour valider les composants individuels.
* Tests de bout en bout pour garantir la cohérence des données et le bon fonctionnement du pipeline en production.
#### 4.Scalabilité

* En s’appuyant sur Apache Beam, la pipeline peut facilement évoluer pour traiter de plus grands volumes de données ou s'exécuter dans des environnements distribués.


## Pour aller plus loin 
pour pouvoir de grosses volumétries de données il faut prendre en considération les éléments suivant :
###### Infrastructure scalable 
Utiliser une plateforme de calcul distribuée comme Google Cloud Dataflow pour gérer automatiquement les ressources nécessaires.
###### Partitionnement des données :
Découper les fichiers en partitions ou shards pour permettre un traitement parallèle efficace.
Utiliser des formats de fichiers adaptés aux traitements distribués, comme *`Parquet`* ou *`Avro`*.
###### Entrées et sorties :
S'assurer que les données sont stockées dans un système distribué performant (comme Cloud Storage, BigQuery).
Minimiser les écritures intermédiaires et optimiser les lectures en batch.
###### Autoscaling :
Configurer un mécanisme d'autoscaling pour ajuster dynamiquement les ressources (nombre de workers, type de machines) selon la charge.

#### Amélioration à  apporter au code pour prendre de grosses volumétries de données
le code actuel permet de s'intégrer facilement avec GCP et en peux l'éxécuter dans dataflow comme suit :
* installé la dépendance gcp : `pip install apache-beam[gcp]`
* lancer cette command : 
  ```
    python -m apache_beam.examples.wordcount \
    --region DATAFLOW_REGION \
    --data_folder_path gs://dataflow-samples/shakespeare/kinglear.txt \
    --output_folder_path gs://STORAGE_BUCKET/results/outputs \
    --runner DataflowRunner \
    --project PROJECT_ID \
    --temp_location gs://STORAGE_BUCKET/tmp/
  ```
  cependant il faut quand même apporter des modifications permettant notament la lecture de plusieurs fichiers de même type en même temps (drugs1.csv, drugs2.csv ...)ou bien la lecture de d'autres format de fichier mieux adapter (*`Parquet`* ou *`Avro`*)

# SQL
### Première partie
pour trouver le chiffre d’affaires par jour, du 1er janvier 2019 au 31 décembre 201

```
select 
    date,
    sum(prod_price*prod_qty) as ventes
from TRANSACTIONS
where date(date) between '2019/01/01' and '2019/12/31'
group by date
order by date
```

Pour déterminer les ventes meuble et déco réalisées par client et sur la période allant du  1er janvier 2019 au 31 décembre 2019: 
```
SELECT 
    t.client_id AS client_id, 
    SUM(CASE WHEN p.product_type = 'MEUBLE' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_meuble,
    SUM(CASE WHEN p.product_type = 'DECO' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_deco
FROM 
    TRANSACTIONS t
JOIN 
    PRODUCT_NOMENCLATURE p 
ON 
    t.prod_id = p.product_id
WHERE 
    t.date BETWEEN '2019/01/01' AND '2019/12/31'
GROUP BY 
    t.client_id
ORDER BY 
    t.client_id;

```