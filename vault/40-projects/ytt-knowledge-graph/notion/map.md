These diagrams are generated from the CSV dataset in tide (`40-projects/ytt-knowledge-graph`). The dataset was drafted by Claude from memory, so verify dates and attributions before teaching them. For the interactive version with portraits, open the [Yoga Lineage Atlas](https://claude.ai/artifact/GmnMQKiVqocJYwViegS8uK).

## Lineage tree
Solid arrows run parent → branch. Dotted arrows are a secondary influence.
```mermaid
flowchart TD
  L001["Yoga (all traditions)"]
  L002["Pre-classical (Vedic; Upaniṣadic; Gītā)"]
  L003["Classical (Sāṃkhya-Yoga / Patañjala)"]
  L004["Tantric yoga"]
  L005["Haṭha yoga (premodern)"]
  L006["Modern yoga (c. 1890–present)"]
  L007["Vedānta societies (Vivekananda)"]
  L008["Kriya Yoga / Self-Realization"]
  L009["Integral Yoga (Aurobindo)"]
  L010["Scientific and institutional yoga"]
  L011["Krishnamacharya lineage (Mysore)"]
  L012["Ashtanga Vinyasa"]
  L013["Iyengar Yoga"]
  L014["Viniyoga"]
  L015["Indra Devi style"]
  L016["Power Yoga and Vinyasa Flow"]
  L017["Sivananda lineage"]
  L018["Sivananda Yoga (Vishnudevananda)"]
  L019["Integral Yoga (Satchidananda)"]
  L020["Bihar School of Yoga (Satyananda)"]
  L021["Siddha Yoga (Muktananda)"]
  L022["Himalayan Institute (Swami Rama)"]
  L023["Kundalini Yoga (Yogi Bhajan)"]
  L024["Kripalu Yoga"]
  L025["Ghosh lineage and Hot Yoga (Bikram)"]
  L026["Transcendental Meditation"]
  L027["Western hybrid and therapeutic styles"]
  L028["Jivamukti"]
  L029["Anusara"]
  L030["Yin Yoga"]
  L031["Restorative Yoga"]
  L032["Forrest Yoga"]
  L001 --> L002
  L001 --> L003
  L001 --> L004
  L004 --> L005
  L001 --> L006
  L005 -.-> L006
  L006 --> L007
  L006 --> L008
  L006 --> L009
  L006 --> L010
  L006 --> L011
  L011 --> L012
  L011 --> L013
  L011 --> L014
  L011 --> L015
  L012 --> L016
  L006 --> L017
  L017 --> L018
  L017 --> L019
  L017 --> L020
  L006 --> L021
  L006 --> L022
  L006 --> L023
  L006 --> L024
  L006 --> L025
  L006 --> L026
  L006 --> L027
  L027 --> L028
  L012 -.-> L028
  L017 -.-> L028
  L027 --> L029
  L013 -.-> L029
  L027 --> L030
  L027 --> L031
  L013 -.-> L031
  L027 --> L032
  classDef era fill:#f4ead5,stroke:#8a6d3b
  classDef style fill:#e3eef7,stroke:#4a7aa0
  class L001,L002,L003,L004,L005,L006 era
  class L016,L028,L029,L030,L031,L032 style
```

## Who taught whom
Grouped by school. Solid arrows run teacher → student; dashed means the link is known only from traditional accounts. Grey rounded boxes are teachers outside the dataset.
```mermaid
flowchart LR
  subgraph L008_g["Kriya Yoga / Self-Realization"]
    F001["Lahiri Mahasaya<br/>1828–1895"]
    F004["Sri Yukteswar Giri<br/>1855–1936"]
    F005["Paramahansa Yogananda<br/>1893–1952"]
  end
  subgraph L007_g["Vedānta societies"]
    F002["Swami Vivekananda<br/>1863–1902"]
  end
  subgraph L009_g["Integral Yoga"]
    F003["Sri Aurobindo<br/>1872–1950"]
  end
  subgraph L010_g["Scientific and institutional yoga"]
    F006["Swami Kuvalayananda<br/>1883–1966"]
    F007["Shri Yogendra<br/>1897–1989"]
  end
  subgraph L017_g["Sivananda lineage"]
    F008["Swami Sivananda<br/>1887–1963"]
  end
  subgraph L011_g["Krishnamacharya lineage"]
    F009["Tirumalai Krishnamacharya<br/>1888–1989"]
  end
  subgraph L012_g["Ashtanga Vinyasa"]
    F010["K. Pattabhi Jois<br/>1915–2009"]
  end
  subgraph L013_g["Iyengar Yoga"]
    F011["B.K.S. Iyengar<br/>1918–2014"]
  end
  subgraph L015_g["Indra Devi style"]
    F012["Indra Devi<br/>1899–2002"]
  end
  subgraph L014_g["Viniyoga"]
    F013["T.K.V. Desikachar<br/>1938–2016"]
  end
  subgraph L018_g["Sivananda Yoga"]
    F014["Swami Vishnudevananda<br/>1927–1993"]
  end
  subgraph L019_g["Integral Yoga"]
    F015["Swami Satchidananda<br/>1914–2002"]
  end
  subgraph L020_g["Bihar School of Yoga"]
    F016["Swami Satyananda Saraswati<br/>1923–2009"]
  end
  subgraph L022_g["Himalayan Institute"]
    F017["Swami Rama<br/>1925–1996"]
  end
  subgraph L026_g["Transcendental Meditation"]
    F018["Maharishi Mahesh Yogi<br/>1918–2008"]
  end
  subgraph L023_g["Kundalini Yoga"]
    F019["Yogi Bhajan<br/>1929–2004"]
  end
  subgraph L025_g["Ghosh lineage and Hot Yoga"]
    F020["Bishnu Charan Ghosh<br/>1903–1970"]
    F021["Bikram Choudhury<br/>1944–"]
  end
  subgraph L021_g["Siddha Yoga"]
    F022["Swami Muktananda<br/>1908–1982"]
  end
  subgraph L024_g["Kripalu Yoga"]
    F023["Swami Kripalvananda<br/>1913–1981"]
    F024["Amrit Desai<br/>1932–"]
  end
  subgraph L027_g["Western hybrid and therapeutic styles"]
    F025["Richard Hittleman<br/>1927–1991"]
  end
  subgraph L028_g["Jivamukti"]
    F026["Sharon Gannon and David Life"]
  end
  subgraph L029_g["Anusara"]
    F027["John Friend"]
  end
  subgraph L016_g["Power Yoga and Vinyasa Flow"]
    F028["Beryl Bender Birch"]
    F029["Baron Baptiste"]
  end
  subgraph L032_g["Forrest Yoga"]
    F030["Ana Forrest"]
  end
  subgraph L030_g["Yin Yoga"]
    F031["Paul Grilley"]
    F032["Paulie Zink"]
  end
  subgraph L006_g["Modern yoga"]
    F033["Mark Singleton"]
    F034["Elizabeth De Michelis"]
    F035["Joseph Alter"]
    F037["Georg Feuerstein<br/>1947–2012"]
  end
  subgraph L005_g["Haṭha yoga"]
    F036["James Mallinson"]
  end
  X1(["Mahavatar Babaji"]):::ext
  X1 -.-> F001
  X2(["Ramakrishna Paramahamsa"]):::ext
  X2 --> F002
  F001 --> F004
  F004 --> F005
  X3(["Paramahamsa Madhavdasji"]):::ext
  X3 --> F006
  X3 --> F007
  X4(["Rāmamohana Brahmacāri"]):::ext
  X4 -.-> F009
  F009 --> F010
  F009 --> F011
  F009 --> F012
  F009 --> F013
  F008 --> F014
  F008 --> F015
  F008 --> F016
  X5(["Bengali Baba"]):::ext
  X5 -.-> F017
  X6(["Swami Brahmananda Saraswati"]):::ext
  X6 --> F018
  F020 --> F021
  X7(["Bhagawan Nityananda"]):::ext
  X7 --> F022
  F023 --> F024
  F010 --> F028
  F032 --> F031
  F020 -. sibling .- F005
  F009 -. parent .- F013
  F036 -. co-author .- F033
  classDef ext fill:#eee,stroke:#999,color:#555
```

## Timeline: premodern
```mermaid
timeline
  title Premodern yoga (dates approximate; verify)
  section Proto-historic
    c. 2600–1900 BCE : Indus Valley civilization
  section Vedic
    c. 1500–1000 BCE : Ṛgveda composed
    c. 1200–900 BCE : Atharvaveda compiled
  section Brahmana-Aranyaka
    c. 900–600 BCE : Brāhmaṇas and Āraṇyakas interiorize ritual
  section Upanishadic
    c. 800–500 BCE : Early prose Upaniṣads ātman-brahman and inner sacrifice
    c. 5th–3rd c. BCE : Kaṭha Upaniṣad defines yoga chariot metaphor
    c. 4th–2nd c. BCE : Śvetāśvatara Upaniṣad posture and breath
    c. 3rd c. BCE–1st c. CE : Maitrī Upaniṣad six-limbed yoga
  section Sramana
    c. 6th–4th c. BCE : Śramaṇa movements the Buddha and Mahāvīra
  section Epic
    c. 200 BCE–200 CE : Mahābhārata and the Bhagavad Gītā
  section Classical
    c. 2nd c. BCE–4th c. CE debated : Patañjali's Yoga Sūtras compiled
    c. 4th–5th c. CE : Sāṃkhyakārikā 25 tattvas and three guṇas
    c. 5th c. CE : Vyāsa's Yoga Bhāṣya
    c. 10th c. CE : Vācaspati Miśra's Tattvavaiśāradī
  section Tantric
    c. 6th–10th c. CE : Tantric traditions mantra, cakras, kuṇḍalinī
  section Early Hatha
    c. 11th–13th c. CE : Nāth Siddhas develop haṭha techniques
  section Hatha
    c. 15th c. CE : Haṭha Yoga Pradīpikā compiled
    c. 17th–18th c. CE : Later haṭha compendia expand posture lists
```

## Timeline: modern
```mermaid
timeline
  title Modern yoga 1875–present (verify)
  section Colonial
    1875–1900 : Theosophy and Orientalism recast yoga
  section Modern
    1893–1896 : Vivekananda in Chicago; Rāja Yoga
    c. 1900–1930 : Physical culture meets yoga; modern postural yoga forms
    1918 : The Yoga Institute founded Bombay
    1920 : Yogananda arrives in the US; SRF founded
    1924 : Kaivalyadhama founded; yoga research begins
    1933–1934 : Krishnamacharya at the Mysore Palace
    1936 : Divine Life Society founded Rishikesh
    1946 : Autobiography of a Yogi published
    1947–1948 : Indra Devi in Hollywood; Jois's institute in Mysore
    1952–1954 : Menuhin brings Iyengar to the West
    1959 : First Sivananda Yoga Vedanta Centre Montréal
    1961–c. 1970 : Television yoga Hittleman; Lilias
    1966 : Light on Yoga published; Integral Yoga Institute NYC
    1967–1969 : Counterculture Beatles, Woodstock, 3HO
    1971–1975 : Institutions consolidate Himalayan Institute, Pune, Yoga Journal
    c. 1973 : Bikram's Beverly Hills studio hot yoga
    1976 : Krishnamacharya Yoga Mandiram founded Chennai
    1984–1999 : Studio-yoga boom Jivamukti, Power Yoga, Anusara
    2010s–present : Misconduct reckonings and ethics debates
    2014–2015 : International Day of Yoga proclaimed
  section Scholarship
    2004–2010 : Critical histories of modern yoga
```

## Sāṃkhya: puruṣa, prakṛti and the tattvas
```mermaid
flowchart TD
  P001["Puruṣa<br/>Pure consciousness (witness)"]
  P002["Prakṛti (mūla-prakṛti; pradhāna; avyakta)<br/>Primal nature (unmanifest matter-energy)"]
  P003["Buddhi (mahat)<br/>Intellect (discernment)"]
  P004["Ahaṃkāra<br/>I-maker (ego-sense)"]
  P005["Manas<br/>Sense-mind (coordinating mind)"]
  P006["Jñānendriyas (group)<br/>Five sense capacities"]
  P007["Śrotra<br/>Hearing (ear)"]
  P008["Tvak<br/>Touch (skin)"]
  P009["Cakṣus<br/>Sight (eye)"]
  P010["Rasanā<br/>Taste (tongue)"]
  P011["Ghrāṇa<br/>Smell (nose)"]
  P012["Karmendriyas (group)<br/>Five action capacities"]
  P013["Vāk<br/>Speech (voice)"]
  P014["Pāṇi<br/>Grasping (hands)"]
  P015["Pāda<br/>Locomotion (feet)"]
  P016["Pāyu<br/>Excretion"]
  P017["Upastha<br/>Generation (procreation)"]
  P018["Tanmātras (group)<br/>Five subtle elements"]
  P019["Śabda-tanmātra<br/>Subtle sound"]
  P020["Sparśa-tanmātra<br/>Subtle touch"]
  P021["Rūpa-tanmātra<br/>Subtle form (color)"]
  P022["Rasa-tanmātra<br/>Subtle taste"]
  P023["Gandha-tanmātra<br/>Subtle smell"]
  P024["Mahābhūtas (group)<br/>Five gross elements"]
  P025["Ākāśa<br/>Space (ether)"]
  P026["Vāyu<br/>Air"]
  P027["Tejas (agni)<br/>Fire (light)"]
  P028["Āpas (jala)<br/>Water"]
  P029["Pṛthvī<br/>Earth"]
  P030["Īśvara<br/>Special puruṣa (Lord)"]
  P031["Citta (Yoga usage)<br/>Mind-stuff (buddhi + ahaṃkāra + manas working together)"]
  P032["Saṃyoga (puruṣa-prakṛti conjunction)<br/>Association of seer and seen"]
  P033["Kaivalya (isolation)<br/>Puruṣa abides in its own nature; guṇas return to latency"]
  P034["Sāmya / Vaiṣamya<br/>Equilibrium / disturbance of the guṇas"]
  G001["Sattva<br/>Lucidity; purity; balance"]
  G002["Rajas<br/>Activity; passion; movement"]
  G003["Tamas<br/>Inertia; heaviness; obscuration"]
  P002 --> P003
  P003 --> P004
  P004 --> P005
  P004 --> P006
  P006 --> P007
  P006 --> P008
  P006 --> P009
  P006 --> P010
  P006 --> P011
  P004 --> P012
  P012 --> P013
  P012 --> P014
  P012 --> P015
  P012 --> P016
  P012 --> P017
  P004 --> P018
  P018 --> P019
  P018 --> P020
  P018 --> P021
  P018 --> P022
  P018 --> P023
  P018 --> P024
  P019 --> P025
  P020 --> P026
  P021 --> P027
  P022 --> P028
  P023 --> P029
  P002 --> P034
  P002 --> G001
  P002 --> G002
  P002 --> G003
  P001 -. saṃyoga .- P002
```

## Āsana names by category
```mermaid
mindmap
  root((āsana names))
    action
      Uttānāsana — standing forward fold
      Utthita Trikoṇāsana — extended triangle
      Baddha Koṇāsana — bound angle
      Upaviṣṭa Koṇāsana — seated angle
      Pavanamuktāsana — wind-relieving pose
    animal
      Adho Mukha Śvānāsana — downward-facing dog
      Ūrdhva Mukha Śvānāsana — upward-facing dog
      Bhujaṅgāsana — cobra pose
      Śalabhāsana — locust pose
      Uṣṭrāsana — camel pose
      Matsyāsana — fish pose
      Gomukhāsana — cow-face pose
      Mayūrāsana — peacock pose
      Bakāsana — crane pose
      Kūrmāsana — tortoise pose
      Garuḍāsana — eagle pose
      Kapotāsana — pigeon pose
    body
      Pādahastāsana — hands-to-feet
      Jānu Śīrṣāsana — head-to-knee
      Śīrṣāsana — headstand
      Sarvāṅgāsana — shoulderstand
      Karṇapīḍāsana — ear-pressure pose
    concept
      āsana — posture
      yoga — union
    deity
      Vīrabhadrāsana — warrior pose
      Naṭarājāsana — lord of the dance
      Hanumānāsana — Hanuman's pose splits
    descriptor
      Utkaṭāsana — chair pose fierce pose
      Vīrāsana — hero pose
      Bālāsana — child's pose
      Siddhāsana — accomplished pose
      Svastikāsana — auspicious pose
      Sukhāsana — easy pose
      Śavāsana — corpse pose
      Ānanda Bālāsana — happy baby
    direction
      Pārśvakoṇāsana — side-angle
      Paścimottānāsana — seated forward fold
    modifier
      Utthita modifier — extended
      Parivṛtta modifier — revolved
      Supta modifier — reclining
      Ardha modifier — half
      Eka Pāda modifier — one-footed
      Prasārita modifier — spread out
    nature
      Tāḍāsana — mountain pose
      Vṛkṣāsana — tree pose
      Padmāsana — lotus pose
      Ardha Candrāsana — half moon
    number
      Trikoṇāsana — triangle
      Caturaṅga Daṇḍāsana — four-limbed staff
    object
      Dhanurāsana — bow pose
      Setu Bandhāsana — bridge pose
      Vajrāsana — thunderbolt pose
      Halāsana — plough pose
      Daṇḍāsana — staff pose
      Nāvāsana — boat pose
      Mālāsana — garland pose
    person
      Ardha Matsyendrāsana — half spinal twist half lord of the fishes
      Aṣṭāvakrāsana — eight-angle pose
      Vasiṣṭhāsana — side plank
    practice
      Prāṇāyāma — breath regulation
      Bandha — lock
    sequence
      Sūrya Namaskāra — sun salutation
    standing
      Samasthiti — equal standing
```
