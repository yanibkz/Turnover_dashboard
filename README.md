# Dashboard de Prédiction de Turnover des Employés

## 🌟 **À propos de ce projet**

Ce **dashboard interactif** a été spécialement conçu pour les **ressources humaines (RH)** afin de **prédire la probabilité qu'un employé quitte l'entreprise**. En utilisant un modèle de régression logistique, ce tableau de bord fournit des **analyses approfondies** et des **visualisations intuitives** pour aider les professionnels RH à **identifier les facteurs clés** influençant le turnover et à **prendre des décisions éclairées** pour réduire le taux de départ des employés.

## 📊 **Fonctionnalités Principales**

- **Prédiction de Turnover**  
  Affiche la probabilité qu'un employé quitte l'entreprise via une **barre de scoring** interactive.

- **Visualisation des Détails**  
  Présente les caractéristiques spécifiques de l'employé sélectionné, permettant une analyse personnalisée.

- **Explications SHAP**  
  Fournit des explications détaillées sur l'impact des différentes caractéristiques (features) sur la prédiction, facilitant la compréhension des résultats.

- **Graphiques de Dispersion**  
  Visualise la distribution des caractéristiques sélectionnées avec indication des valeurs de l'employé, permettant de comparer ses données avec l'ensemble du personnel.

- **Téléchargement des Scores**  
  Offre la possibilité de télécharger les résultats de la prédiction au format CSV pour une analyse ultérieure ou des rapports.

- **Recommandations**  
  Affiche des recommandations basées sur l'analyse des données pour améliorer la rétention des employés et réduire le turnover.

## 💡 **Recommandations et Résultats**

### 👤 **Profil des Collaborateurs qui Quitte l'Entreprise :**

- **Satisfaction Faible**  
  Les employés ayant un niveau de satisfaction faible sont plus susceptibles de quitter l'entreprise.

- **Charge de Travail Déséquilibrée**  
  - **Surcharge** : Heures travaillées > 220.
  - **Sous-utilisation** : Heures travaillées < 150.

- **Salaire Bas**  
  Les employés dans les catégories de salaire bas sont majoritairement touchés par le turnover.

- **Postes à Risque**  
  Les départements **Ressources Humaines (HR)** et **Accounting** présentent un taux de turnover plus élevé.

- **Facteurs Spécifiques**  
  Les employés insatisfaits sont plus aptes à quitter l'entreprise.

### ❓ **Pourquoi les Collaborateurs Quittent-ils ?**

- **Insatisfaction au Travail**  
  - Faible reconnaissance.
  - Mauvaises conditions de travail.

- **Charge de Travail**  
  - **Surmenage (Burnout)** : Trop d'heures de travail.
  - **Sous-engagement (Désintérêt)** : Trop peu d'heures de travail.

- **Rémunération Insuffisante**  
  - Salaire bas perçu comme non compétitif par rapport au marché.

### 💡 **Comment Améliorer le Turnover :**

- **Améliorer la Satisfaction**  
  - Équilibrer les charges de travail.
  - Mieux reconnaître et récompenser les efforts des employés.

- **Offrir des Promotions Régulières**  
  - Clarifier les plans de carrière.
  - Fournir des opportunités de développement professionnel.

- **Augmenter la Rémunération**  
  - Aligner les salaires sur le marché.
  - Introduire des primes de performance.

- **Cibler les Postes Critiques**  
  - Offrir des formations spécifiques.
  - Fournir un soutien supplémentaire pour les départements Accounting et RH.

## 🎨 **Design et Accessibilité**

Pour garantir une **expérience utilisateur optimale** et une **accessibilité conforme**, ce dashboard respecte les **critères de succès** suivants issus des [Web Content Accessibility Guidelines (WCAG) 2.1](https://www.w3.org/Translations/WCAG21-fr/) du W3C :

1. **Critère de succès 1.1.1 Contenu non textuel**  
   Assurer que tout contenu non textuel dispose d'une alternative textuelle afin que les utilisateurs ayant des déficiences visuelles puissent comprendre l'information.

2. **Critère de succès 1.4.1 Utilisation de la couleur**  
   Ne pas utiliser la couleur comme seul moyen de transmettre l'information, permettant ainsi aux utilisateurs daltoniens de naviguer efficacement dans le dashboard.

3. **Critère de succès 1.4.3 Contraste (minimum)**  
   Maintenir un contraste suffisant entre le texte et le fond pour garantir une lisibilité optimale, notamment pour les utilisateurs ayant une vision réduite.

4. **Critère de succès 1.4.4 Redimensionnement du texte**  
   Permettre aux utilisateurs de redimensionner le texte jusqu'à 200% sans perte de contenu ou de fonctionnalité, facilitant la lecture pour ceux ayant des difficultés visuelles.

5. **Critère de succès 2.4.2 Titre de page**  
   Fournir un titre de page unique et descriptif pour chaque page du dashboard, aidant les utilisateurs à comprendre rapidement le contenu et la fonction de chaque section.

### 🌈 **Palette de Couleurs et Typographie**

- **Couleurs**  
  Utilisation de couleurs contrastées et harmonieuses pour faciliter la lecture et la navigation.
  
- **Typographie**  
  Choix de polices lisibles et bien espacées pour améliorer la compréhension et l'accessibilité.

## 🚀 **Déploiement de l'Application**

L'application est déployée sur [Streamlit Cloud](https://streamlit.io/cloud) pour un accès facile et une utilisation interactive. Les utilisateurs peuvent accéder au dashboard en suivant le lien ci-dessous :

[Accéder au Dashboard de Prédiction de Turnover](https://share.streamlit.io/votre_nom_utilisateur/votre_depot/main/Home.py)

*Remplacez l'URL ci-dessus par le lien réel de votre application déployée sur Streamlit Cloud.*

## 📚 **Source**

Ces critères de succès sont issus des [Web Content Accessibility Guidelines (WCAG) 2.1](https://www.w3.org/Translations/WCAG21-fr/) élaborées par le W3C (World Wide Web Consortium).

## 🤝 **Contribuer**

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, veuillez suivre les étapes suivantes :

1. Forkez ce dépôt.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`).
3. Commitez vos changements (`git commit -m 'Add some AmazingFeature'`).
4. Poussez vers la branche (`git push origin feature/AmazingFeature`).
5. Ouvrez une Pull Request.
